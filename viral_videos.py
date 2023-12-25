import os
import requests
from pytube import YouTube
from moviepy.editor import VideoFileClip, TextClip, concatenate_videoclips, CompositeVideoClip

def find_viral_videos(api_key):
    # (unchanged)

def download_clip(video_url, output_path):
    # (unchanged)

def clip_video(video_path, output_path):
    # (unchanged)

def clip_videos(viral_videos, output_path):
    # (unchanged)

def load_video_clip(video_path):
    try:
        return VideoFileClip(video_path)
    except Exception as e:
        print(f"Error loading video: {e}")
        return None

def process_video(video_path):
    clip = load_video_clip(video_path)
    if clip:
        duration = clip.duration
        print(f"Video: {video_path}, Duration: {duration} seconds")
        clip.close()
    else:
        print(f"Skipping {video_path} due to error loading video.")

def process_videos_in_folder(folder_path):
    video_files = [f for f in os.listdir(folder_path) if f.endswith(".mp4")]
    for video_file in video_files:
        video_path = os.path.join(folder_path, video_file)
        process_video(video_path)

def make_tiktok_video(viral_videos, output_path):
    clips = []
    for video in viral_videos:
        video_id = video['id']
        clip_path = os.path.join(output_path, f"{video_id}_clip.mp4")

        if os.path.exists(clip_path):
            clips.append(VideoFileClip(clip_path))

    try:
        concatenated_clip = concatenate_videoclips(clips, method="compose")

        text = TextClip("This is a TikTok video made by an AI!", fontsize=24, color='white', bg_color='black')
        text = text.set_pos('center')
        text = text.set_duration(concatenated_clip.duration)
        final_video = CompositeVideoClip([concatenated_clip, text])

        final_video_path = os.path.join(output_path, "tiktok_video.mp4")
        final_video.write_videofile(final_video_path)

        concatenated_clip.close()
        final_video.close()

        print(f"Processed TikTok Video Path: {final_video_path}")

    except Exception as e:
        print(f"Error making TikTok video: {e}")

def main():
    api_key = "AIzaSyAJ2e9oVr-_7F-bOlZtVVx5BZxuRh1yY6c"  # Replace with your actual YouTube API key
    output_path = "viral_videos"

    viral_videos = find_viral_videos(api_key)
    clip_videos(viral_videos, output_path)
    process_videos_in_folder(output_path)
    make_tiktok_video(viral_videos, output_path)

if __name__ == "__main__":
    main()
