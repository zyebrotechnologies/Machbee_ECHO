# import tkinter as tk
# from tkinter import filedialog, messagebox
# import moviepy.editor as mp
# import whisper
# from transformers import MarianMTModel, MarianTokenizer
# from gtts import gTTS
# import ffmpeg
# import os
# import threading

# def extract_audio(video_path, audio_output):
#     video = mp.VideoFileClip(video_path)
#     video.audio.write_audiofile(audio_output)

# def transcribe_audio(audio_path):
#     model = whisper.load_model("base")
#     result = model.transcribe(audio_path)
#     return result["text"]

# def translate_text(text, tgt_lang):
#     src_lang = "en"
#     model_name = f'Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}'
#     tokenizer = MarianTokenizer.from_pretrained(model_name)
#     model = MarianMTModel.from_pretrained(model_name)
#     tokens = tokenizer.prepare_seq2seq_batch([text], return_tensors='pt')
#     translated = model.generate(**tokens)
#     return tokenizer.decode(translated[0], skip_special_tokens=True)

# def text_to_speech(text, output_audio, lang='fr'):
#     tts = gTTS(text=text, lang=lang)
#     tts.save(output_audio)

# def replace_audio_in_video(video_path, new_audio_path, output_path):
#     video = ffmpeg.input(video_path)
#     audio = ffmpeg.input(new_audio_path)
#     ffmpeg.output(video.video, audio.audio, output_path, vcodec='copy', acodec='aac').overwrite_output().run()

# def process_video(video_path, lang_code, output_label):
#     base = os.path.splitext(video_path)[0]
#     extracted_audio = base + "_audio.wav"
#     translated_audio = base + "_translated.mp3"
#     final_video = base + "_translated.mp4"

#     try:
#         output_label.config(text="Extracting audio...")
#         extract_audio(video_path, extracted_audio)

#         output_label.config(text="Transcribing...")
#         text = transcribe_audio(extracted_audio)

#         output_label.config(text="Translating...")
#         translated = translate_text(text, lang_code)

#         output_label.config(text="Generating speech...")
#         text_to_speech(translated, translated_audio, lang=lang_code)

#         output_label.config(text="Replacing audio...")
#         replace_audio_in_video(video_path, translated_audio, final_video)

#         output_label.config(text=f"Done! Output: {final_video}")
#         messagebox.showinfo("Success", f"Translated video saved as:\n{final_video}")
#     except Exception as e:
#         output_label.config(text="Error occurred.")
#         messagebox.showerror("Error", str(e))

# def browse_file(entry):
#     filepath = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
#     entry.delete(0, tk.END)
#     entry.insert(0, filepath)

# def start_processing(entry, lang_code_entry, output_label):
#     path = entry.get()
#     lang = lang_code_entry.get()
#     if not path or not lang:
#         messagebox.showwarning("Missing Info", "Please select video and enter language code.")
#         return
#     threading.Thread(target=process_video, args=(path, lang, output_label)).start()

# def create_gui():
#     root = tk.Tk()
#     root.title("Translate Video Audio")

#     tk.Label(root, text="Select video file (.mp4):").pack(pady=5)
#     file_entry = tk.Entry(root, width=60)
#     file_entry.pack()
#     tk.Button(root, text="Browse", command=lambda: browse_file(file_entry)).pack()

#     tk.Label(root, text="Target language code (e.g., 'fr', 'hi', 'es'):").pack(pady=5)
#     lang_entry = tk.Entry(root)
#     lang_entry.pack()

#     output_label = tk.Label(root, text="", fg="blue")
#     output_label.pack(pady=10)

#     tk.Button(root, text="Translate & Generate", command=lambda: start_processing(file_entry, lang_entry, output_label)).pack(pady=10)

#     root.mainloop()

# create_gui()
##########################################################################################################################################################################33
# import tkinter as tk
# from tkinter import filedialog, messagebox, ttk
# import moviepy.editor as mp
# import whisper
# from transformers import MarianMTModel, MarianTokenizer
# from gtts import gTTS
# import ffmpeg
# import os
# import threading

# # Language mappings for better user experience
# LANGUAGE_OPTIONS = {
#     'French': 'fr',
#     'Hindi': 'hi', 
#     'Spanish': 'es',
#     'Malayalam': 'ml',
#     'German': 'de',
#     'Italian': 'it',
#     'Portuguese': 'pt',
#     'Russian': 'ru',
#     'Japanese': 'ja',
#     'Korean': 'ko',
#     'Chinese': 'zh',
#     'Arabic': 'ar'
# }

# def extract_audio(video_path, audio_output):
#     video = mp.VideoFileClip(video_path)
#     video.audio.write_audiofile(audio_output)

