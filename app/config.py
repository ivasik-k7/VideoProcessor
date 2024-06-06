import os


class Config:
    def __init__(self):
        self._project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )

    @property
    def project_root(self) -> str:
        return self._project_root

    @property
    def localization(self) -> str:
        """
        Apply localization to subtitles
        """
        return os.environ.get("LOCALE", "pl")

    @property
    def results_directory(self) -> str:
        default = os.path.join(self.project_root, "out/results")
        return os.environ.get("RESULTS_DIR", default)

    @property
    def subtitles_directory(self) -> str:
        default = os.path.join(self.project_root, "out/subtitles")
        return os.environ.get("SUBTITLES_DIR", default)

    @property
    def audio_directory(self) -> str:
        default = os.path.join(self.project_root, "out/audio")
        return os.environ.get("AUDIO_DIR", default)

    @property
    def downloads_directory(self) -> str:
        default = os.path.join(self.project_root, "out/downloads")
        return os.environ.get("DOWNLOADS_DIR", default)

    @property
    def ssml_directory(self) -> str:
        default = os.path.join(self.project_root, "out/ssml")
        return os.environ.get("SSML_DIR", default)


class DatabaseConfig:
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "sqlite:///database.db")
    DATABASE_NAME: str = os.environ.get("DATABASE_NAME", "primary")
    DATABASE_USER: str = os.environ.get("DATABASE_USER", "admin")
    DATABASE_PASSWORD: str = os.environ.get("DATABASE_USER", "password")


class RabbitMQConfig:
    HOST = os.environ.get("RABBITMQ_HOST", "localhost")
    PORT = os.environ.get("RABBITMQ_PORT", "5672")
    USERNAME = os.environ.get("RABBITMQ_USERNAME", "admin")
    PASSWORD = os.environ.get("RABBIT_MQ_PASSWORD", "secret")


config = Config()
database_config = DatabaseConfig()
rabbitmq_config = RabbitMQConfig()
