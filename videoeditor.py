
import tkinter as tk
from tkinter import filedialog, messagebox
import moviepy.editor as mp
import whisper
from transformers import MarianMTModel, MarianTokenizer
from gtts import gTTS
import ffmpeg
import os
import threading

def extract_audio(video_path, audio_output):
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_output)

def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]

def translate_text(text, tgt_lang):
    src_lang = "en"
    model_name = f'Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}'
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    tokens = tokenizer.prepare_seq2seq_batch([text], return_tensors='pt')
    translated = model.generate(**tokens)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

def text_to_speech(text, output_audio, lang='fr'):
    tts = gTTS(text=text, lang=lang)
    tts.save(output_audio)

def create_subtitle_file(text, output_path, video_duration=None):
    """Create a simple SRT subtitle file"""
    # Split text into sentences and clean them
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    
    if not sentences:
        return
    
    # Calculate duration per subtitle (default to 4 seconds if no video duration)
    if video_duration:
        duration_per_subtitle = max(2, video_duration / len(sentences))
    else:
        duration_per_subtitle = 4
    
    subtitle_content = ""
    
    for i, sentence in enumerate(sentences):
        if sentence:
            start_time = i * duration_per_subtitle
            end_time = (i + 1) * duration_per_subtitle
            
            # Format time as HH:MM:SS,mmm
            start_formatted = f"{int(start_time//3600):02d}:{int((start_time%3600)//60):02d}:{int(start_time%60):02d},{int((start_time%1)*1000):03d}"
            end_formatted = f"{int(end_time//3600):02d}:{int((end_time%3600)//60):02d}:{int(end_time%60):02d},{int((end_time%1)*1000):03d}"
            
            subtitle_content += f"{i+1}\n"
            subtitle_content += f"{start_formatted} --> {end_formatted}\n"
            subtitle_content += f"{sentence}\n\n"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(subtitle_content)