# def transcribe_audio(audio_path):
#     model = whisper.load_model("base")
#     result = model.transcribe(audio_path)
#     return result["text"]

# def translate_text(text, tgt_lang):
#     src_lang = "en"
    
#     # Special handling for Malayalam and other languages
#     if tgt_lang == "ml":
#         # For Malayalam, we might need to use a different model or approach
#         # Check if Malayalam model exists, otherwise use a fallback
#         try:
#             model_name = f'Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}'
#             tokenizer = MarianTokenizer.from_pretrained(model_name)
#             model = MarianMTModel.from_pretrained(model_name)
#         except:
#             # Fallback: Try using English to Indic languages model if available
#             try:
#                 model_name = 'Helsinki-NLP/opus-mt-en-mul'  # Multilingual model
#                 tokenizer = MarianTokenizer.from_pretrained(model_name)
#                 model = MarianMTModel.from_pretrained(model_name)
#             except:
#                 raise Exception("Malayalam translation model not available. Please install required models or use online translation services.")
#     else:
#         model_name = f'Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}'
#         tokenizer = MarianTokenizer.from_pretrained(model_name)
#         model = MarianMTModel.from_pretrained(model_name)
    
#     # Split text into smaller chunks for better translation
#     sentences = text.split('. ')
#     translated_sentences = []
    
#     for sentence in sentences:
#         if sentence.strip():
#             tokens = tokenizer.prepare_seq2seq_batch([sentence], return_tensors='pt')
#             translated = model.generate(**tokens)
#             translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
#             translated_sentences.append(translated_text)
    
#     return '. '.join(translated_sentences)

# def text_to_speech(text, output_audio, lang='fr'):
#     try:
#         tts = gTTS(text=text, lang=lang)
#         tts.save(output_audio)
#     except Exception as e:
#         if lang == 'ml':
#             # If Malayalam TTS fails, provide alternative suggestion
#             raise Exception(f"Malayalam TTS not available in gTTS. Error: {str(e)}")
#         else:
#             raise e

# def replace_audio_in_video(video_path, new_audio_path, output_path):
#     video = ffmpeg.input(video_path)
#     audio = ffmpeg.input(new_audio_path)
#     ffmpeg.output(video.video, audio.audio, output_path, vcodec='copy', acodec='aac').overwrite_output().run()

# def process_video(video_path, lang_code, output_label, progress_bar):
#     base = os.path.splitext(video_path)[0]
#     extracted_audio = base + "_audio.wav"
#     translated_audio = base + "_translated.mp3"
#     final_video = base + "_translated.mp4"

#     try:
#         progress_bar['value'] = 10
#         output_label.config(text="Extracting audio...")
#         extract_audio(video_path, extracted_audio)

#         progress_bar['value'] = 30
#         output_label.config(text="Transcribing...")
#         text = transcribe_audio(extracted_audio)

#         progress_bar['value'] = 50
#         output_label.config(text="Translating...")
#         translated = translate_text(text, lang_code)

#         progress_bar['value'] = 70
#         output_label.config(text="Generating speech...")
#         text_to_speech(translated, translated_audio, lang=lang_code)

#         progress_bar['value'] = 90
#         output_label.config(text="Replacing audio...")
#         replace_audio_in_video(video_path, translated_audio, final_video)

#         progress_bar['value'] = 100
#         output_label.config(text=f"Done! Output: {final_video}")
#         messagebox.showinfo("Success", f"Translated video saved as:\n{final_video}")
        
#         # Show translated text for Malayalam (since TTS might not work)
#         if lang_code == 'ml':
#             show_translated_text(translated)
            
#     except Exception as e:
#         progress_bar['value'] = 0
#         output_label.config(text="Error occurred.")
#         error_msg = str(e)
#         if 'Malayalam' in error_msg:
#             error_msg += "\n\nSuggestion: You can use the translated text with other Malayalam TTS services."
#         messagebox.showerror("Error", error_msg)

# def show_translated_text(text):
#     """Show translated text in a separate window"""
#     text_window = tk.Toplevel()
#     text_window.title("Translated Text")
#     text_window.geometry("600x400")
    
#     tk.Label(text_window, text="Translated Text:", font=("Arial", 12, "bold")).pack(pady=5)
    
#     text_area = tk.Text(text_window, wrap=tk.WORD, font=("Arial", 10))
#     text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
#     text_area.insert(tk.END, text)
    
#     # Add copy button
#     def copy_text():
#         text_window.clipboard_clear()
#         text_window.clipboard_append(text)
#         messagebox.showinfo("Copied", "Text copied to clipboard!")
    
#     tk.Button(text_window, text="Copy Text", command=copy_text).pack(pady=5)

