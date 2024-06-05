import asyncio
import os
import sys

import app.utils as utils
from app.butcher.youtube import YoutubeButcher
from app.config import config
from app.rabbitmq import RabbitMQContext
from app.synthesizer.ssml import SSMLConverter
from app.transcriber.whisper import WhisperVideoProcessor

logger = utils.get_logger(__name__)


def manage_event(body):
    source = body.decode("utf-8")

    YoutubeButcher.download_source(
        source=source,
        output_path=config.downloads_directory,
    )

    with utils.DirectoryManager(config.downloads_directory) as files:
        for file in files:
            with WhisperVideoProcessor(file) as processor:
                ssml_filename = utils.get_file_name_without_extension(file)

                audio_file_path = processor.extract_audio(config.audio_directory)

                language, segments = processor.transcribe(
                    audio=audio_file_path,
                    model_name="large-v3",
                    language=config.localization,
                )

                subtitle_file_path = processor.generate_subtitle_file(
                    language,
                    segments,
                    config.subtitles_directory,
                )

                SSMLConverter(
                    srt_file=subtitle_file_path,
                    output_file=config.ssml_directory + f"/{ssml_filename}.txt",
                    voice_name="en-US-DavisNeural",
                ).convert()

                processor.add_subtitle_to_video(
                    soft_subtitle=False,
                    subtitle_file_path=subtitle_file_path,
                    subtitle_language=language,
                    output_directory=config.results_directory,
                )

                utils.delete_file(subtitle_file_path)
                utils.delete_file(audio_file_path)
                utils.delete_file(file)


async def main():
    with RabbitMQContext() as rabbit:
        while True:
            rabbit.consume_message(manage_event)


if __name__ == "__main__":
    try:
        utils.create_directory(config.downloads_directory)
        utils.create_directory(config.results_directory)
        utils.create_directory(config.subtitles_directory)
        utils.create_directory(config.audio_directory)
        utils.create_directory(config.ssml_directory)

        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
