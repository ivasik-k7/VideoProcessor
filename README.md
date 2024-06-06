# Automation Video Processing

<p align="center">
<img src="https://img.shields.io/badge/coverage-38%25-orange" alt="Test Coverage" />
<img src="https://img.shields.io/badge/python-3.11.3-blue" alt="Python Version" />
<img src="https://github.com/ivasik-k7/reels/actions/workflows/tests.yml/badge.svg" />
<img src="https://badgen.net/docker/pulls/ikovtun7/trans_app?icon=docker&label=pulls" alt="Docker Pulls" />
<img src="https://badgen.net/docker/size/ikovtun7/trans_app?icon=docker&label=image%20size" alt="Docker Image Size" />
</a>
<p/>

## Overview

This project is designed to extract audio from videos downloaded from multiple sources such as YouTube, transcribe the audio with start and end time subtitles, translate subtitles to different languages, and convert subtitle documents into SSML (Speech Synthesis Markup Language) for synthesizing the text and voicing it.

## Features

**Video Downloading**: Automatically download videos from YouTube.

**Audio Extraction**: Extract audio from downloaded videos.

**Transcription**: Transcribe audio to generate subtitles with start and end times.

**Translation**: Translate subtitles into different languages.

**SSML Conversion**: Convert subtitle files into SSML format for speech synthesis.

**Subtitle Integration**: Add subtitles back to the video.

## Setup

### Prerequisites

- Python 3.8 or higher
- RabbitMQ
- FFmpeg (for audio extraction and video processing)
- Poetry

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ivasik-k7/YoutubeTranscriptor.git .
   ```
2. Install dependencies and create a virtual environment using Poetry:

   ```shell
   poetry install
   ```

3. Set up RabbitMQ on your machine and ensure it is running
4. Configure the settings in `app/config/config.py` to match your environment.

## Usage

The project listens to a RabbitMQ queue for messages containing the URL of the YouTube video to process.

Upon receiving a message, it downloads the video, extracts the audio, transcribes it, generates subtitles, translates them if needed, converts the subtitles to SSML, and integrates the subtitles back into the video.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Contribution

We welcome contributions to this project! If you would like to contribute, please follow these steps:

- Fork the repository.
- Create a new branch (`git checkout -b feature-branch`).
- Make your changes.
- Commit your changes (`git commit -m 'Add some feature'`).
- Push to the branch (git push origin feature-branch).
- Create a new Pull Request.
- Please ensure your code follows the project's coding standards and includes appropriate tests.

## Contact

For any questions or inquiries, please contact Ivan Kovtun at ivan.kovtun@capgemini.com.
