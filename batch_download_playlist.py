import subprocess
import os
import json

# Nested folder to save files
output_dir = "/Users/mac/Desktop/"
os.makedirs(output_dir, exist_ok=True)

# Playlist URL (add from Lenny's channel)
playlist_url = ""  # Replace with playlist URL

# Get video URLs from playlist
try:
    result = subprocess.run(
        ["yt-dlp", "--flat-playlist", "--print", "url", playlist_url],
        capture_output=True, text=True, check=True
    )
    video_urls = result.stdout.strip().split("\n")
    print(f"Found {len(video_urls)} videos in playlist")
except Exception as e:
    print(f"Error fetching playlist: {e}")
    exit(1)

# Download each video as MP3 with original title
for url in video_urls:
    try:
        # Get video title with yt-dlp
        title_result = subprocess.run(
            ["yt-dlp", "--get-title", url],
            capture_output=True, text=True, check=True
        )
        title = title_result.stdout.strip().replace("/", "_").replace(":", "_").replace("|", "_")
        output = f"{output_dir}/{title}.mp3"
        command = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format", "mp3",
            "-o", output,
            url
        ]
        subprocess.run(command, check=True)
        print(f"Downloaded: {output}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        continue