# def browse_file(entry):
#     filepath = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
#     entry.delete(0, tk.END)
#     entry.insert(0, filepath)

# def start_processing(entry, lang_combo, output_label, progress_bar):
#     path = entry.get()
#     selected_lang = lang_combo.get()
    
#     if not path or not selected_lang:
#         messagebox.showwarning("Missing Info", "Please select video and choose target language.")
#         return
    
#     lang_code = LANGUAGE_OPTIONS.get(selected_lang, selected_lang.lower())
    
#     # Reset progress bar
#     progress_bar['value'] = 0
    
#     threading.Thread(target=process_video, args=(path, lang_code, output_label, progress_bar)).start()

# def create_gui():
#     root = tk.Tk()
#     root.title("Video Audio Translator - Malayalam Support")
#     root.geometry("500x300")

#     # File selection
#     tk.Label(root, text="Select video file (.mp4):", font=("Arial", 10)).pack(pady=5)
#     file_entry = tk.Entry(root, width=60)
#     file_entry.pack(pady=5)
#     tk.Button(root, text="Browse", command=lambda: browse_file(file_entry)).pack(pady=5)

#     # Language selection
#     tk.Label(root, text="Select target language:", font=("Arial", 10)).pack(pady=5)
#     lang_combo = ttk.Combobox(root, values=list(LANGUAGE_OPTIONS.keys()), state="readonly", width=20)
#     lang_combo.pack(pady=5)
#     lang_combo.set("Malayalam")  # Default to Malayalam

#     # Progress bar
#     progress_bar = ttk.Progressbar(root, length=400, mode='determinate')
#     progress_bar.pack(pady=10)

#     # Status label
#     output_label = tk.Label(root, text="", fg="blue", font=("Arial", 9))
#     output_label.pack(pady=10)

#     # Process button
#     tk.Button(root, text="Translate & Generate", 
#               command=lambda: start_processing(file_entry, lang_combo, output_label, progress_bar),
#               bg="green", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

#     # Info label
#     info_label = tk.Label(root, text="Note: Malayalam TTS might not be available in gTTS.\nTranslated text will be shown in a separate window.", 
#                          fg="gray", font=("Arial", 8))
#     info_label.pack(pady=5)

#     root.mainloop()

# # Additional setup instructions
# def print_setup_instructions():
#     print("""
#     Setup Instructions for Malayalam Support:
    
#     1. Install required packages:
#        pip install moviepy whisper transformers gtts ffmpeg-python torch
    
#     2. For Malayalam translation, you might need additional models:
#        - The code will attempt to use Helsinki-NLP models
#        - If Malayalam model is not available, consider using:
#          * Google Translate API
#          * Microsoft Translator API
#          * Or other translation services
    
#     3. For Malayalam TTS (Text-to-Speech):
#        - gTTS might not support Malayalam well
#        - Consider using:
#          * Azure Cognitive Services
#          * Amazon Polly
#          * Google Cloud TTS
#          * Indian language TTS services
    
#     4. Alternative approach for Malayalam:
#        - Use the translated text output
#        - Feed it to specialized Malayalam TTS services
#        - Or use it for subtitles instead of audio replacement
#     """)

# if __name__ == "__main__":
#     print_setup_instructions()
#     create_gui()

##################################################################################################################################################

# import tkinter as tk
# from tkinter import filedialog, messagebox, ttk
# import moviepy.editor as mp
# import whisper
# from transformers import MarianMTModel, MarianTokenizer
# from gtts import gTTS
# import ffmpeg
# import os
# import threading
# import json
# import re
# from datetime import timedelta
# import tempfile

# # Language mappings for better user experience
# LANGUAGE_OPTIONS = {
#     'French': 'fr',
#     'Hindi': 'hi', 
#     'Spanish': 'es',
#     'Malayalam': 'ml',
#     'German': 'de',
#     'Italian': 'it',
#     'Portuguese': 'pt',
#     'Russian': 'ru',
#     'Japanese': 'ja',
#     'Korean': 'ko',
#     'Chinese': 'zh',
#     'Arabic': 'ar'
# }

# class VideoProcessor:
#     def __init__(self):
#         self.original_segments = []
#         self.translated_segments = []
#         self.video_duration = 0
        
#     def extract_audio(self, video_path, audio_output):
#         """Extract audio from video file"""
#         video = mp.VideoFileClip(video_path)
#         self.video_duration = video.duration
#         if video.audio is not None:
#             video.audio.write_audiofile(audio_output, fps=22050)
#             video.audio.close()
#         else:
#             # Create a silent audio file if no audio in video
#             silent_audio = mp.AudioClip(make_frame=lambda t: [0, 0], 
#                                       duration=self.video_duration, fps=22050)
#             silent_audio.write_audiofile(audio_output, fps=22050)
#             silent_audio.close()
#         video.close()

