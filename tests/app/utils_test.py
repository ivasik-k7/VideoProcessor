import os
import tempfile
import unittest

from app.utils import (
    DirectoryManager,
    clean_file_name,
    create_directory,
    create_directory_for_file,
    format_time,
    get_file_name_without_extension,
    is_video_file,
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
            get_file_name_without_extension("/path/to/archive.tar.gz"), "archive.tar"
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


class TestDirectoryManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()

        self.files = []
        for i in range(5):
            file_path = os.path.join(self.test_dir.name, f"file_{i}.txt")
            with open(file_path, "w") as f:
                f.write("Test content")
            self.files.append(file_path)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_directory_exists(self):
        with DirectoryManager(self.test_dir.name) as file_paths:
            self.assertEqual(sorted(file_paths), sorted(self.files))

    def test_directory_does_not_exist(self):
        with self.assertRaises(FileNotFoundError):
            with DirectoryManager("non_existent_directory"):
                pass

    def test_empty_directory(self):
        empty_dir = tempfile.TemporaryDirectory()
        with DirectoryManager(empty_dir.name) as file_paths:
            self.assertEqual(file_paths, [])
        empty_dir.cleanup()

    def test_directory_with_mixed_content(self):
        sub_dir = os.path.join(self.test_dir.name, "sub_dir")
        os.mkdir(sub_dir)

        with DirectoryManager(self.test_dir.name) as file_paths:
            self.assertEqual(sorted(file_paths), sorted(self.files))


if __name__ == "__main__":
    unittest.main()
