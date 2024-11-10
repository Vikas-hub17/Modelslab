import whisper

def transcribe_audio(audio_path):
    """
    Transcribes audio and returns a list of segments with timestamps.
    Each segment includes the text, start time, and end time.
    """
    model = whisper.load_model("base")  # Choose model size as needed (base, small, medium, large)
    result = model.transcribe(audio_path)
    
    segments = []
    for segment in result['segments']:
        segments.append({
            "start": segment["start"],  # Start time in seconds
            "end": segment["end"],      # End time in seconds
            "text": segment["text"]     # Transcribed text
        })
    
    return segments
