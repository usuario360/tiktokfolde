import os
from pytube import YouTube
from moviepy.editor import VideoFileClip, concatenate_videoclips

def download_video(video_url, output_path):
    try:
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
    video_url = "https://youtu.be/QdBZY2fkU-0?si=k-AhLFNf6imtERlf"  # Replace with the actual YouTube video URL
    output_folder = "downloaded_videos"
    output_clips_folder = "clipped_videos"

    # Create folders if they don't exist
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(output_clips_folder, exist_ok=True)

    # Download video
    downloaded_video_path = download_video(video_url, output_folder)

    if downloaded_video_path:
        # Clip video to 5 seconds
        output_clip_path = os.path.join(output_clips_folder, "clipped_video.mp4")
        clip_video(downloaded_video_path, output_clip_path, duration=5)

if __name__ == "__main__":
    main()

