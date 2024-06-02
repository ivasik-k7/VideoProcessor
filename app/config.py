import os


class Config:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

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


config = Config()
