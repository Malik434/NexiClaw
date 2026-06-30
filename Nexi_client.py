from gradio_client import Client
from hyperon import MeTTa
import sys


def run_pipeline(file_path):
    try:
        with open(file_path, 'r') as f:
            transcript = f.read()
        
        print("Connecting to NexiClaw on Hugging Face...")
        client = Client("Malik434/NexiClaw")
        
        # We pass a generic context since we are reading a raw file
        result = client.predict(
            transcript_text=transcript,
            global_context="Autonomous OmegaClaw Ingestion Pass",
            api_name="/predict"
        )
        
        metta_code = result[1]
        print("Translation successful. Appending to local AtomSpace...")
        
        # Save to the target atomspace file
        target_atomspace = "/PeTTa/repos/OmegaClaw-Core/atomspace.metta"
        with open(target_atomspace, 'a') as atom_file:
            atom_file.write(f"\n\n; --- Autonomous NexiClaw Ingestion ---\n{metta_code}\n")
            
        print(f"Success! Atoms successfully injected into {target_atomspace}")
        
    except Exception as e:
        print(f"Pipeline Error: {e}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python nexiclaw_client.py <path_to_transcript>")
    else:
        run_pipeline(sys.argv[1])