#     def transcribe_audio_with_timestamps(self, audio_path):
#         """Transcribe audio with word-level timestamps"""
#         model = whisper.load_model("base")
#         result = model.transcribe(audio_path, word_timestamps=True)
        
#         # Extract segments with timestamps
#         segments = []
#         for segment in result["segments"]:
#             segments.append({
#                 "start": segment["start"],
#                 "end": segment["end"],
#                 "text": segment["text"].strip(),
#                 "words": segment.get("words", [])
#             })
        
#         self.original_segments = segments
#         return result["text"], segments

#     def translate_text_segments(self, segments, tgt_lang):
#         """Translate text segments while preserving timing"""
#         src_lang = "en"
        
#         # Load translation model
#         try:
#             if tgt_lang == "ml":
#                 try:
#                     model_name = f'Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}'
#                     tokenizer = MarianTokenizer.from_pretrained(model_name)
#                     model = MarianMTModel.from_pretrained(model_name)
#                 except:
#                     model_name = 'Helsinki-NLP/opus-mt-en-mul'
#                     tokenizer = MarianTokenizer.from_pretrained(model_name)
#                     model = MarianMTModel.from_pretrained(model_name)
#             else:
#                 model_name = f'Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}'
#                 tokenizer = MarianTokenizer.from_pretrained(model_name)
#                 model = MarianMTModel.from_pretrained(model_name)
#         except Exception as e:
#             raise Exception(f"Translation model for {tgt_lang} not available: {str(e)}")
        
#         translated_segments = []
        
#         for segment in segments:
#             text = segment["text"]
#             if text.strip():
#                 try:
#                     tokens = tokenizer.prepare_seq2seq_batch([text], return_tensors='pt')
#                     translated = model.generate(**tokens)
#                     translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
                    
#                     translated_segments.append({
#                         "start": segment["start"],
#                         "end": segment["end"],
#                         "original_text": text,
#                         "translated_text": translated_text,
#                         "duration": segment["end"] - segment["start"]
#                     })
#                 except Exception as e:
#                     print(f"Translation error for segment: {text[:50]}... Error: {str(e)}")
#                     # Keep original text if translation fails
#                     translated_segments.append({
#                         "start": segment["start"],
#                         "end": segment["end"],
#                         "original_text": text,
#                         "translated_text": text,
#                         "duration": segment["end"] - segment["start"]
#                     })
        
#         self.translated_segments = translated_segments
#         return translated_segments

#     def create_subtitle_file(self, segments, output_path, subtitle_format='srt'):
#         """Create subtitle file from segments"""
#         if subtitle_format == 'srt':
#             self.create_srt_file(segments, output_path)
#         elif subtitle_format == 'vtt':
#             self.create_vtt_file(segments, output_path)

#     def create_srt_file(self, segments, output_path):
#         """Create SRT subtitle file"""
#         with open(output_path, 'w', encoding='utf-8') as f:
#             for i, segment in enumerate(segments, 1):
#                 start_time = self.seconds_to_srt_time(segment["start"])
#                 end_time = self.seconds_to_srt_time(segment["end"])
                
#                 f.write(f"{i}\n")
#                 f.write(f"{start_time} --> {end_time}\n")
#                 f.write(f"{segment['translated_text']}\n\n")

#     def create_vtt_file(self, segments, output_path):
#         """Create VTT subtitle file"""
#         with open(output_path, 'w', encoding='utf-8') as f:
#             f.write("WEBVTT\n\n")
#             for segment in segments:
#                 start_time = self.seconds_to_vtt_time(segment["start"])
#                 end_time = self.seconds_to_vtt_time(segment["end"])
                
#                 f.write(f"{start_time} --> {end_time}\n")
#                 f.write(f"{segment['translated_text']}\n\n")

#     def seconds_to_srt_time(self, seconds):
#         """Convert seconds to SRT time format"""
#         td = timedelta(seconds=seconds)
#         hours = int(td.total_seconds() // 3600)
#         minutes = int((td.total_seconds() % 3600) // 60)
#         secs = int(td.total_seconds() % 60)
#         millisecs = int((td.total_seconds() % 1) * 1000)
#         return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

#     def seconds_to_vtt_time(self, seconds):
#         """Convert seconds to VTT time format"""
#         td = timedelta(seconds=seconds)
#         hours = int(td.total_seconds() // 3600)
#         minutes = int((td.total_seconds() % 3600) // 60)
#         secs = int(td.total_seconds() % 60)
#         millisecs = int((td.total_seconds() % 1) * 1000)
#         return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millisecs:03d}"

