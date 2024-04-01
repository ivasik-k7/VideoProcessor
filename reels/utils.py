import os
import math
import logging
import re

from moviepy.editor import VideoFileClip


def crop_video(input_path, output_path, target_ratio=(9, 16)):
    """
    Crop a video to a specific aspect ratio.

    Parameters:
        input_path (str): The path to the input video file.
        output_path (str): The path where the cropped video will be saved.
        target_ratio (tuple): The target aspect ratio as a tuple of (width, height).
                              Default is (9, 16) for a 9:16 aspect ratio.

    Returns:
        None
    """
    try:
        # Load the video clip
        clip = VideoFileClip(input_path)

        # Calculate the dimensions for cropping
        width, height = clip.size
        target_width = min(width, int(height * (target_ratio[0] / target_ratio[1])))
        target_height = min(height, int(width * (target_ratio[1] / target_ratio[0])))

        # Calculate the cropping box
        x1 = (width - target_width) / 2
        y1 = (height - target_height) / 2
        x2 = x1 + target_width
        y2 = y1 + target_height

        # Crop the video clip
        cropped_clip = clip.crop(x1=x1, y1=y1, x2=x2, y2=y2)

        # Write the cropped clip to a new file with H.264 codec and .mp4 format
        cropped_clip.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            fps=clip.fps,
        )

        print("Cropping successful")
    except Exception as e:
        print("Error during cropping:", e)


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


def get_files_in_directory(directory: str) -> list:
    """
    Retrieve a list of file paths within the specified directory.

    Args:
        directory (str): The path of the directory to search.

    Returns:
        list: A list containing the file paths within the directory.

    Raises:
        FileNotFoundError: If the specified directory does not exist.
    """
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory '{directory}' does not exist.")

    file_paths = []
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            file_paths.append(file_path)

    if not file_paths:
        logging.warning(f"No files found in directory '{directory}'.")

    return file_paths


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
    file_name_without_extension = os.path.splitext(file_name_with_extension)[0]
    return file_name_without_extension


def format_time(seconds: float) -> str:
    """
    Formats a time duration given in seconds into the HH:MM:SS,MMM format.

    Args:
        seconds (float): Time duration in seconds.

    Returns:
        str: Formatted time string in the format HH:MM:SS,MMM.
    """
    hours = math.floor(seconds / 3600)
    seconds %= 3600

    minutes = math.floor(seconds / 60)
    seconds %= 60

    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)

    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

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
