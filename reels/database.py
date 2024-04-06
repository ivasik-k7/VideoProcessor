import sqlite3
from typing import List, Dict

ERROR_MESSAGE: str = "Error:"


class DatabaseManager:
    def __init__(self, db_name: str) -> None:
        self.conn: sqlite3.Connection = sqlite3.connect(db_name)
        self.cursor: sqlite3.Cursor = self.conn.cursor()
        self.create_table()

    def create_table(self) -> None:
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS videos
                               (id INTEGER PRIMARY KEY, link TEXT UNIQUE, date TEXT)"""
        )
        self.conn.commit()

    def insert_video(self, link: str, date: str) -> None:
        try:
            self.cursor.execute("SELECT link FROM videos WHERE link=?", (link,))
            existing_link = self.cursor.fetchone()
            if existing_link:
                print("Video with link", link, "already exists.")
            else:
                self.cursor.execute(
                    "INSERT INTO videos (link, date) VALUES (?, ?)", (link, date)
                )
                self.conn.commit()
                print("Video with link", link, "inserted successfully.")
        except Exception as e:
            print(ERROR_MESSAGE, str(e))
            self.conn.rollback()

    def get_all_videos(self) -> List[Dict[str, str]]:
        self.cursor.execute("SELECT * FROM videos")
        rows = self.cursor.fetchall()
        return [{"id": row[0], "link": row[1], "date": row[2]} for row in rows]

    def get_video_by_id(self, video_id: int) -> Dict[str, str]:
        self.cursor.execute("SELECT * FROM videos WHERE id=?", (video_id,))
        row = self.cursor.fetchone()
        return {"id": row[0], "link": row[1], "date": row[2]} if row else {}

    def delete_video(self, video_id: int) -> None:
        try:
            self.cursor.execute("DELETE FROM videos WHERE id=?", (video_id,))
            self.conn.commit()
        except Exception as e:
            print(ERROR_MESSAGE, str(e))
            self.conn.rollback()

    def clean(self):
        try:
            self.cursor.execute("DELETE FROM videos")
            self.conn.commit()
            print("Database cleaned successfully.")
        except Exception as e:
            print("Error:", str(e))
            self.conn.rollback()

    def close_connection(self) -> None:
        self.conn.close()