#     def generate_synced_audio(self, segments, lang_code, output_path):
#         """Generate synchronized audio from translated segments"""
#         # Create a list to store audio segments with their timings
#         audio_segments = []
        
#         for segment in segments:
#             text = segment["translated_text"]
#             start_time = segment["start"]
#             end_time = segment["end"]
#             duration = end_time - start_time
            
#             if text.strip():
#                 # Generate TTS for this segment
#                 temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
#                 try:
#                     tts = gTTS(text=text, lang=lang_code, slow=False)
#                     tts.save(temp_audio.name)
                    
#                     # Load the audio clip
#                     audio_clip = mp.AudioFileClip(temp_audio.name)
                    
#                     # Adjust speed to match original timing
#                     if audio_clip.duration > duration:
#                         # Speed up if TTS is longer than original
#                         speed_factor = audio_clip.duration / duration
#                         audio_clip = audio_clip.fx(mp.afx.speedx, speed_factor)
#                     elif audio_clip.duration < duration:
#                         # Add silence if TTS is shorter than original
#                         silence_duration = duration - audio_clip.duration
#                         silence = mp.AudioClip(make_frame=lambda t: [0, 0], duration=silence_duration, fps=22050)
#                         audio_clip = mp.concatenate_audioclips([audio_clip, silence])
                    
#                     # Store segment info
#                     audio_segments.append({
#                         'clip': audio_clip,
#                         'start': start_time,
#                         'end': end_time,
#                         'duration': duration
#                     })
                    
#                 except Exception as e:
#                     print(f"TTS error for segment: {text[:50]}... Error: {str(e)}")
#                     # Create silence for failed segments
#                     silence = mp.AudioClip(make_frame=lambda t: [0, 0], duration=duration, fps=22050)
#                     audio_segments.append({
#                         'clip': silence,
#                         'start': start_time,
#                         'end': end_time,
#                         'duration': duration
#                     })
#                 finally:
#                     # Clean up temp file
#                     try:
#                         os.unlink(temp_audio.name)
#                     except:
#                         pass
        
#         if audio_segments:
#             # Create final audio by concatenating segments in order
#             try:
#                 # Sort segments by start time
#                 audio_segments.sort(key=lambda x: x['start'])
                
#                 # Create final audio timeline
#                 final_clips = []
#                 current_time = 0
                
#                 for segment in audio_segments:
#                     start_time = segment['start']
#                     clip = segment['clip']
                    
#                     # Add silence if there's a gap
#                     if start_time > current_time:
#                         gap_duration = start_time - current_time
#                         silence_gap = mp.AudioClip(make_frame=lambda t: [0, 0], 
#                                                  duration=gap_duration, fps=22050)
#                         final_clips.append(silence_gap)
                    
#                     # Add the audio clip
#                     final_clips.append(clip)
#                     current_time = start_time + clip.duration
                
#                 # Add final silence if needed
#                 if current_time < self.video_duration:
#                     final_silence = mp.AudioClip(make_frame=lambda t: [0, 0], 
#                                                duration=self.video_duration - current_time, fps=22050)
#                     final_clips.append(final_silence)
                
#                 # Concatenate all clips
#                 if final_clips:
#                     final_audio = mp.concatenate_audioclips(final_clips)
#                     final_audio.write_audiofile(output_path, fps=22050)
#                     final_audio.close()
                    
#                     # Clean up clips
#                     for clip in final_clips:
#                         if hasattr(clip, 'close'):
#                             clip.close()
                            
#             except Exception as e:
#                 print(f"Audio composition error: {str(e)}")
#                 # Fallback: create a simple silence track
#                 silence_track = mp.AudioClip(make_frame=lambda t: [0, 0], 
#                                            duration=self.video_duration, fps=22050)
#                 silence_track.write_audiofile(output_path, fps=22050)
#                 silence_track.close()

#     def create_video_with_subtitles(self, video_path, subtitle_path, output_path):
#         """Create video with embedded subtitles"""
#         try:
#             # Use ffmpeg to embed subtitles
#             video_input = ffmpeg.input(video_path)
            
#             # Add subtitles
#             video_with_subs = ffmpeg.filter(video_input, 'subtitles', subtitle_path)
            
#             # Output with subtitles
#             ffmpeg.output(video_with_subs, output_path, vcodec='libx264', acodec='aac').overwrite_output().run()
            
#         except Exception as e:
#             print(f"Subtitle embedding error: {str(e)}")
#             # Fallback: just copy the original video
#             import shutil
#             shutil.copy2(video_path, output_path)

