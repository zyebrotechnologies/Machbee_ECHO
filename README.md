# Machbee_ECHO
AI platform that auto-generates lip-synced dubbing and subtitles in multiple languages, preserving original voices. Upload a video, select languages—E.C.H.O. handles the rest with perfect sync, voice cloning, and neural video re-synthesis.


● **Title:** ECHO - Every Character Heard Original
● **Basic Details:** Machbee - Rahul Mohan , Abhijith Surendran , Lakshmi Radhakrishnan - Entertainment - 
**Problem Statement**: Language barriers limit the global reach of video content, making it inaccessible to non-native audiences. Manual dubbing and translation are costly and time-consuming. Our solution automates transcription, translation, voiceover, and subtitle generation, enabling fast, affordable, and scalable multilingual video localization for educators, creators, and businesses. 
**Solution** :Language barriers limit the global reach of video content, making it inaccessible to non-native audiences. Manual dubbing and translation are costly and time-consuming. Our solution automates transcription, translation, voiceover, and subtitle generation, enabling fast, affordable, and scalable multilingual video localization for educators, creators, and businesses. 
**Project Description** :This project is an AI-powered desktop application that automates the multilingual localization of video content. Users can upload any MP4 video, select a target language, and the tool performs transcription using Whisper, translates the text using MarianMT, and generates natural voiceovers using gTTS. Optionally, subtitles are created and overlaid on the video. The processed video is then saved with the new audio and/or subtitles embedded. Designed with a simple Tkinter GUI, the application supports offline usage and is ideal for educators, content creators, NGOs, and businesses seeking to expand their audience reach across language boundaries efficiently and affordably.
**● Technical Details**: Speech to Text Transcription : WHISPER by OpenAI
Text to Speech : gTTS, pyttsx3, Edge TTS, Coqui TTS
Subtitle Generation Translation : transformers library from Hugginface & MarianMTModel MarianTokenizer from Helsinki-NLP
Audio Extraction & Video Generation : Moviepy, ffmpeg-python
Framework : Tkinter
Lip Sync : Wav2Lip, SadTalker 
**● Installation and execution instructions**

✅ 1. Clone or Download the Project

git clone https://github.com/your-repo-name/videoeditor.git
cd videoeditor

✅ 2. Set Up Python Environment

python -m venv myenv
# Windows
myenv\Scripts\activate
# macOS/Linux
source myenv/bin/activate

✅ 3. Install Dependencies

pip install moviepy openai-whisper gtts ffmpeg-python transformers torch
Note: tkinter is included by default in standard Python installations.

✅ 4. Install FFmpeg
Windows: Download from ffmpeg.org, unzip, and add bin/ to your system PATH.

macOS:

brew install ffmpeg
Linux:

sudo apt install ffmpeg
▶️ Running the Application

python videoeditor.py

● Screenshots
![WhatsApp Image 2025-07-20 at 08 57 51_c23a9332](https://github.com/user-attachments/assets/deedd1db-7b6f-4523-8b25-cda3c88052d1)
