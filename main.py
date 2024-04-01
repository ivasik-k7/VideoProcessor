import os
import logging


import reels.transcript as trsc
import reels.utils as utils
import reels.certificate as cert
import reels.butcher as butcher

from reels.database import DatabaseManager


logging.basicConfig()
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)

# While true coroutines
# Initialize sqlite database for managing and maintaining of the sources
# Download the source of data into separated storage
# Handle the naming of the downloaded videos
# Handle batching and cropping the video into separated reels videos
# Handle the detection of the words and translations with subtitles to English, Chinese, Russian
# Implement multiple strategies for deploying the content into various media platforms as (Instagram, TikTok, YoutubeShorts)
# Implement watermark dynamic graphic solution

if __name__ == "__main__":

    # Verify SSL certificate
    cert.verify()

    pwd = os.getcwd()

    # Initialize database manager
    database = DatabaseManager("test")

    database.clean()

    database.insert_video(
        link="https://www.youtube.com/watch?v=gXs8222C3Oo",
        date="never",
    )

    downloads_directory = os.path.join(pwd, "downloads")

    content_directory = os.path.join(pwd, "content")

    # Retrieve all video links from the database
    elements = database.get_all_videos()
    links = [element["link"] for element in elements]

    # Get a list of files in the output destination directory
    utils.create_directory(downloads_directory)
    utils.create_directory(content_directory)

    # Download videos to the output destination
    butcher.download_videos(links, downloads_directory)

    downloaded_files = utils.get_files_in_directory(downloads_directory)

    for file in downloaded_files:
        filename = os.path.basename(file)
        output_path = os.path.join(content_directory, filename)
        utils.crop_video(file, output_path)

    content_files = utils.get_files_in_directory(content_directory)

    for file in content_files:
        try:

            # Set directories
            audio_output_directory = os.path.join(pwd, "audio-outputs")
            subtitles_output_directory = os.path.join(pwd, "subtitles")
            results_directory = os.path.join(pwd, "results")

            audio_filename = trsc.extract_audio(file, audio_output_directory)
            audio__file_path = os.path.join(audio_output_directory, audio_filename)

            # Set wished language
            wished_language_code: str = "pl"

            # Transcribe the audio
            language, segments = trsc.transcribe(
                audio=audio__file_path,
                model_name="large-v3",
                language=wished_language_code,
            )

            # Generate subtitles
            subtitle_file_path = trsc.generate_subtitle_file(
                language=language,
                segments=segments,
                input_video_path=file,
                output_dir=subtitles_output_directory,
            )

            trsc.add_subtitle_to_video(
                soft_subtitle=False,
                input_video_path=file,
                output_directory=results_directory,
                subtitle_file_path=subtitle_file_path,
                subtitle_language=language,
            )

            # Remove the processed files
            os.remove(audio__file_path)
            os.remove(subtitle_file_path)
        except Exception as e:
            print(e)
