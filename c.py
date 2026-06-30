import sys
from gradio_client import Client

def run_pipeline(file_path):
    try:
        with open(file_path, "r") as f:
            transcript = f.read()
        print("Connecting to NexiClaw API...")
        client = Client("Malik434/NexiClaw")
        
        result = client.predict(
            transcript_text=transcript,
            global_context="Autonomous OmegaClaw Ingestion",
            api_name="/predict"
        )
        
        target = "/tmp/atomspace.metta"
        with open(target, "a") as f_out:
            f_out.write("\n\n; --- Autonomous NexiClaw Ingestion ---\n" + result[1] + "\n")
            
        print("Success! Atoms injected into " + target)
        
    except Exception as e:
        print("Pipeline Error: " + str(e))

if __name__ == "__main__":
    run_pipeline(sys.argv[1])