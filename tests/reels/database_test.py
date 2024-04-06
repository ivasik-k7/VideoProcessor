import unittest
from reels.database import DatabaseManager

TEST_DB_NAME = "test_database.db"


class TestDatabaseManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_manager = DatabaseManager(TEST_DB_NAME)

    def setUp(self):
        self.db_manager.clean()

    def tearDown(self):
        self.db_manager.clean()

    @classmethod
    def tearDownClass(cls):
        cls.db_manager.close_connection()

    def test_insert_video(self):
        self.db_manager.insert_video("video_link", "2024-04-07")
        videos = self.db_manager.get_all_videos()
        self.assertEqual(len(videos), 1)

    def test_get_all_videos(self):
        self.db_manager.insert_video("video_link1", "2024-04-07")
        self.db_manager.insert_video("video_link2", "2024-04-08")
        videos = self.db_manager.get_all_videos()
        self.assertEqual(len(videos), 2)

    def test_get_video_by_id(self):
        self.db_manager.insert_video("video_link", "2024-04-07")
        video_id = self.db_manager.get_all_videos()[0]["id"]
        video = self.db_manager.get_video_by_id(video_id)
        self.assertEqual(video["link"], "video_link")

    def test_delete_video(self):
        self.db_manager.insert_video("video_link", "2024-04-07")
        video_id = self.db_manager.get_all_videos()[0]["id"]
        self.db_manager.delete_video(video_id)
        videos = self.db_manager.get_all_videos()
        self.assertEqual(len(videos), 0)


if __name__ == "__main__":
    unittest.main()
