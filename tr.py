import os
from reels.utils import get_files_in_directory
from reels.translator import translate_file, detect_language
from reels.butcher import download_video
from reels.certificate import verify

if __name__ == "__main__":
    verify()

    PWD = os.getcwd()

    subtitles_directory = os.path.join(PWD, "subtitles")
    outputs_directory = os.path.join(PWD, "outputs")

    subtitles = get_files_in_directory(subtitles_directory)

    link = "https://www.youtube.com/watch?v=K3aTpytFqFI"

    download_video(link, outputs_directory)
