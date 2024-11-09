import tkinter as tk
from tkinter import messagebox
from download_and_extract import download_youtube_video  # Remove extract_audio import
from separate_vocals import separate_vocals
from transcribe import transcribe_audio
from chunk_audio import chunk_audio
from utils.file_management import save_transcriptions_and_chunks
import os

class AudioProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Audio Processor")
        
        tk.Label(root, text="YouTube URL:").grid(row=0, column=0, padx=5, pady=5)
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.process_button = tk.Button(root, text="Process", command=self.process_video)
        self.process_button.grid(row=1, column=1, padx=5, pady=10)
        
        self.status_text = tk.Text(root, height=10, width=60, state='disabled')
        self.status_text.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

    def process_video(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Input Error", "Please enter a YouTube URL.")
            return
        self.update_status("Downloading video...")
        audio_path = download_youtube_video(url)  # Now this downloads and extracts the audio
        
        self.update_status("Separating vocals...")
        vocal_audio_path = separate_vocals(audio_path)

         # Check if vocal file was created successfully
        if not os.path.exists(vocal_audio_path):
            self.update_status("Error: Vocal-only file was not created.")
            return

        self.update_status("Transcribing audio...")
        transcription = transcribe_audio(vocal_audio_path)
        
        self.update_status("Chunking audio...")
        chunks = chunk_audio(vocal_audio_path, transcription["segments"])
        
        self.update_status("Saving transcription...")
        save_transcriptions_and_chunks(transcription, chunks)
        
        self.update_status("Processing complete.")

    def update_status(self, message):
        self.status_text.config(state='normal')
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.config(state='disabled')

root = tk.Tk()
app = AudioProcessorApp(root)
root.mainloop()
