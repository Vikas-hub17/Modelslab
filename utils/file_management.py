import os

def save_transcriptions_and_chunks(transcription, chunks):
    for i, segment in enumerate(transcription["segments"]):
        text = segment["text"]
        chunk_path = chunks[i]
        txt_path = chunk_path.replace(".wav", ".txt")
        with open(txt_path, "w") as f:
            f.write(text)
