import os
import random
import requests
from pytube import YouTube
from moviepy.editor import VideoFileClip, concatenate_videoclips

YOUTUBE_DATA_API_KEY = "AIzaSyAJ2e9oVr-_7F-bOlZtVVx5BZxuRh1yY6c"  # Replace with your actual YouTube API key
NUM_VIDEOS = 10
MIN_VIEWS = 1000000

def get_random_videos(api_key, num_videos, min_views):
    try:
        url = f"https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "snippet",
            "chart": "mostPopular",
            "regionCode": "US",  # You can change the region code if needed
            "maxResults": 50,  # Maximum allowed by the API
            "videoCategoryId": "10",  # Music category
            "type": "video",
            "key": api_key,
        }

        response = requests.get(url, params=params)
        data = response.json()

        videos = [item["id"] for item in data.get("items", []) if int(item["statistics"]["viewCount"]) >= min_views]
        random_videos = random.sample(videos, min(num_videos, len(videos)))
        return random_videos

    except Exception as e:
        print(f"Error getting random videos: {e}")
        return []

def download_video(video_id, output_path):
    try:
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        yt = YouTube(video_url)
        stream = yt.streams.filter(file_extension="mp4", res="360p").first()
        stream.download(output_path)
        print(f"Downloaded: {yt.title}")
        return os.path.join(output_path, f"{yt.title}.mp4")
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None

def clip_video(input_path, output_path, duration=5):
    try:
        clip = VideoFileClip(input_path)
        clipped = clip.subclip(0, duration)
        clipped.write_videofile(output_path, codec="libx264", audio_codec="aac")
        print(f"Clipped and saved: {output_path}")
        clip.close()
        clipped.close()
    except Exception as e:
        print(f"Error clipping video: {e}")

def main():
    output_folder = "downloaded_videos"
    output_clips_folder = "clipped_videos"

    # Create folders if they don't exist
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(output_clips_folder, exist_ok=True)

    # Get random videos with over 1 million views
    random_videos = get_random_videos(YOUTUBE_DATA_API_KEY, NUM_VIDEOS, MIN_VIEWS)

    for video_id in random_videos:
        # Download video
        downloaded_video_path = download_video(video_id, output_folder)

        if downloaded_video_path:
            # Clip video to 5 seconds
            output_clip_path = os.path.join(output_clips_folder, f"{video_id}_clipped_video.mp4")
            clip_video(downloaded_video_path, output_clip_path, duration=5)

if __name__ == "__main__":
    main()
