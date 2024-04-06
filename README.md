# Reels Project Documentation

<p align="center">
<img src="https://img.shields.io/badge/coverage-52%25-yellow" alt="Test Coverage" />
<img src="https://img.shields.io/badge/python-3.11.3-blue" alt="Python Version" />
<img src="https://github.com/ivasik-k7/reels/actions/workflows/python_ci.yml/badge.svg" />
<p/>

This documentation outlines the functionalities and workflows of the Reels project.

## Overview

The Reels project aims to handle various tasks related to video processing, transcription, translation, and content deployment across different media platforms.

## Features

- **Video Processing:** Downloading, cropping, and processing videos from specified links.
- **Transcription:** Extracting audio from videos and transcribing them into text.
- **Translation:** Translating transcribed text into different languages.
- **Subtitles Generation:** Generating subtitles for videos based on transcribed and translated text.
- **Content Deployment:** Deploying content to various media platforms such as Instagram, TikTok, and YouTube Shorts.
- **Watermarking:** Implementing dynamic graphic watermark solutions for videos.

## Usage

1. **Verify SSL Certificate:** Ensure SSL certificate verification.
2. **Initialize Database:** Initialize and manage the SQLite database.
3. **Download Videos:** Download videos from specified links.
4. **Crop Videos:** Crop downloaded videos to desired aspect ratios.
5. **Extract Audio:** Extract audio from cropped videos.
6. **Transcribe Audio:** Transcribe audio into text using specified language models.
7. **Generate Subtitles:** Generate subtitles for videos based on transcribed text.
8. **Add Subtitles to Videos:** Add subtitles to videos with specified language settings.
9. **Content Deployment:** Deploy processed content to various media platforms.
10. **Watermarking:** Implement dynamic graphic watermarking solutions for videos.

## Dependencies

- `reels.transcript`: Handles audio extraction, transcription, translation, and subtitle generation.
- `reels.utils`: Provides utility functions for file handling, directory management, and video cropping.
- `reels.certificate`: Handles SSL certificate verification.
- `reels.butcher`: Handles video downloading from specified links.
- `reels.database`: Manages SQLite database for storing video metadata.

## Example Usage

```python
python3 main.py
```
