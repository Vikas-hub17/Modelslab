import librosa
import soundfile as sf

def chunk_audio(audio_path, timestamps):
    y, sr = librosa.load(audio_path)
    chunks = []
    for i, segment in enumerate(timestamps):
        start_sample = int(segment['start'] * sr)
        end_sample = int(segment['end'] * sr)
        chunk = y[start_sample:end_sample]
        chunk_path = f"output/chunk_{i}.wav"
        sf.write(chunk_path, chunk, sr)
        chunks.append(chunk_path)
    return chunks