#     def replace_audio_in_video(self, video_path, new_audio_path, output_path):
#         """Replace audio in video with proper sync"""
#         try:
#             video = ffmpeg.input(video_path)
#             audio = ffmpeg.input(new_audio_path)
            
#             # Ensure audio and video are properly synchronized
#             ffmpeg.output(
#                 video.video, 
#                 audio.audio, 
#                 output_path, 
#                 vcodec='copy', 
#                 acodec='aac',
#                 **{'avoid_negative_ts': 'make_zero'}
#             ).overwrite_output().run()
            
#         except Exception as e:
#             raise Exception(f"Audio replacement failed: {str(e)}")

# def process_video(video_path, lang_code, output_label, progress_bar, subtitle_var, audio_replace_var):
#     """Main video processing function"""
#     processor = VideoProcessor()
#     base = os.path.splitext(video_path)[0]
#     extracted_audio = base + "_audio.wav"
#     translated_audio = base + "_translated_audio.wav"
#     subtitle_file = base + "_subtitles.srt"
#     final_video = base + "_final.mp4"
    
#     try:
#         # Step 1: Extract audio
#         progress_bar['value'] = 10
#         output_label.config(text="Extracting audio...")
#         processor.extract_audio(video_path, extracted_audio)

#         # Step 2: Transcribe with timestamps
#         progress_bar['value'] = 25
#         output_label.config(text="Transcribing with timestamps...")
#         full_text, segments = processor.transcribe_audio_with_timestamps(extracted_audio)

#         # Step 3: Translate segments
#         progress_bar['value'] = 45
#         output_label.config(text="Translating segments...")
#         translated_segments = processor.translate_text_segments(segments, lang_code)

#         # Step 4: Create subtitles if requested
#         if subtitle_var.get():
#             progress_bar['value'] = 60
#             output_label.config(text="Creating subtitles...")
#             processor.create_subtitle_file(translated_segments, subtitle_file)

#         # Step 5: Generate synced audio if requested
#         if audio_replace_var.get():
#             progress_bar['value'] = 75
#             output_label.config(text="Generating synchronized audio...")
#             processor.generate_synced_audio(translated_segments, lang_code, translated_audio)

#         # Step 6: Create final video
#         progress_bar['value'] = 90
#         output_label.config(text="Creating final video...")
        
#         if audio_replace_var.get() and subtitle_var.get():
#             # Replace audio first, then add subtitles
#             temp_video = base + "_temp_audio.mp4"
#             processor.replace_audio_in_video(video_path, translated_audio, temp_video)
#             processor.create_video_with_subtitles(temp_video, subtitle_file, final_video)
#             os.remove(temp_video)
#         elif audio_replace_var.get():
#             # Only replace audio
#             processor.replace_audio_in_video(video_path, translated_audio, final_video)
#         elif subtitle_var.get():
#             # Only add subtitles
#             processor.create_video_with_subtitles(video_path, subtitle_file, final_video)
#         else:
#             # No changes requested
#             import shutil
#             shutil.copy2(video_path, final_video)

#         progress_bar['value'] = 100
#         output_label.config(text=f"Done! Output: {final_video}")
        
#         # Show results
#         result_message = f"Processing complete!\n\nOutput video: {final_video}"
#         if subtitle_var.get():
#             result_message += f"\nSubtitle file: {subtitle_file}"
        
#         messagebox.showinfo("Success", result_message)
        
#         # Show translated text for reference
#         if lang_code == 'ml' or not audio_replace_var.get():
#             show_translated_segments(translated_segments)
            
#     except Exception as e:
#         progress_bar['value'] = 0
#         output_label.config(text="Error occurred.")
#         messagebox.showerror("Error", f"Processing failed: {str(e)}")
#     finally:
#         # Clean up temporary files
#         for temp_file in [extracted_audio, translated_audio]:
#             if os.path.exists(temp_file):
#                 try:
#                     os.remove(temp_file)
#                 except:
#                     pass

# def show_translated_segments(segments):
#     """Show translated segments in a separate window"""
#     text_window = tk.Toplevel()
#     text_window.title("Translated Segments")
#     text_window.geometry("800x600")
    
#     tk.Label(text_window, text="Translated Segments with Timestamps:", 
#              font=("Arial", 12, "bold")).pack(pady=5)
    
#     # Create text area with scrollbar
#     frame = tk.Frame(text_window)
#     frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
#     text_area = tk.Text(frame, wrap=tk.WORD, font=("Arial", 10))
#     scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=text_area.yview)
#     text_area.configure(yscrollcommand=scrollbar.set)
    
#     text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#     scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
#     # Add segments to text area
#     for i, segment in enumerate(segments, 1):
#         start_time = str(timedelta(seconds=segment["start"]))[:7]
#         end_time = str(timedelta(seconds=segment["end"]))[:7]
        
