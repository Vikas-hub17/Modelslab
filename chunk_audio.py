import librosa
import soundfile as sf
import os

def chunk_audio(audio_path, segments, video_title):
    """
    Splits the audio file into chunks based on timestamps and saves each chunk
    with a corresponding transcription file.
    """
    y, sr = librosa.load(audio_path, sr=None)  # Load audio file with original sample rate
    output_dir = os.path.join("output", video_title)
    os.makedirs(output_dir, exist_ok=True)

    chunk_files = []
    for i, segment in enumerate(segments):
        start_sample = int(segment["start"] * sr)
        end_sample = int(segment["end"] * sr)
        chunk_audio = y[start_sample:end_sample]
        
        # Define paths for the audio chunk and transcription file
        chunk_audio_path = os.path.join(output_dir, f"{video_title}_chunk_{i+1}.wav")
        chunk_text_path = os.path.join(output_dir, f"{video_title}_chunk_{i+1}.txt")
        
        # Save the audio chunk
        sf.write(chunk_audio_path, chunk_audio, sr)
        
        # Save the corresponding transcription text
        with open(chunk_text_path, "w") as f:
            f.write(segment["text"])
        
        chunk_files.append((chunk_audio_path, chunk_text_path))
    
    return chunk_files
