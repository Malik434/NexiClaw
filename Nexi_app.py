import gradio as gr
import requests

# --- YOU MUST PASTE YOUR ACTUAL ASI CLOUD KEY HERE ---
API_KEY = "YOUR-ASI-CLOUD-KEY-HERE"

# --- UPDATED: The correct ASI Cloud Hackathon Gateway ---
API_URL = "https://inference.asicloud.cudos.org/v1/chat/completions"

def extract_to_atomspace(transcript_text: str) -> str:
    if not transcript_text.strip():
        return "Error: Please enter a transcript."

    # Standard OpenAI-compatible Auth Headers
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        # Step 1: Qualitative Extraction (The Anti-Flattening Step)
        extraction_prompt = (
            "You are Nexi, a qualitative ethics researcher. Analyze the user transcript.\n"
            "1. Identify the core Local Context (e.g., geographic/cultural demographic).\n"
            "2. Extract specific Value Assertions made by the speaker.\n"
            "3. Identify systemic Frictions or power imbalances.\n"
            "Strictly avoid generic corporate safety jargon (e.g., 'stakeholder compliance'). "
            "Keep the terms descriptive of ground reality."
        )

        payload1 = {
            "model": "minimax/minimax-m3", # Use lowercase standard mapping if ASI requires it
            "messages": [
                {"role": "system", "content": extraction_prompt},
                {"role": "user", "content": transcript_text}
            ],
            "temperature": 0.15
        }

        resp1 = requests.post(API_URL, headers=headers, json=payload1)

        if resp1.status_code != 200:
            return f"API Error (Step 1): {resp1.status_code}\n{resp1.text}"

        extracted_analysis = resp1.json()['choices'][0]['message']['content'].strip()

        # Step 2: The AtomSpace Translation
        metta_prompt = (
            "You are a Hyperon MeTTa compiler. Translate the ethical analysis provided by the user into valid MeTTa AtomSpace expressions.\n"
            "Use the following symbolic schema rules:\n"
            "- Define Context nodes: (ContextNode \"Name\")\n"
            "- Define Value nodes: (ValueNode \"Name\")\n"
                        "- Define Value nodes: (ValueNode \"Name\")\n"
            "- Link Context to Value: (EvaluationLink (ContextNode \"A\") (ValueNode \"B\") (stv 1.0 0.9))\n"
            "- Represent systemic contradictions: (FrictionLink (ValueNode \"A\") (ConceptNode \"B\"))\n\n"
            "Ensure the output contains ONLY valid MeTTa code blocks. Do not flatten localized perspectives."
        )

        payload2 = {
            "model": "minimax/minimax-m3",
            "messages": [
                {"role": "system", "content": metta_prompt},
                {"role": "user", "content": extracted_analysis}
            ],
            "temperature": 0.1
        }

        resp2 = requests.post(API_URL, headers=headers, json=payload2)

        if resp2.status_code != 200:
            return f"API Error (Step 2): {resp2.status_code}\n{resp2.text}"

        return resp2.json()['choices'][0]['message']['content'].strip()

    except Exception as e:
        return f"System Error: {str(e)}"

# Build the Web Interface
with gr.Blocks() as demo:
    gr.Markdown("# NexiClaw: Phase 0 AtomSpace Ingestion")
    gr.Markdown("This interface bypasses traditional LLM flattening by utilizing a reflexive extraction pipeline to map raw qualitative interviews directly into structured OpenCog Hyperon (MeTTa) expressions.")

    with gr.Row():
        with gr.Column():
            input_text = gr.Textbox(
                label="Raw Interview Transcript",
                lines=15,
                placeholder="Paste the interview text here..."
            )
            submit_btn = gr.Button("Execute Reflexive Extraction", variant="primary")

        with gr.Column():
            output_code = gr.Textbox(
                label="Generated MeTTa Expressions (AtomSpace Ready)",
                lines=15
            )

    submit_btn.click(fn=extract_to_atomspace, inputs=input_text, outputs=output_code)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)