#         text_area.insert(tk.END, f"{i}. [{start_time} - {end_time}]\n")
#         text_area.insert(tk.END, f"Original: {segment['original_text']}\n")
#         text_area.insert(tk.END, f"Translated: {segment['translated_text']}\n\n")
    
#     # Add export buttons
#     button_frame = tk.Frame(text_window)
#     button_frame.pack(pady=5)
    
#     def export_text():
#         content = text_area.get(1.0, tk.END)
#         file_path = filedialog.asksaveasfilename(
#             defaultextension=".txt",
#             filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
#         )
#         if file_path:
#             with open(file_path, 'w', encoding='utf-8') as f:
#                 f.write(content)
#             messagebox.showinfo("Exported", f"Text exported to: {file_path}")
    
#     def copy_all():
#         content = text_area.get(1.0, tk.END)
#         text_window.clipboard_clear()
#         text_window.clipboard_append(content)
#         messagebox.showinfo("Copied", "All text copied to clipboard!")
    
#     tk.Button(button_frame, text="Export to File", command=export_text).pack(side=tk.LEFT, padx=5)
#     tk.Button(button_frame, text="Copy All", command=copy_all).pack(side=tk.LEFT, padx=5)

# def browse_file(entry):
#     """Browse for video file"""
#     filepath = filedialog.askopenfilename(
#         filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv"), ("All files", "*.*")]
#     )
#     entry.delete(0, tk.END)
#     entry.insert(0, filepath)

# def start_processing(entry, lang_combo, output_label, progress_bar, subtitle_var, audio_replace_var):
#     """Start the processing in a separate thread"""
#     path = entry.get()
#     selected_lang = lang_combo.get()
    
#     if not path or not selected_lang:
#         messagebox.showwarning("Missing Info", "Please select video and choose target language.")
#         return
    
#     if not os.path.exists(path):
#         messagebox.showerror("File Error", "Selected video file does not exist.")
#         return
    
#     if not subtitle_var.get() and not audio_replace_var.get():
#         messagebox.showwarning("No Action", "Please select at least one option: Add Subtitles or Replace Audio.")
#         return
    
#     lang_code = LANGUAGE_OPTIONS.get(selected_lang, selected_lang.lower())
    
#     # Reset progress bar
#     progress_bar['value'] = 0
    
#     # Start processing in separate thread
#     threading.Thread(
#         target=process_video, 
#         args=(path, lang_code, output_label, progress_bar, subtitle_var, audio_replace_var),
#         daemon=True
#     ).start()

# def create_gui():
#     """Create the main GUI"""
#     root = tk.Tk()
#     root.title("Advanced Video Dubbing Tool - Subtitles & Sync")
#     root.geometry("600x450")
#     root.configure(bg='#f0f0f0')

#     # Main frame
#     main_frame = tk.Frame(root, bg='#f0f0f0')
#     main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

#     # Title
#     title_label = tk.Label(main_frame, text="Advanced Video Dubbing Tool", 
#                           font=("Arial", 16, "bold"), bg='#f0f0f0')
#     title_label.pack(pady=(0, 20))

#     # File selection section
#     file_frame = tk.LabelFrame(main_frame, text="Video Selection", font=("Arial", 10, "bold"), bg='#f0f0f0')
#     file_frame.pack(fill=tk.X, pady=(0, 15))

#     tk.Label(file_frame, text="Select video file:", font=("Arial", 10), bg='#f0f0f0').pack(anchor=tk.W, padx=10, pady=5)
    
#     file_entry_frame = tk.Frame(file_frame, bg='#f0f0f0')
#     file_entry_frame.pack(fill=tk.X, padx=10, pady=5)
    
#     file_entry = tk.Entry(file_entry_frame, font=("Arial", 10))
#     file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
#     browse_btn = tk.Button(file_entry_frame, text="Browse", 
#                           command=lambda: browse_file(file_entry),
#                           bg='#4CAF50', fg='white', font=("Arial", 9))
#     browse_btn.pack(side=tk.RIGHT, padx=(5, 0))

#     # Language selection section
#     lang_frame = tk.LabelFrame(main_frame, text="Language Settings", font=("Arial", 10, "bold"), bg='#f0f0f0')
#     lang_frame.pack(fill=tk.X, pady=(0, 15))

#     tk.Label(lang_frame, text="Target language:", font=("Arial", 10), bg='#f0f0f0').pack(anchor=tk.W, padx=10, pady=5)
    