def replace_audio_in_video(video_path, new_audio_path, output_path, subtitle_path=None):
    """Replace audio in video and optionally add subtitles"""
    try:
        if subtitle_path and os.path.exists(subtitle_path):
            # Escape the subtitle path for FFmpeg
            escaped_subtitle_path = subtitle_path.replace('\\', '\\\\').replace(':', '\\:')
            
            # Use moviepy for subtitle integration as it's more reliable
            video = mp.VideoFileClip(video_path)
            audio = mp.AudioFileClip(new_audio_path)
            
            # Set the new audio
            final_video = video.set_audio(audio)
            
            # Create subtitle clips
            subtitle_clips = []
            with open(subtitle_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse SRT content
            subtitles = []
            blocks = content.strip().split('\n\n')
            
            for block in blocks:
                lines = block.split('\n')
                if len(lines) >= 3:
                    time_line = lines[1]
                    text_line = ' '.join(lines[2:])
                    
                    # Parse time
                    start_str, end_str = time_line.split(' --> ')
                    start_time = parse_time(start_str)
                    end_time = parse_time(end_str)
                    
                    # Create text clip
                    txt_clip = mp.TextClip(text_line, 
                                         fontsize=24, 
                                         color='white', 
                                         font='Arial-Bold',
                                         stroke_color='black',
                                         stroke_width=2)
                    txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(end_time - start_time).set_start(start_time)
                    subtitle_clips.append(txt_clip)
            
            # Composite video with subtitles
            if subtitle_clips:
                final_video = mp.CompositeVideoClip([final_video] + subtitle_clips)
            
            # Write the final video
            final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')
            
            # Clean up
            video.close()
            audio.close()
            final_video.close()
            
        else:
            # No subtitles, just replace audio
            video = ffmpeg.input(video_path)
            audio = ffmpeg.input(new_audio_path)
            ffmpeg.output(video.video, audio.audio, output_path, vcodec='copy', acodec='aac').overwrite_output().run()
            
    except Exception as e:
        print(f"Error in replace_audio_in_video: {e}")
        # Fallback to simple audio replacement
        video = ffmpeg.input(video_path)
        audio = ffmpeg.input(new_audio_path)
        ffmpeg.output(video.video, audio.audio, output_path, vcodec='copy', acodec='aac').overwrite_output().run()

def parse_time(time_str):
    """Parse SRT time format to seconds"""
    time_str = time_str.replace(',', '.')
    parts = time_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = float(parts[2])
    return hours * 3600 + minutes * 60 + seconds

def process_video(video_path, lang_code, output_label, include_subtitles=False):
    base = os.path.splitext(video_path)[0]
    extracted_audio = base + "_audio.wav"
    translated_audio = base + "_translated.mp3"
    subtitle_file = base + "_subtitles.srt"
    final_video = base + "_translated.mp4"

    try:
        output_label.config(text="Extracting audio...")
        extract_audio(video_path, extracted_audio)

        output_label.config(text="Transcribing...")
        text = transcribe_audio(extracted_audio)

        output_label.config(text="Translating...")
        translated = translate_text(text, lang_code)

        output_label.config(text="Generating speech...")
        text_to_speech(translated, translated_audio, lang=lang_code)

        # Create subtitle file if requested
        if include_subtitles:
            output_label.config(text="Creating subtitles...")
            # Get video duration for better subtitle timing
            video_clip = mp.VideoFileClip(video_path)
            video_duration = video_clip.duration
            video_clip.close()
            create_subtitle_file(translated, subtitle_file, video_duration)

        output_label.config(text="Replacing audio...")
        replace_audio_in_video(
            video_path, 
            translated_audio, 
            final_video, 
            subtitle_file if include_subtitles else None
        )

        output_label.config(text=f"Done! Output: {final_video}")
        messagebox.showinfo("Success", f"Translated video saved as:\n{final_video}")
        
        # Clean up temporary files
        if os.path.exists(extracted_audio):
            os.remove(extracted_audio)
        if os.path.exists(translated_audio):
            os.remove(translated_audio)
        if include_subtitles and os.path.exists(subtitle_file):
            os.remove(subtitle_file)
            
    except Exception as e:
        output_label.config(text="Error occurred.")
        messagebox.showerror("Error", str(e))

def browse_file(entry):
    filepath = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    entry.delete(0, tk.END)
    entry.insert(0, filepath)

def start_processing(entry, lang_code_entry, output_label, subtitle_var):
    path = entry.get()
    lang = lang_code_entry.get()
    include_subs = subtitle_var.get()
    
    if not path or not lang:
        messagebox.showwarning("Missing Info", "Please select video and enter language code.")
        return
    
    threading.Thread(target=process_video, args=(path, lang, output_label, include_subs)).start()

def create_gui():
    root = tk.Tk()
    root.title("ECHO - Every Character Heard Original")
    root.geometry("800x500")

    # Video file selection
    tk.Label(root, text="Select video file (.mp4):").pack(pady=5)
    file_entry = tk.Entry(root, width=60)
    file_entry.pack()
    tk.Button(root, text="Browse", command=lambda: browse_file(file_entry)).pack()

    # Language code input
    tk.Label(root, text="Target language code (e.g., 'fr', 'hi', 'es'):").pack(pady=5)
    lang_entry = tk.Entry(root)
    lang_entry.pack()

    # Subtitle option
    subtitle_var = tk.BooleanVar()
    subtitle_check = tk.Checkbutton(
        root, 
        text="Include subtitles in video", 
        variable=subtitle_var
    )
    subtitle_check.pack(pady=10)

    # Output status
    output_label = tk.Label(root, text="", fg="blue")
    output_label.pack(pady=10)

    # Process button
    tk.Button(
        root, 
        text="Translate & Generate", 
        command=lambda: start_processing(file_entry, lang_entry, output_label, subtitle_var),
        bg="green",
        fg="white",
        font=("Arial", 12, "bold")
    ).pack(pady=10)

    # Instructions
    instructions = tk.Label(
        root, 
        text="Instructions:\n1. Select your MP4 video file\n2. Enter target language code\n3. Check subtitle option if needed\n4. Click 'Translate & Generate'",
        justify=tk.LEFT,
        fg="gray"
    )
    instructions.pack(pady=10)

    root.mainloop()

create_gui()
