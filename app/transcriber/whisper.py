import os
from typing import Any, List, Tuple

import ffmpeg
from faster_whisper import WhisperModel

import app.utils as utils
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

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def _ffmpeg_input_stream(
        self,
        input_path: str,
    ) -> Any:
        try:
            input_path = input_path.strip(" ").strip('"').strip("\n").strip('"')
            return ffmpeg.input(input_path, threads=0)
        except ffmpeg.Error as e:
            logger.exception("An error occurred:", e.stderr.decode("utf-8"))
            raise RuntimeError(f"Failed to load audio: {e}")

    def _output_audio_stream(
        self,
        stream: Any,
        extracted_audio: str,
    ) -> Any:
        utils.create_directory_for_file(extracted_audio)
        return ffmpeg.output(stream, extracted_audio)

    def _run_ffmpeg(
        self,
        stream: Any,
        overwrite_output: bool = True,
    ) -> None:
        try:
            ffmpeg.run(stream, overwrite_output=overwrite_output)
        except ffmpeg.Error as e:
            logger.exception("An error occurred:", e.stderr.decode("utf-8"))
            raise

    def extract_audio(
        self,
        output_dir: str = "./",
    ) -> str:
        input_video_name: str = utils.get_file_name_without_extension(
            self.input_video_path
        )
        extracted_audio = f"{input_video_name}.wav"
        expected_audio_path = os.path.join(output_dir, extracted_audio)

        stream = self._ffmpeg_input_stream(self.input_video_path)
        stream = self._output_audio_stream(stream, expected_audio_path)

        self._run_ffmpeg(stream, True)

        return expected_audio_path

    def transcribe(
        self,
        audio: str,
        model_name: str = "small",  # large-v3 | small
        device: str = "cpu",
        compute_type: str = "int8",
        num_workers: int = 1,
        language: str = "en",
    ) -> Tuple:
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
        input_video_name: str = utils.get_file_name_without_extension(
            self.input_video_path
        )

        if not segments:
            raise ValueError("Segments list is empty.")

        subtitle_file = f"sub-{input_video_name}.{language}.srt"
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

    # def resize(self):
    #     stream = ffmpeg.input(self.input_video_path)
    #     probe = ffmpeg.probe(self.input_video_path)
    #     output_path = self.input_video_path.replace(".mp4", "_resized.mp4")

    #     video_stream = next(
    #         (stream for stream in probe["streams"] if stream["codec_type"] == "video"),
    #         None,
    #     )
    #     if video_stream is None:
    #         raise ValueError("No video stream found")

    #     width = int(video_stream["width"])
    #     height = int(video_stream["height"])

    #     if width / height > 9 / 16:
    #         new_width = width
    #         new_height = int(width * 16 / 9)
    #     else:
    #         new_height = height
    #         new_width = int(height * 9 / 16)

    #     if new_height % 2 != 0:
    #         new_height += 1
    #     if new_width % 2 != 0:
    #         new_width += 1

    #     # ! TODO : Add dynamic 9:16 aspect ration
    #     stream = ffmpeg.output(
    #         stream,
    #         output_path,
    #         vcodec="libx264",
    #         acodec="aac",
    #         video_bitrate="500k",
    #         audio_bitrate="128k",
    #         metadata="author=Ivan Kovtun",
    #     )

    #     self._run_ffmpeg(stream, True)

    #     return output_path

    def add_subtitle_to_video(
        self,
        soft_subtitle: bool,
        subtitle_file_path: str,
        subtitle_language: str,
        output_directory: str = "./",
    ):
        input_video_name: str = utils.get_file_name_without_extension(
            self.input_video_path
        )

        video_input_stream = self._ffmpeg_input_stream(self.input_video_path)
        subtitle_input_stream = self._ffmpeg_input_stream(subtitle_file_path)

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
                    "metadata:s:s:0": f"language={subtitle_language}",  # noqa: F601
                    "metadata:s:s:0": f"title={subtitle_track_title}",  # noqa: F601
                },
            )

            self._run_ffmpeg(stream, True)
        else:
            stream = ffmpeg.output(
                video_input_stream,
                output_video_path,
                vf=f"subtitles={subtitle_file_path}:force_style='FontName=Display,FontSize=14,PrimaryColour=&HFFFFFF&,Bold=1'",
            )

            self._run_ffmpeg(stream, True)
