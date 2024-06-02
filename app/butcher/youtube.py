from pytube import YouTube
from unidecode import unidecode

from app.logger import get_logger
from app.utils import clean_file_name

logger = get_logger(__name__)


class YoutubeButcher:
    @staticmethod
    def download_source(
        output_path: str,
        source: str,
    ) -> None:
        try:
            provider = YouTube(
                source,
                use_oauth=True,
                allow_oauth_cache=True,
            )

            obj = (
                provider.streams.filter(progressive=True, file_extension="mp4")
                .order_by("resolution")
                .desc()
                .first()
            )

            if not obj:
                logger.warn("Not downloadable object!")
                return

            title = clean_file_name(unidecode(obj.title))
            filename = f"{title}.mp4"
            obj.download(output_path=output_path, filename=filename)

            logger.info(f"The element {filename} from {source} has been downloaded!")

        except Exception as e:
            logger.exception(f"There is an error occurred: {e}")
