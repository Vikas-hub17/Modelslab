import os
import subprocess

def separate_vocals(audio_path):
    # Ensure the output directory exists
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Path for the vocal-only output
    vocal_output_path = os.path.join(output_dir, "vocal_only.wav")

    # Example command for Demucs (make sure Demucs is installed and configured correctly)
    # Adjust the command if you're using a specific Demucs installation or model.
    command = [
        "demucs",
        "--two-stems=vocals",  # Separate vocals only
        "-o", output_dir,
        audio_path
    ]

    try:
        # Run Demucs as a subprocess
        subprocess.run(command, check=True)
        
        # Check if Demucs created the expected output
        # Demucs typically outputs a directory structure, adjust path as needed
        demucs_output_folder = os.path.join(output_dir, os.path.splitext(os.path.basename(audio_path))[0])
        expected_vocal_path = os.path.join(demucs_output_folder, "vocals.wav")
        
        # Rename or copy the separated vocals to "vocal_only.wav" for consistency
        if os.path.exists(expected_vocal_path):
            os.rename(expected_vocal_path, vocal_output_path)
            return vocal_output_path
        else:
            raise FileNotFoundError("Expected vocal output file was not created by Demucs.")
    
    except subprocess.CalledProcessError as e:
        print(f"Error during vocal separation: {e}")
        raise e
