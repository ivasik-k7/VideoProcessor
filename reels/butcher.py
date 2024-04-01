import os
from pytube import YouTube
from unidecode import unidecode
from reels.utils import clean_file_name


def download_video(url, output_folder):
    try:
        yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
        video = (
            yt.streams.filter(progressive=True, file_extension="mp4")
            .order_by("resolution")
            .desc()
            .first()
        )

        if video:
            video_title = clean_file_name(unidecode(yt.title))
            video.download(output_path=output_folder, filename=f"{video_title}.mp4")
            print(f"Downloaded: {yt.title}")
        else:
            print(f"No downloadable video found for {url}")
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")


def download_videos(urls, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for url in urls:
        if "youtube.com" in url or "youtu.be" in url:
            download_video(url, output_folder)
        else:
            print(f"Not a YouTube link: {url}")
