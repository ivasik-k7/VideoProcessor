import os
import ffmpeg
import subprocess


import reels.utils as utils

from typing import Any, Tuple, List
from faster_whisper import WhisperModel


def ffmpeg_input_stream(input_path: str) -> Any:
    """
    Creates an input stream from the given video file.

    Args:
        input_path (str): Path to the input  file.

    Returns:
        Any: Input stream object.
    """
    return ffmpeg.input(input_path)


def output_audio_stream(stream: Any, extracted_audio: str) -> Any:
    """
    Creates an output stream for audio extraction.

    Args:
        stream (Any): Input stream object.
        extracted_audio (str): Path to save the extracted audio file.

    Returns:
        Any: Output stream object.
    """
    utils.create_directory_for_file(extracted_audio)

    return ffmpeg.output(stream, extracted_audio)


import ffmpeg


def run_ffmpeg(stream: Any, overwrite_output: bool = True) -> None:
    """
    Runs the FFmpeg process with the given stream.

    Args:
        stream (Any): FFmpeg stream object.
        overwrite_output (bool, optional): Whether to overwrite existing output files.
            Defaults to True.
    """
    ffmpeg.run(stream, overwrite_output=overwrite_output)


def add_subtitle_to_video(
    soft_subtitle: bool,
    subtitle_file_path: str,
    input_video_path: str,
    subtitle_language: str,
    output_directory: str = "./",
):
    input_video_name: str = utils.get_file_name_without_extension(input_video_path)

    video_input_stream = ffmpeg_input_stream(input_video_path)
    subtitle_input_stream = ffmpeg_input_stream(subtitle_file_path)

    output_video_name = f"{input_video_name}.mp4"
    output_video_path = os.path.join(output_directory, output_video_name)

    utils.create_directory_for_file(output_video_path)

    subtitle_track_title = os.path.basename(subtitle_file_path).replace(".srt", "")

    if soft_subtitle:
        stream = ffmpeg.output(
            video_input_stream,
            subtitle_input_stream,
            output_video_path,
            **{"c": "copy", "c:s": "mov_text"},
            **{
                "metadata:s:s:0": f"language={subtitle_language}",
                "metadata:s:s:0": f"title={subtitle_track_title}",
            },
        )

        run_ffmpeg(stream, True)
    else:
        stream = ffmpeg.output(
            video_input_stream,
            output_video_path,
            vf=f"subtitles={subtitle_file_path}",
        )

        run_ffmpeg(stream, True)


def transcribe(
    audio: str,
    model_name: str = "small",  # large-v3 | small
    device: str = "cpu",
    compute_type: str = "int8",
    num_workers: int = 1,
    language: str = "en",
) -> Tuple:
    """
    Transcribe audio using Whisper model and print results.

    Args:
        audio (str): Path to the audio file for transcription.
        model_name (str, optional): Name of the Whisper model to use for transcription.
            Defaults to "small".
        device (str, optional): Device to use for transcription (e.g., "cpu" or "cuda").
            Defaults to "cpu".
        compute_type (str, optional): Type of computation to perform (e.g., "int8" or "float32").
            Defaults to "int8".
        num_workers (int, optional): Number of workers for parallel processing.
            Defaults to 1.

    Returns:
        Tuple[str, List[Segment]]: A tuple containing the transcription language and a list of
        transcription segments.
            - language (str): Transcription language.
            - segments (List[Segment]): List of transcription segments.
    """
    model = WhisperModel(
        model_name,
        compute_type=compute_type,
        device=device,
        num_workers=num_workers,
    )

    segments, info = model.transcribe(
        audio,
        vad_filter=True,
        language=language,
        beam_size=5,
        condition_on_previous_text=False,
        word_timestamps=True,
    )

    language = info[0]
    return language, segments


def extract_audio(input_video_path: str, output_dir: str = "./") -> str:
    """
    Extracts audio from a video file.

    Args:
        input_video (str): The path to the input video file.
        output_dir (str, optional): The directory where the extracted audio will be saved.
            Defaults to "./" (current directory).

    Returns:
        str: The name of the extracted audio file.

    Raises:
        FileNotFoundError: If the input video file does not exist.
    """

    if not os.path.exists(input_video_path):
        raise FileNotFoundError(
            f"Input video file '{input_video_path}' does not exist."
        )

    if not utils.is_video_file(input_video_path):
        raise ValueError(f"The provided file '{input_video_path}' is not a video file.")

    input_video_name: str = utils.get_file_name_without_extension(input_video_path)
    extracted_audio = f"{input_video_name}.wav"
    expected_audio_path = os.path.join(output_dir, extracted_audio)

    stream = ffmpeg_input_stream(input_video_path)
    stream = output_audio_stream(stream, expected_audio_path)

    run_ffmpeg(stream, True)

    return extracted_audio


def generate_subtitle_file(
    language: str,
    segments: List,
    input_video_path: str,
    output_dir: str = "./",
) -> str:
    """
    Generate a subtitle file in SRT format.

    Args:
        language (str): Language of the transcription.
        segments (List[Segment]): List of transcription segments.
        input_video (str): Path of the input video file.

    Returns:
        str: Name of the generated subtitle file.

    Raises:
        ValueError: If segments list is empty.
    """
    input_video_name: str = utils.get_file_name_without_extension(input_video_path)

    if not segments:
        raise ValueError("Segments list is empty.")

    subtitle_file = f"sub-{input_video_name}.{language}.srt"
    subtitle_path = os.path.join(output_dir, subtitle_file)

    utils.create_directory_for_file(subtitle_path)

    text = ""
    for index, segment in enumerate(segments):
        segment_start = utils.format_time(segment.start)
        segment_end = utils.format_time(segment.end)
        text += f"{str(index+1)} \n"
        text += f"{segment_start} --> {segment_end} \n"
        text += f"{segment.text} \n"
        text += "\n"

    with open(subtitle_path, "w") as f:
        f.write(text)

    return subtitle_path
