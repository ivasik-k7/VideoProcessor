import tempfile
import unittest
import os

from reels.utils import (
    clean_file_name,
    create_directory,
    get_files_in_directory,
    is_video_file,
    get_file_name_without_extension,
    format_time,
    create_directory_for_file,
)


class UtilsTests(unittest.TestCase):

    def test_create_directory_for_file(self):
        file_path = "./README.md"

        create_directory_for_file(file_path)

        self.assertTrue(os.path.exists(os.path.dirname(file_path)))

    def test_create_directory_for_existing_file(self):
        file_path = "./README.md"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        create_directory_for_file(file_path)

        self.assertTrue(os.path.exists(os.path.dirname(file_path)))

    def test_format_time(self):
        assert format_time(3661.234) == "01:01:01,234"
        assert format_time(7200) == "02:00:00,000"
        assert format_time(123.456) == "00:02:03,456"

        assert format_time(0) == "00:00:00,000"
        assert format_time(1) == "00:00:01,000"
        assert format_time(3600) == "01:00:00,000"

        assert format_time(-123.456) == "-00:02:03,456"

        assert format_time(123456789) == "34293:33:09,000"

        assert format_time(123.456) == "00:02:03,456"
        assert format_time(123.0) == "00:02:03,000"
        assert format_time(123.999) == "00:02:03,999"

        assert format_time(86400.123) == "24:00:00,123"

    def test_clean_file_name(self):
        self.assertEqual(clean_file_name("abc.xyz"), "abc.xyz")
        self.assertEqual(
            clean_file_name("a!b#c$d%e^f&g*h(i)j_k"), "a_b_c_d_e_f_g_h_i_j_k"
        )
        self.assertEqual(clean_file_name("  abc def  "), "abcdef")
        self.assertEqual(clean_file_name("a___b___c"), "a_b_c")

    def test_create_directory(self):
        directory = "test_directory"
        create_directory(directory)
        self.assertTrue(os.path.exists(directory))
        os.rmdir(directory)

    def test_get_file_name_without_extension(self):
        self.assertEqual(get_file_name_without_extension("/path/to/file.txt"), "file")
        self.assertEqual(get_file_name_without_extension("/path/to/image.jpg"), "image")
        self.assertEqual(
            get_file_name_without_extension("/path/to/document.pdf"), "document"
        )
        self.assertEqual(get_file_name_without_extension("/path/to/audio.mp3"), "audio")
        self.assertEqual(
            get_file_name_without_extension("/path/to/archive.tar.gz"), "archive"
        )

    def test_is_video_file(self):
        self.assertTrue(is_video_file("video.mp4"))
        self.assertTrue(is_video_file("video.avi"))
        self.assertTrue(is_video_file("video.mov"))
        self.assertTrue(is_video_file("video.mkv"))
        self.assertTrue(is_video_file("video.wmv"))
        self.assertTrue(is_video_file("video.flv"))
        self.assertTrue(is_video_file("video.webm"))
        self.assertTrue(is_video_file("video.m4v"))

        self.assertFalse(is_video_file("image.jpg"))
        self.assertFalse(is_video_file("document.pdf"))
        self.assertFalse(is_video_file("audio.mp3"))
        self.assertFalse(is_video_file("text.txt"))

    def test_get_files_in_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_paths = [
                os.path.join(temp_dir, f"test_file_{i}.txt") for i in range(3)
            ]
            for file_path in file_paths:
                open(file_path, "w").close()

            files_found = get_files_in_directory(temp_dir)

            self.assertEqual(set(files_found), set(file_paths))

    def test_get_files_in_nonexistent_directory(self):
        non_existent_dir = "/non_exist_directory"

        with self.assertRaises(FileNotFoundError):
            get_files_in_directory(non_existent_dir)


if __name__ == "__main__":
    unittest.main()
