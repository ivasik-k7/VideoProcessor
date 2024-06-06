from typing import Any

import ffmpeg

from app.utils import get_logger

logger = get_logger(__name__)


class FFmpegProcessor:
    def run(
        self,
        stream_spec: Any,
        overwrite_output: bool = False,
    ) -> tuple[bytes, bytes]:
        """
        Run a given FFmpeg stream specific command.
        """
        try:
            return ffmpeg.run(
                stream_spec,
                overwrite_output=overwrite_output,
                capture_stdout=True,
                capture_stderr=True,
            )
        except ffmpeg.Error as e:
            logger.exception("An ffmpeg error occurred: %s", e.stderr.decode("utf-8"))
            raise RuntimeError(f"Failed to execute FFmpeg command: {e}")

    def input(
        self,
        file_path: str,
        **kwargs,
    ) -> Any:
        """
        Create an FFmpeg input stream.

        Args:
            file_path (str): The path to the input file.
            **kwargs: Additional keyword arguments to customize the FFmpeg input stream.

        Any supplied kwargs are passed to ffmpeg verbatim (e.g. ``t=20``,
        ``f='mp4'``, ``acodec='pcm'``, etc.).

        Returns:
            Any: An FFmpeg input stream object.

        Raises:
            RuntimeError: If an error occurs while creating the FFmpeg input stream.

        Example:
            To create an FFmpeg input stream with custom options:
            >>> input_stream = self.ffmpeg_input(file_path, threads=4)
        """
        try:
            file_path = file_path.strip(" ").strip('"').strip("\n").strip('"')
            return ffmpeg.input(file_path, **kwargs)
        except ffmpeg.Error as e:
            logger.exception("An ffmpeg error occurred: %s", e.stderr.decode("utf-8"))
            raise RuntimeError(f"Failed to load audio: {e}")

    def output(
        self,
        *streams_and_filename: Any,
        **kwargs: Any,
    ) -> Any:
        """Create an FFmpeg output stream.

        Args:
            *streams_and_filename (Any): FFmpeg input streams and the output filename.
            **kwargs (Any): Additional keyword arguments to customize the FFmpeg output stream.

        Returns:
            Any: An FFmpeg output stream object.

        Raises:
            RuntimeError: If an error occurs while creating the FFmpeg output stream.

        Example:
            To create an FFmpeg output stream with custom options:
            >>> output_stream = self.ffmpeg_output(stream1, stream2, 'output_file.mp4', c='copy', c:s='mov_text', metadata:s:s:0='language=en', metadata:s:s:0='title=subtitle_track_title')
        """
        try:
            return ffmpeg.output(
                *streams_and_filename,
                **kwargs,
            )
        except ffmpeg.Error as e:
            logger.exception("An ffmpeg error occurred: %s", e.stderr.decode("utf-8"))
            raise RuntimeError(f"Failed to create FFmpeg output stream: {e}")
