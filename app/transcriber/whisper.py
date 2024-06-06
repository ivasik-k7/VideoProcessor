import os
from typing import List, Tuple

from faster_whisper import WhisperModel

import app.utils as utils
from app.ffmpeg_utils import FFmpegProcessor
from app.logger import get_logger

logger = get_logger(__name__)


class WhisperVideoProcessor:
    def __init__(
        self,
        input_video_path: str,
    ):
        if not os.path.exists(input_video_path):
            raise FileNotFoundError(
                f"Input video file '{self.input_video_path}' does not exist."
            )

        if not utils.is_video_file(input_video_path):
            raise ValueError(
                f"The provided file '{self.input_video_path}' is not a video file."
            )

        self.input_video_path = input_video_path
        self.ffmpeg_processor = FFmpegProcessor()

    @property
    def input_filename(self) -> str:
        """Get the filename of the input video file without the extension.

        Returns:
            str: The filename of the input video file without the extension.
        """
        return utils.get_file_name_without_extension(self.input_video_path)

    def extract_audio(
        self,
        output_dir: str = "./",
    ) -> str:
        """Extract the audio from the input video and save it as a WAV file.

        Args:
            output_dir (str, optional): The directory where the extracted audio file will be saved.
                Defaults to "./".

        Returns:
            str: The path to the extracted audio file.
        """
        expected_audio_path = os.path.join(output_dir, f"{self.input_filename}.wav")

        utils.create_directory_for_file(expected_audio_path)

        stream = self.ffmpeg_processor.input(self.input_video_path)
        stream = self.ffmpeg_processor.output(stream, expected_audio_path)

        self.ffmpeg_processor.run(stream)

        return expected_audio_path

    def transcribe(
        self,
        audio: str,
        model_name: str = "small",
        device: str = "cpu",
        compute_type: str = "int8",
        num_workers: int = 1,
        language: str = "en",
    ) -> Tuple[str, dict]:
        """
        Transcribe the audio file using the Whisper model.

        Args:
            audio (str): The path to the audio file to transcribe.
            model_name (str, optional): The name of the Whisper model to use. Defaults to "small". Better choose from "large-v3" or "small"
            device (str, optional): The device to use for inference. Choose from "cpu" or "cuda".
                Defaults to "cpu".
            compute_type (str, optional): The precision type for computation. Choose from "int8", "fp16",
                or "fp32". Defaults to "int8".
            num_workers (int, optional): The number of workers to use for transcription. Defaults to 1.
            language (str, optional): The language code for transcription. Defaults to "en" (English).

        Returns:
            Tuple[str, dict]: A tuple containing the detected language and the transcription segments.
                The first element is a string representing the detected language code.
                The second element is a dictionary containing the transcription segments
                with word timestamps.
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

    def generate_subtitle_file(
        self,
        language: str,
        segments: List,
        output_dir: str = "./",
    ) -> str:
        """Generate a subtitle file from transcription segments.

        Args:
            language (str): The language of the subtitles.
            segments (List): A list of transcription segments.
            output_dir (str, optional): The directory where the subtitle file will be saved. Defaults to "./".

        Returns:
            str: The path to the generated subtitle file.

        Raises:
            ValueError: If the segments list is empty.
        """
        if not segments:
            raise ValueError("Segments list is empty.")

        subtitle_file = f"sub-{self.input_filename}.{language}.srt"
        subtitle_path = os.path.join(output_dir, subtitle_file)

        utils.create_directory_for_file(subtitle_path)

        with open(subtitle_path, "w", encoding="utf-8") as file:
            for index, segment in enumerate(segments, start=1):
                start = utils.format_time(segment.start)
                end = utils.format_time(segment.end)
                text = segment.text.strip()
                file.write(f"{index}\n")
                file.write(f"{start} --> {end}\n")
                file.write(f"{text}\n\n")

        return subtitle_path

    def add_subtitle_to_video(
        self,
        embedded_subtitles: bool,
        subtitle_file_path: str,
        subtitle_language: str,
        output_directory: str = "./",
    ):
        """Add subtitles to the input video and save the result to an output file.

        Args:
            embedded_subtitles (bool): Whether the subtitles should be embedded directly into the video.
                If True, the subtitles will be burned into the video. If False, the subtitles will be
                added as a separate stream.
            subtitle_file_path (str): The path to the subtitle file.
            subtitle_language (str): The language of the subtitles.
            output_directory (str, optional): The directory where the output video will be saved.
                Defaults to "./".

        Raises:
            ValueError: If embedded_subtitles is True but the subtitle file path is invalid.
            FileNotFoundError: If the input video file or subtitle file does not exist.
            subprocess.CalledProcessError: If the FFmpeg command fails.

        Note:
            - If embedded_subtitles is True, the subtitles will be burned into the video using
            the specified font and style.
            - If embedded_subtitles is False, the subtitles will be added as a separate stream
            to the output video file.

        Returns:
            None
        """
        output_video_path = os.path.join(output_directory, f"{self.input_filename}.mp4")
        utils.create_directory_for_file(output_video_path)

        video_stream = self.ffmpeg_processor.input(self.input_video_path)
        subtitle_stream = self.ffmpeg_processor.input(subtitle_file_path)

        subtitle_track_title = utils.get_file_name_without_extension(subtitle_file_path)

        if embedded_subtitles:
            stream = self.ffmpeg_processor.output(
                video_stream,
                output_video_path,
                **{
                    "vf": f"subtitles={subtitle_file_path}:force_style='FontName=Display,FontSize=14,PrimaryColour=&HFFFFFF&,Bold=1'"
                },
                # vf=f"subtitles={subtitle_file_path}:force_style='FontName=Display,FontSize=14,PrimaryColour=&HFFFFFF&,Bold=1'"},
            )
        else:
            stream = self.ffmpeg_processor.output(
                video_stream,
                subtitle_stream,
                output_video_path,
                **{"c": "copy", "c:s": "mov_text"},
                **{
                    "metadata:s:s:0": f"language={subtitle_language}",  # noqa: F601
                    "metadata:s:s:0": f"title={subtitle_track_title}",  # noqa: F601
                },
            )

        self.ffmpeg_processor.run(stream, overwrite_output=True)
