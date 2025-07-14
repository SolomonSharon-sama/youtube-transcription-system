# youtube-transcription-system
A simple python code that auto downloads bulk videos from youtube channels(You can download playlist by playlist) and transcribes them using yt-dlp &amp; whisper.

## Features
- Downloads YouTube playlist videos as MP3s using `yt-dlp`.
- Saves to `~/Desktop/transcriptions/lenny/strategy`.

**Update**
- Transcribes audio with Whisper and diarizes speakers with `pyannote.audio`.
- Updates status on videos transcribed successfully and videos that failed
- Confirms if video transcript already exists and skips over 


## Setup
```bash
pip3 install yt-dlp whisper pyannote.audio
