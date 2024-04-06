# import unittest
# import os
# from unittest.mock import patch, MagicMock
# from reels.butcher import download_video, download_videos


# class TestDownload(unittest.TestCase):
#     @patch("pytube.YouTube")
#     def test_download_video(self, mock_youtube):
#         # Mock YouTube object
#         yt_mock = MagicMock()
#         yt_mock.title = "Test Video Title"
#         mock_youtube.return_value = yt_mock

#         # Mock Stream object
#         stream_mock = MagicMock()
#         stream_mock.download = MagicMock()
#         yt_mock.streams.filter.return_value.order_by.return_value.desc.return_value.first.return_value = (
#             stream_mock
#         )

#         # Test downloading video
#         output_folder = "test_output"
#         download_video("https://www.youtube.com/watch?v=testvideo", output_folder)
#         expected_filename = os.path.join(output_folder, "Test_Video_Title.mp4")
#         self.assertTrue(os.path.exists(expected_filename))

#     @patch("pytube.YouTube")
#     def test_download_videos(self, mock_youtube):
#         # Mock YouTube object
#         yt_mock = MagicMock()
#         yt_mock.title = "Test Video Title"
#         mock_youtube.return_value = yt_mock

#         # Mock Stream object
#         stream_mock = MagicMock()
#         stream_mock.download = MagicMock()
#         yt_mock.streams.filter.return_value.order_by.return_value.desc.return_value.first.return_value = (
#             stream_mock
#         )

#         # Test downloading videos
#         output_folder = "test_output"
#         urls = [
#             "https://www.youtube.com/watch?v=testvideo1",
#             "https://www.youtube.com/watch?v=testvideo2",
#         ]
#         download_videos(urls, output_folder)

#         expected_filenames = [os.path.join(output_folder, "Test_Video_Title.mp4")] * 2
#         for expected_filename in expected_filenames:
#             self.assertTrue(os.path.exists(expected_filename))

#     def test_download_videos_non_youtube(self):
#         with patch("builtins.print") as mock_print:
#             output_folder = "test_output"
#             urls = ["https://example.com/video"]
#             download_videos(urls, output_folder)
#             mock_print.assert_called_with(
#                 "Not a YouTube link: https://example.com/video"
#             )


# if __name__ == "__main__":
#     unittest.main()
