import math
import os
import re

from .logger import get_logger

logger = get_logger(__name__)


def clean_file_name(title):
    """
    Clean the title to make it safe for use as a file name.

    Args:
        title (str): The title to clean.

    Returns:
        str: The cleaned file name.
    """
    # Remove special characters and replace spaces and dots with underscores
    cleaned_title = re.sub(r"[^a-zA-Z0-9\s.]", "_", title)
    # Remove consecutive underscores
    cleaned_title = re.sub(r"_+", "_", cleaned_title)
    # Remove leading and trailing underscores
    cleaned_title = cleaned_title.strip("_").replace(" ", "")
    return cleaned_title


def create_directory(directory: str) -> None:
    """
    Create a directory if it does not exist.

    Args:
        directory (str): The directory path to create.
    """
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


class DirectoryManager:
    def __init__(self, directory):
        self.directory = directory

    def __enter__(self):
        if not os.path.exists(self.directory):
            raise FileNotFoundError(f"Directory '{self.directory}' does not exist.")

        file_paths = []
        for file_name in os.listdir(self.directory):
            file_path = os.path.join(self.directory, file_name)
            if os.path.isfile(file_path):
                file_paths.append(file_path)

        return file_paths

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            logger.exception(f"An error occurred: {exc_value}")


# def get_files_in_directory(directory: str) -> list:
#     """
#     Retrieve a list of file paths within the specified directory.

#     Args:
#         directory (str): The path of the directory to search.

#     Returns:
#         list: A list containing the file paths within the directory.

#     Raises:
#         FileNotFoundError: If the specified directory does not exist.
#     """
# if not os.path.exists(directory):
#     raise FileNotFoundError(f"Directory '{directory}' does not exist.")

# file_paths = []
# for file_name in os.listdir(directory):
#     file_path = os.path.join(directory, file_name)
#     if os.path.isfile(file_path):
#         file_paths.append(file_path)

#     if not file_paths:
#         logging.warning(f"No files found in directory '{directory}'.")

#     return file_paths


def get_file_name_without_extension(file_path: str) -> str:
    """
    Extract the file name without extension from the given file path.

    Args:
        file_path (str): The path of the file.

    Returns:
        str: The file name without extension.

    Example:
        If file_path is '/path/to/file.txt', the function returns 'file'.
    """
    file_name_with_extension = os.path.basename(file_path)
    file_name_without_extension, _ = os.path.splitext(file_name_with_extension)
    return file_name_without_extension


def format_time(seconds: float) -> str:
    """
    Formats a time duration given in seconds into the HH:MM:SS,MMM format.

    Args:
        seconds (float): Time duration in seconds.

    Returns:
        str: Formatted time string in the format HH:MM:SS,MMM.
    """
    sign = "-" if seconds < 0 else ""
    seconds = abs(seconds)

    hours = math.floor(seconds / 3600)
    seconds %= 3600

    minutes = math.floor(seconds / 60)
    seconds %= 60

    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)

    formatted_time = f"{sign}{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

    return formatted_time


def create_directory_for_file(file_path: str) -> None:
    """
    Create the directory for the given file path if it does not exist.

    Args:
        file_path (str): The file path for which to create the directory.
    """
    directory = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)


def is_video_file(file_path: str) -> bool:
    """
    Check if the file at the given path is a video file.

    Args:
        file_path (str): The path to the file to check.

    Returns:
        bool: True if the file is a video file, False otherwise.
    """
    video_extensions = [".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv", ".webm", ".m4v"]
    file_extension = os.path.splitext(file_path)[1].lower()
    return file_extension in video_extensions
