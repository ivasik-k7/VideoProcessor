import unittest
from unittest.mock import Mock, patch

import ffmpeg

from app.ffmpeg_utils import FFmpegProcessor


class TestFFmpegProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = FFmpegProcessor()

    @patch("ffmpeg.run")
    def test_run_success(self, mock_run):
        mock_run.return_value = (b"stdout data", b"stderr data")
        stream_spec = Mock()

        stdout, stderr = self.processor.run(stream_spec, overwrite_output=True)

        mock_run.assert_called_once_with(
            stream_spec,
            overwrite_output=True,
            capture_stdout=True,
            capture_stderr=True,
        )
        self.assertEqual(stdout, b"stdout data")
        self.assertEqual(stderr, b"stderr data")

    @patch("ffmpeg.run")
    def test_run_failure(self, mock_run):
        error = ffmpeg.Error("An error occurred", b"error details", b"stderr data")
        mock_run.side_effect = error
        stream_spec = Mock()

        with self.assertRaises(RuntimeError) as context:
            self.processor.run(stream_spec, overwrite_output=True)

        self.assertIn("Failed to execute FFmpeg command", str(context.exception))

    @patch("ffmpeg.input")
    def test_input_success(self, mock_input):
        mock_stream = Mock()
        mock_input.return_value = mock_stream
        file_path = " test.mp4 "

        result = self.processor.input(file_path, t=20, f="mp4")

        mock_input.assert_called_once_with("test.mp4", t=20, f="mp4")
        self.assertEqual(result, mock_stream)

    @patch("ffmpeg.input")
    def test_input_failure(self, mock_input):
        error = ffmpeg.Error("An error occurred", b"error details", b"stderr data")
        mock_input.side_effect = error
        file_path = " test.mp4 "

        with self.assertRaises(RuntimeError) as context:
            self.processor.input(file_path, t=20, f="mp4")

        self.assertIn("Failed to load audio", str(context.exception))

    @patch("ffmpeg.output")
    def test_output_success(self, mock_output):
        mock_stream = Mock()
        mock_output.return_value = mock_stream
        stream1 = Mock()
        stream2 = Mock()
        output_filename = "output.mp4"

        result = self.processor.output(stream1, stream2, output_filename, c="copy")

        mock_output.assert_called_once_with(stream1, stream2, output_filename, c="copy")
        self.assertEqual(result, mock_stream)

    @patch("ffmpeg.output")
    def test_output_failure(self, mock_output):
        error = ffmpeg.Error("An error occurred", b"error details", b"stderr data")
        mock_output.side_effect = error
        stream1 = Mock()
        stream2 = Mock()
        output_filename = "output.mp4"

        with self.assertRaises(RuntimeError) as context:
            self.processor.output(stream1, stream2, output_filename, c="copy")

        self.assertIn("Failed to create FFmpeg output stream", str(context.exception))


if __name__ == "__main__":
    unittest.main()