#     lang_combo = ttk.Combobox(lang_frame, values=list(LANGUAGE_OPTIONS.keys()), 
#                              state="readonly", font=("Arial", 10))
#     lang_combo.pack(anchor=tk.W, padx=10, pady=5)
#     lang_combo.set("Malayalam")

#     # Processing options section
#     options_frame = tk.LabelFrame(main_frame, text="Processing Options", font=("Arial", 10, "bold"), bg='#f0f0f0')
#     options_frame.pack(fill=tk.X, pady=(0, 15))

#     subtitle_var = tk.BooleanVar(value=True)
#     audio_replace_var = tk.BooleanVar(value=False)

#     tk.Checkbutton(options_frame, text="Add Subtitles (SRT file)", 
#                   variable=subtitle_var, font=("Arial", 10), bg='#f0f0f0').pack(anchor=tk.W, padx=10, pady=2)
    
#     tk.Checkbutton(options_frame, text="Replace Audio (Dubbing)", 
#                   variable=audio_replace_var, font=("Arial", 10), bg='#f0f0f0').pack(anchor=tk.W, padx=10, pady=2)

#     # Progress section
#     progress_frame = tk.LabelFrame(main_frame, text="Progress", font=("Arial", 10, "bold"), bg='#f0f0f0')
#     progress_frame.pack(fill=tk.X, pady=(0, 15))

#     progress_bar = ttk.Progressbar(progress_frame, length=500, mode='determinate')
#     progress_bar.pack(padx=10, pady=10)

#     output_label = tk.Label(progress_frame, text="Ready to process...", 
#                            fg="blue", font=("Arial", 9), bg='#f0f0f0')
#     output_label.pack(pady=(0, 10))

#     # Control buttons
#     button_frame = tk.Frame(main_frame, bg='#f0f0f0')
#     button_frame.pack(fill=tk.X, pady=(0, 10))

#     process_btn = tk.Button(button_frame, text="Start Processing", 
#                            command=lambda: start_processing(file_entry, lang_combo, output_label, 
#                                                           progress_bar, subtitle_var, audio_replace_var),
#                            bg="#2196F3", fg="white", font=("Arial", 12, "bold"),
#                            padx=20, pady=10)
#     process_btn.pack(side=tk.LEFT, padx=(0, 10))

#     def show_help():
#         help_text = """
# Features:
# • Add Subtitles: Creates synchronized subtitle files (SRT format)
# • Replace Audio: Generates dubbed audio with proper timing
# • Timestamp Sync: Maintains perfect audio-video synchronization
# • Multiple Languages: Support for 12+ languages
# • Batch Processing: Process multiple segments efficiently

# Tips:
# • For Malayalam: Subtitles work better than audio dubbing
# • Select both options for complete dubbing with subtitles
# • Processing time depends on video length and complexity
# • Ensure sufficient disk space for temporary files

# Requirements:
# • Python packages: whisper, transformers, moviepy, gtts, ffmpeg-python
# • FFmpeg installed on system
# • Internet connection for translation models
#         """
#         messagebox.showinfo("Help", help_text)

#     help_btn = tk.Button(button_frame, text="Help", command=show_help,
#                         bg="#FF9800", fg="white", font=("Arial", 10))
#     help_btn.pack(side=tk.RIGHT)

#     # Status info
#     info_text = ("Note: Processing time varies with video length. "
#                 "For Malayalam, subtitles are recommended over audio dubbing.")
#     info_label = tk.Label(main_frame, text=info_text, 
#                          fg="gray", font=("Arial", 8), bg='#f0f0f0', wraplength=550)
#     info_label.pack(pady=(10, 0))

#     root.mainloop()

# def print_setup_instructions():
#     """Print setup instructions"""
#     print("""
#     Enhanced Video Dubbing Tool Setup Instructions:
    
#     1. Install Python packages:
#        pip install moviepy whisper transformers gtts ffmpeg-python torch
    
#     2. Install FFmpeg (required for video processing):
#        - Windows: Download from https://ffmpeg.org/download.html
#        - macOS: brew install ffmpeg
#        - Linux: sudo apt-get install ffmpeg
    
#     3. Features:
#        ✓ Subtitle generation with perfect timing
#        ✓ Audio replacement with synchronization
#        ✓ Multiple language support
#        ✓ Timestamp-based processing
#        ✓ Segment-wise translation
    
#     4. For Malayalam:
#        - Subtitles work reliably
#        - Audio dubbing may have limitations with gTTS
#        - Consider using subtitle option for better results
    
#     5. Output files:
#        - Original_video_final.mp4 (processed video)
#        - Original_video_subtitles.srt (subtitle file)
#        - Translated segments displayed in GUI
#     """)

# if __name__ == "__main__":
#     print_setup_instructions()
#     create_gui()
##########################################################################################

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