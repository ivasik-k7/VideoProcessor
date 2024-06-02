# Reels Project Documentation

<p align="center">
<img src="https://img.shields.io/badge/coverage-38%25-orange" alt="Test Coverage" />
<img src="https://img.shields.io/badge/python-3.11.3-blue" alt="Python Version" />
<img src="https://github.com/ivasik-k7/reels/actions/workflows/tests.yml/badge.svg" />
<img src="https://badgen.net/docker/pulls/ikovtun7/trans_app?icon=docker&label=pulls" alt="Docker Pulls" />
<img src="https://badgen.net/docker/size/ikovtun7/trans_app?icon=docker&label=image%20size" alt="Docker Image Size" />
</a>
<p/>

This documentation outlines the functionalities and workflows of the project.

## Overview

This repository provides a tool for generating subtitles with various localizations for video files. It utilizes several components to achieve this, including:

- **YouTube Downloader**: The `YoutubeButcher` module allows downloading videos from YouTube.
- **Video Processing**: The `WhisperVideoProcessor` module handles video processing tasks such as extracting audio, transcribing speech, and adding subtitles.
- **Localization Support**: Subtitles can be generated in different languages by specifying the desired locale.

## Setup

To set up the project, follow these steps:

1. Install the required dependencies listed in `pyproject.toml` using poetry:

   ```shell
   pip install
   ```

2. Make sure to configure the paths in the `config.py` file according to your system's directory structure.

## Usage

To use the tool, follow these steps:

1. Place the video files you want to process in the `downloads_directory`.
2. Run the script `main.py`.
3. The script will process each video file found in the `downloads_directory`:

- Extract audio from the video.
- Transcribe the speech in the video to text.
- Generate subtitles in the specified language.
- Add subtitles to the video.

4. The processed videos with subtitles will be saved in the `results_directory`.

## Localization

To generate subtitles in different languages, set the desired locale in the `main.py` script. For example, to generate subtitles in Ukrainian, set `locale = "uk"`.

## License

This project is licensed under the [MIT License](LICENSE).
