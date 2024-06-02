import app.utils as utils
from app.butcher.youtube import YoutubeButcher  # noqa
from app.config import config
from app.transcriber.whisper import WhisperVideoProcessor

if __name__ == "__main__":
    utils.create_directory(config.downloads_directory)
    utils.create_directory(config.results_directory)
    utils.create_directory(config.subtitles_directory)
    utils.create_directory(config.audio_directory)

    with utils.DirectoryManager(config.downloads_directory) as files:
        for file in files:
            with WhisperVideoProcessor(file) as processor:
                audio_filename = processor.extract_audio(config.audio_directory)

                language, segments = processor.transcribe(
                    audio=audio_filename,
                    model_name="large-v3",
                    language=config.localization,
                )

                subtitle_file_path = processor.generate_subtitle_file(
                    language, segments, config.subtitles_directory
                )

                processor.add_subtitle_to_video(
                    soft_subtitle=False,
                    subtitle_file_path=subtitle_file_path,
                    subtitle_language=language,
                    output_directory=config.results_directory,
                )
