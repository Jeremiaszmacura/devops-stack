import logging
import os
import tempfile
import unittest

from logger import configure_logging, logger


class TestConfigureLogging(unittest.TestCase):
    """Tests for logger.configure_logging."""

    def test_creates_logs_dir_and_log_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            logs_dir = os.path.join(tmp_dir, "logs")
            logs_file_path = configure_logging(logs_dir)

            self.assertTrue(os.path.isdir(logs_dir))
            self.assertTrue(logs_file_path.startswith(logs_dir))

    def test_attaches_file_and_console_handlers(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            configure_logging(tmp_dir)

            handler_types = {type(handler) for handler in logger.handlers}
            self.assertIn(logging.FileHandler, handler_types)
            self.assertIn(logging.StreamHandler, handler_types)

    def test_does_not_duplicate_handlers_when_called_twice(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            configure_logging(tmp_dir)
            handler_count_first = len(logger.handlers)

            configure_logging(tmp_dir)

            self.assertEqual(len(logger.handlers), handler_count_first)


if __name__ == "__main__":
    unittest.main()
