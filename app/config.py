import os


class Config:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    localization: str = os.environ.get("LOCALE", "uk")

    results_directory = os.environ.get(
        "RESULTS_DIR",
        os.path.join(project_root, "results"),
    )
    subtitles_directory = os.environ.get(
        "SUBTITLES_DIR",
        os.path.join(project_root, "subtitles"),
    )
    audio_directory = os.environ.get(
        "AUDIO_DIR",
        os.path.join(project_root, "audio"),
    )
    downloads_directory = os.environ.get(
        "DOWNLOADS_DIR",
        os.path.join(project_root, "downloads"),
    )


class DatabaseConfig:
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "sqlite:///database.db")
    DATABASE_NAME: str = os.environ.get("DATABASE_NAME", "primary")
    DATABASE_USER: str = os.environ.get("DATABASE_USER", "admin")
    DATABASE_PASSWORD: str = os.environ.get("DATABASE_USER", "password")


config = Config()
database_config = DatabaseConfig()
