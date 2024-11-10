import os
import subprocess
import glob

def separate_vocals(audio_path):
    # Ensure the output directory exists
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Run Demucs command
    command = [
        "demucs",
        "--two-stems=vocals",  # Separate vocals only
        "-o", output_dir,       # Output directory
        audio_path
    ]

    try:
        # Execute Demucs command
        subprocess.run(command, check=True)

        # Search for the separated vocals file in the output directory
        # Demucs typically creates a subdirectory named after the audio file
        audio_basename = os.path.splitext(os.path.basename(audio_path))[0]
        expected_vocal_path_pattern = os.path.join(output_dir, audio_basename, "vocals.wav")
        vocal_files = glob.glob(expected_vocal_path_pattern)
        
        if vocal_files:
            vocal_output_path = os.path.join(output_dir, "vocals.wav")
            os.rename(vocal_files[0], vocal_output_path)  # Rename for consistency
            return vocal_output_path
        else:
            raise FileNotFoundError("Expected vocal output file was not created by Demucs.")
    
    except subprocess.CalledProcessError as e:
        print(f"Error during vocal separation: {e}")
        raise e
