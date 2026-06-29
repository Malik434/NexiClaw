import gradio as gr
import requests
import os

# Secure API Key handling
# If testing locally, run: export ASI_API_KEY="your-key-here" before starting
API_KEY = os.getenv("ASI_API_KEY")
API_URL = "https://inference.asicloud.cudos.org/v1/chat/completions"

def chunk_text(text, chunk_size=3000, overlap=500):
    """Splits text into overlapping chunks based on character count."""
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        chunks.append(text[start:end])
        if end >= text_length:
            break
        start = end - overlap
    return chunks

def extract_to_atomspace(transcript_text: str, global_context: str):
    if not API_KEY:
        return "System Error: ASI_API_KEY environment variable not set.", ""
    if not transcript_text.strip():
        return "Error: Please enter a transcript.", ""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        # --- CAVEAT 1 & 2: Map Phase (Chunking with Global Context) ---
        # We process each chunk individually to prevent flattening
        chunks = chunk_text(transcript_text)
        all_extractions = []
        
        # Provide a default context if the user leaves it blank
        context_str = global_context.strip() if global_context.strip() else "Unknown context."

        for i, chunk in enumerate(chunks):
            extraction_prompt = (
                "You are Nexi, a qualitative ethics researcher. Analyze this specific chunk of an interview.\n"
                f"GLOBAL CONTEXT: {context_str}\n\n"
                "Task: Identify localized values, systemic frictions, and power imbalances in this text.\n"
                "Strictly avoid generic corporate safety jargon. Keep terms descriptive of ground reality."
            )

            payload1 = {
                "model": "minimax/minimax-m3", 
                "messages": [
                    {"role": "system", "content": extraction_prompt},
                    {"role": "user", "content": f"CHUNK {i+1}:\n{chunk}"}
                ],
                "temperature": 0.15
            }

            resp1 = requests.post(API_URL, headers=headers, json=payload1)
            if resp1.status_code != 200:
                return f"API Error in Chunk {i+1}: {resp1.status_code}\n{resp1.text}", ""
            
            chunk_result = resp1.json()['choices'][0]['message']['content'].strip()
            all_extractions.append(f"--- Chunk {i+1} Findings ---\n{chunk_result}")

        # Combine all findings into one master log
        combined_audit_log = "\n\n".join(all_extractions)

        # --- CAVEAT 3: Reduce Phase (Symbolic Consistency) ---
        # We pass ALL findings to a final synthesis prompt to generate unified MeTTa code
        metta_prompt = (
            "You are a Hyperon MeTTa compiler. I will provide a combined list of qualitative findings extracted from a large interview.\n"
            "Your task is to synthesize these into a single, cohesive MeTTa knowledge graph.\n\n"
            "CRITICAL SCHEMA RULES:\n"
            "1. Consolidate duplicates: If two chunks mention the same concept, use only ONE node for it. Ensure logical consistency.\n"
            "2. Define Context nodes: (ContextNode \"Name\")\n"
            "3. Define Value nodes: (ValueNode \"Name\")\n"
            "4. Link Context to Value: (EvaluationLink (ContextNode \"A\") (ValueNode \"B\") (stv 1.0 0.9))\n"
            "5. Represent systemic contradictions: (FrictionLink (ValueNode \"A\") (ConceptNode \"B\"))\n\n"
            "Output ONLY valid MeTTa code blocks. No introductory text."
        )

        payload2 = {
            "model": "minimax/minimax-m3",
            "messages": [
                {"role": "system", "content": metta_prompt},
                {"role": "user", "content": combined_audit_log}
            ],
            "temperature": 0.1
        }

        resp2 = requests.post(API_URL, headers=headers, json=payload2)
        if resp2.status_code != 200:
            return combined_audit_log, f"API Error (Stage 2): {resp2.status_code}\n{resp2.text}"
        
        final_metta = resp2.json()['choices'][0]['message']['content'].strip()

        return combined_audit_log, final_metta

    except Exception as e:
        return f"System Error: {str(e)}", ""

# Build the Web Interface
with gr.Blocks() as demo:
    gr.Markdown("# NexiClaw: Phase 0 AtomSpace Ingestion (Map-Reduce Architecture)")
    gr.Markdown("This interface handles large transcripts by chunking data with overlap. **Stage 1 (Map)** extracts local friction from each chunk. **Stage 2 (Reduce)** synthesizes all findings into a logically consistent MeTTa graph.")

    with gr.Row():
        with gr.Column(scale=1):
            global_context_input = gr.Textbox(
                label="Global Context (Crucial for preventing Context Drift)",
                lines=2,
                placeholder="e.g., 'Speaker is Tariq, a multi-generational smallholder farmer in Punjab...'"
            )
            input_text = gr.Textbox(
                label="Raw Interview Transcript",
                lines=12,
                placeholder="Paste the large interview text here..."
            )
            submit_btn = gr.Button("Execute Reflexive Extraction", variant="primary")

        with gr.Column(scale=1):
            audit_log = gr.Textbox(
                label="Stage 1: Chunked Qualitative Audit Log",
                lines=17,
                placeholder="The LLM's chunk-by-chunk qualitative extraction will appear here..."
            )

        with gr.Column(scale=1):
            output_code = gr.Textbox(
                label="Stage 2: Synthesized MeTTa Expressions",
                lines=17,
                placeholder="The final compiled and deduplicated AtomSpace code will appear here..."
            )

    submit_btn.click(fn=extract_to_atomspace, inputs=[input_text, global_context_input], outputs=[audit_log, output_code])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)