"""Offline regressions for SD file preservation and UART resource cleanup.

No serial device or pySerial installation is used. Run with:
    python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import m300_console
import prepare_service_sd


class ServiceCardTests(unittest.TestCase):
    def prepare(self, folder):
        with contextlib.redirect_stdout(io.StringIO()):
            prepare_service_sd.prepare(folder)

    def test_missing_files_are_complete_a5_templates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.prepare(root)
            for name, size in prepare_service_sd.FILES.items():
                self.assertEqual((root / name).read_bytes(), b'\xa5' * size)

    def test_existing_completed_files_are_preserved_verbatim(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            originals = {}
            for index, (name, size) in enumerate(prepare_service_sd.FILES.items()):
                originals[name] = bytes([index + 1]) * size
                (root / name).write_bytes(originals[name])
            self.prepare(root)
            self.assertEqual({p.name: p.read_bytes() for p in root.iterdir()}, originals)

    def test_wrong_size_aborts_before_creating_missing_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            # The invalid entry is last in creation order: no earlier template
            # may be created before the whole existing set has been checked.
            invalid = root / 'M3LOG.BIN'
            invalid.write_bytes(b'preserve truncated data')
            with self.assertRaisesRegex(ValueError, 'expected 4096'):
                self.prepare(root)
            self.assertEqual(list(root.iterdir()), [invalid])
            self.assertEqual(invalid.read_bytes(), b'preserve truncated data')

    def test_directory_is_rejected_before_other_files_are_created(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            invalid = root / 'M3INFO.BIN'
            invalid.mkdir()
            with self.assertRaisesRegex(ValueError, 'regular file'):
                self.prepare(root)
            self.assertEqual(list(root.iterdir()), [invalid])
            self.assertTrue(invalid.is_dir())

    def test_existing_and_dangling_symlinks_are_not_followed(self):
        for dangling in (False, True):
            with self.subTest(dangling=dangling), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp) / 'card'
                root.mkdir()
                target = Path(tmp) / 'private-backup.bin'
                if not dangling:
                    target.write_bytes(b'\x5a' * 262144)
                link = root / 'M3FLASH.BIN'
                link.symlink_to(target)
                with self.assertRaisesRegex(ValueError, 'regular file'):
                    self.prepare(root)
                self.assertEqual(list(root.iterdir()), [link])
                self.assertTrue(link.is_symlink())
                if dangling:
                    self.assertFalse(target.exists())
                else:
                    self.assertEqual(target.read_bytes(), b'\x5a' * 262144)


class FakeSerial:
    def __init__(self, open_error=None, close_error=None, **settings):
        self.settings = settings
        self.open_error = open_error
        self.close_error = close_error
        self.open_count = 0
        self.close_count = 0

    def open(self):
        self.open_count += 1
        if self.open_error is not None:
            raise self.open_error

    def close(self):
        self.close_count += 1
        if self.close_error is not None:
            raise self.close_error


class ConsoleResourceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.handles = []
        self.devices = []
        self.open_error = None
        self.close_error = None
        original_open = Path.open

        def record_open(path, *args, **kwargs):
            handle = original_open(path, *args, **kwargs)
            self.handles.append(handle)
            return handle

        def new_serial(**settings):
            device = FakeSerial(self.open_error, self.close_error, **settings)
            self.devices.append(device)
            return device

        self.path_patch = mock.patch.object(Path, 'open', record_open)
        self.path_patch.start()
        self.addCleanup(self.path_patch.stop)
        self.serial_patch = mock.patch.dict(sys.modules, {'serial': types.SimpleNamespace(Serial=new_serial)})
        self.serial_patch.start()
        self.addCleanup(self.serial_patch.stop)

    def make_link(self):
        return m300_console.Link('FAKE_UART_NO_DEVICE', 750000, self.root)

    def test_successful_connection_closes_all_resources_once(self):
        link = self.make_link()
        device = self.devices[0]
        self.assertEqual(device.settings['baudrate'], 750000)
        self.assertIsNone(device.settings['port'])
        self.assertFalse(device.dtr)
        self.assertFalse(device.rts)
        self.assertEqual(device.open_count, 1)
        link.close()
        link.close()
        self.assertEqual(device.close_count, 1)
        self.assertTrue(all(handle.closed for handle in self.handles))

    def test_open_failure_closes_partial_resources(self):
        self.open_error = OSError('injected open failure')
        with self.assertRaisesRegex(OSError, 'injected open failure'):
            self.make_link()
        self.assertEqual(self.devices[0].close_count, 1)
        self.assertEqual(len(self.handles), 2)
        self.assertTrue(all(handle.closed for handle in self.handles))

    def test_cleanup_failure_does_not_mask_original_open_error(self):
        self.open_error = OSError('original connection failure')
        self.close_error = OSError('secondary close failure')
        with self.assertRaisesRegex(OSError, 'original connection failure'):
            self.make_link()
        self.assertTrue(all(handle.closed for handle in self.handles))

    def test_serial_close_failure_still_closes_both_logs(self):
        self.close_error = OSError('injected close failure')
        link = self.make_link()
        with self.assertRaisesRegex(OSError, 'injected close failure'):
            link.close()
        self.assertTrue(all(handle.closed for handle in self.handles))
        link.close()
        self.assertEqual(self.devices[0].close_count, 1)

    def test_existing_log_is_preserved_and_serial_never_opens(self):
        existing = self.root / 'UART.log'
        existing.write_text('previous session')
        with self.assertRaises(FileExistsError):
            self.make_link()
        self.assertEqual(existing.read_text(), 'previous session')
        self.assertEqual(self.devices[0].open_count, 0)
        self.assertEqual(self.devices[0].close_count, 1)
        self.assertTrue(all(handle.closed for handle in self.handles))


class ConsoleProtocolTests(unittest.TestCase):
    def handshake(self, info):
        link = object.__new__(m300_console.Link)
        link.line = mock.Mock(return_value=b'READY')
        link.send = mock.Mock()
        link.response = mock.Mock(side_effect=[[b'DONE ECHO_OFF'], info, [b'PONG M300BOOT']])
        with contextlib.redirect_stdout(io.StringIO()):
            return link.handshake()

    def test_exact_current_info_and_board_identity_are_accepted(self):
        self.assertIn('v1.5', self.handshake([b'M300BOOT v1.5', b'BOARD_CHECK OK']))

    def test_prefix_versions_and_decorated_board_results_are_rejected(self):
        for info in ([b'M300BOOT v1.50', b'BOARD_CHECK OK'],
                     [b'M300BOOT v1.5.1', b'BOARD_CHECK OK'],
                     [b'M300BOOT v1.4.1', b'BOARD_CHECK OK'],
                     [b'M300BOOT v1.4', b'BOARD_CHECK OK'],
                     [b'NOT M300BOOT v1.5', b'BOARD_CHECK OK'],
                     [b'M300BOOT v1.5', b'NOT BOARD_CHECK OK']):
            with self.subTest(info=info), self.assertRaisesRegex(RuntimeError, 'Niepotwierdzony'):
                self.handshake(info)

    def test_close_error_preserves_manifest_archive_and_failure_exit(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'session'
            link = mock.Mock()
            link.handshake.return_value = 'M300BOOT v1.5\nBOARD_CHECK OK'
            link.close.side_effect = OSError('injected close failure')
            with mock.patch.object(m300_console, 'Link', return_value=link), contextlib.redirect_stdout(io.StringIO()):
                code = m300_console.main(['--port', 'FAKE_UART_NO_DEVICE', '--out', str(out)])
            self.assertEqual(code, 2)
            report = json.loads((out / 'MANIFEST.json').read_text())
            self.assertEqual(report['status'], 'FAIL')
            self.assertEqual(report['close_error'], 'injected close failure')
            self.assertTrue(out.with_suffix('.zip').is_file())
            link.close.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
