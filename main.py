import app.utils as utils
from app.butcher.youtube import YoutubeButcher  # noqa
from app.config import config
from app.synthesizer.ssml import SSMLConverter
from app.transcriber.video_processor import VideoProcessorContext

if __name__ == "__main__":
    utils.create_directory(config.downloads_directory)
    utils.create_directory(config.results_directory)
    utils.create_directory(config.subtitles_directory)
    utils.create_directory(config.audio_directory)
    utils.create_directory(config.ssml_directory)

    YoutubeButcher.download_source(
        source="https://www.youtube.com/watch?v=MGJ1of3gw0k",
        output_path=config.downloads_directory,
    )

    with utils.DirectoryManager(config.downloads_directory) as files:
        for file in files:
            with VideoProcessorContext(file) as processor:
                audio_filename = processor.extract_audio(config.audio_directory)

                language, segments = processor.transcribe(
                    audio=audio_filename,
                    model_name="large-v3",
                    language=config.localization,
                )

                subtitle_file_path = processor.generate_subtitle_file(
                    language, segments, config.subtitles_directory
                )

                ssml_filename = utils.get_file_name_without_extension(file)

                SSMLConverter(
                    srt_file=subtitle_file_path,
                    output_file=config.ssml_directory + f"/{ssml_filename}.txt",
                    voice_name="en-US-DavisNeural",
                ).convert()

                # TODO: Include ssml synthesizing into the including completed audio to video

                processor.add_subtitle_to_video(
                    embedded_subtitles=True,
                    subtitle_file_path=subtitle_file_path,
                    subtitle_language=language,
                    output_directory=config.results_directory,
                )
