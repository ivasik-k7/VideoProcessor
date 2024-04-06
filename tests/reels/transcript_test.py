import unittest
from unittest.mock import Mock, patch
from reels.transcript import (
    ffmpeg_input_stream,
    output_audio_stream,
    run_ffmpeg,
    extract_audio,
)


class TestFFMPEG(unittest.TestCase):
    def test_ffmpeg_input_stream(self):
        input_path = "test_video.mp4"
        stream = ffmpeg_input_stream(input_path)
        self.assertIsNotNone(stream)

    def test_output_audio_stream(self):
        input_path = "path/to/input_video.mp4"
        stream = ffmpeg_input_stream(input_path)
        extracted_audio = "path/to/extracted_audio.wav"
        output_stream = output_audio_stream(stream, extracted_audio)
        self.assertIsNotNone(output_stream)

    @patch("reels.transcript.ffmpeg.run")
    def test_run_ffmpeg(self, mock_ffmpeg_run):
        stream = Mock()
        run_ffmpeg(stream)
        mock_ffmpeg_run.assert_called_once_with(stream, overwrite_output=True)


class TestTranscript(unittest.TestCase):
    def test_extract_audio(self):
        input_video_path = "test_video.mp4"
        with patch("os.path.exists", return_value=True), patch(
            "reels.transcript.utils.is_video_file", return_value=True
        ), patch("reels.transcript.ffmpeg.run") as mock_run_ffmpeg:
            extract_audio(input_video_path)
            mock_run_ffmpeg.assert_called_once()

    def test_extract_audio_missing_input(self):
        input_video_path = "missing_video.mp4"
        with self.assertRaises(FileNotFoundError):
            extract_audio(input_video_path)


# def test_generate_subtitle_file(self):
#     segments = [{"start": 0, "end": 5, "text": "Test subtitle"}]
#     input_video_path = "test_video.mp4"
#     language = "en"
#     output_dir = "./"
#     subtitle_file = generate_subtitle_file(
#         language, segments, input_video_path, output_dir
#     )
#     expected_subtitle_file = f"sub-test_video.{language}.srt"
#     self.assertEqual(subtitle_file, expected_subtitle_file)


if __name__ == "__main__":
    unittest.main()
