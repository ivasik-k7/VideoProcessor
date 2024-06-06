import app.utils as utils
from app.transcriber.whisper import WhisperVideoProcessor

logger = utils.get_logger(__name__)


class VideoProcessorContext:
    def __init__(self, input_video_path: str):
        self.input_video_path = input_video_path

    def __enter__(self):
        self.wvp = WhisperVideoProcessor(self.input_video_path)
        return self.wvp

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            logger.exception(f"An exception of type {exc_type} occurred: {exc_value}")
