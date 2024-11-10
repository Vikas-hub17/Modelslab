import tkinter as tk
from tkinter import messagebox, filedialog
import os
import shutil
from download_and_extract import download_youtube_video
from separate_vocals import separate_vocals
from transcribe import transcribe_audio
from chunk_audio import chunk_audio
from utils.file_management import save_transcriptions_and_chunks

class AudioProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Audio Processor")

        # Input field for YouTube URL
        tk.Label(root, text="YouTube URL:").grid(row=0, column=0, padx=5, pady=5)
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)

        # Process and Reset buttons
        self.process_button = tk.Button(root, text="Process", command=self.process_video)
        self.process_button.grid(row=1, column=1, padx=5, pady=10)
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_app)
        self.reset_button.grid(row=1, column=0, padx=5, pady=10)

        # Status display area
        self.status_text = tk.Text(root, height=15, width=70, state='disabled', bg="#f4f4f4")
        self.status_text.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        # Open output folder button
        self.open_output_button = tk.Button(root, text="Open Output Folder", command=self.open_output_folder, state='disabled')
        self.open_output_button.grid(row=3, column=1, pady=5)

        # Create output directory
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)

    def update_status(self, message):
        """ Update the status text area with a new message. """
        self.status_text.config(state='normal')
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state='disabled')

    def reset_app(self):
        """ Reset the application to allow for a new YouTube URL input. """
        self.url_entry.delete(0, tk.END)
        self.status_text.config(state='normal')
        self.status_text.delete(1.0, tk.END)
        self.status_text.config(state='disabled')
        self.open_output_button.config(state='disabled')
        # Clear output directory for fresh start
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir)
        self.update_status("Application reset. Ready for a new video URL.")

    def open_output_folder(self):
        """ Open the output folder in the file explorer. """
        if os.path.exists(self.output_dir):
            filedialog.askopenfilename(initialdir=self.output_dir)

    def process_video(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Input Error", "Please enter a YouTube URL.")
            return
        
        try:
            # Step 1: Download and Extract Audio
            self.update_status("Downloading video...")
            audio_path = download_youtube_video(url)
            
            # Step 2: Separate Vocals
            self.update_status("Separating vocals...")
            vocal_audio_path = separate_vocals(audio_path)
            
            # Step 3: Transcribe Audio with Whisper
            self.update_status("Transcribing audio...")
            video_title = os.path.splitext(os.path.basename(audio_path))[0]
            segments = transcribe_audio(vocal_audio_path)
            
            # Step 4: Chunk Audio Based on Timestamps
            self.update_status("Chunking audio and saving transcriptions...")
            chunk_files = chunk_audio(vocal_audio_path, segments, video_title)
            
            # Notify user of completion
            self.update_status("Processing complete. All files saved in 'output' directory.")
            self.open_output_button.config(state='normal')
        
        except Exception as e:
            self.update_status(f"Error during processing: {str(e)}")
            messagebox.showerror("Processing Error", f"An error occurred: {e}")

root = tk.Tk()
app = AudioProcessorApp(root)
root.mainloop()
