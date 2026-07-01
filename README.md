# NexiClaw

NexiClaw is a Gradio-based transcript ingestion tool that extracts qualitative findings from interview text and compiles them into MeTTa expressions for AtomSpace-style knowledge graphs.

The app uses a two-stage map-reduce workflow:

1. Split long transcripts into overlapping chunks.
2. Extract localized values, frictions, and power imbalances from each chunk.
3. Synthesize the chunk findings into consolidated MeTTa graph expressions.

## Project Structure

```text
.
|-- Nexi_app.py                 # Main Gradio web app
|-- Nexi_client.py              # Client script for hosted NexiClaw ingestion
|-- c.py                        # Lightweight client script targeting /tmp/atomspace.metta
|-- interview.text              # Sample transcript/input text
|-- nexiclaw-presentation.html  # Project presentation
|-- pipeline_fix.md             # Notes for pipeline setup and recovery
|-- .env                        # Local environment variables, not committed
`-- .gitignore
```

## Requirements

- Python 3.10 or newer
- An ASI Cloud-compatible API key
- Python packages:
  - `gradio`
  - `requests`
  - `gradio_client`
  - `hyperon` if using `Nexi_client.py`

Install the core dependencies:

```bash
pip install gradio requests gradio_client
```

Install `hyperon` only if you need the local Hyperon client workflow:

```bash
pip install hyperon
```

## Configuration

`Nexi_app.py` reads the API key from the `API` environment variable:

```bash
export API="your-api-key"
```

On Windows PowerShell:

```powershell
$env:API = "your-api-key"
```

Keep secrets in `.env` or your deployment environment. Do not hardcode API keys in source files.

## Running the Web App

Start the Gradio interface:

```bash
python Nexi_app.py
```

The app launches on port `7860` and is configured with `share=True`, so Gradio may create a public share URL.

In the interface:

1. Enter a global context for the transcript.
2. Paste the raw interview transcript.
3. Run the extraction.
4. Review the chunked qualitative audit log and synthesized MeTTa output.

## Running the Client Scripts

Use `c.py` to call the hosted Hugging Face Space and append generated MeTTa code to `/tmp/atomspace.metta`:

```bash
python c.py interview.text
```

Use `Nexi_client.py` to append generated MeTTa code to the OmegaClaw AtomSpace path configured in the script:

```bash
python Nexi_client.py interview.text
```

Before using `Nexi_client.py`, confirm this target path exists and is writable:

```text
/PeTTa/repos/OmegaClaw-Core/atomspace.metta
```

## Notes for Maintainers

- `chunk_text` uses overlapping character windows to reduce context loss across long transcripts.
- `extract_to_atomspace` returns both the Stage 1 audit log and Stage 2 MeTTa code for reviewability.
- The API model is currently configured as `minimax/minimax-m3`.
- Client scripts depend on the hosted Space endpoint `Malik434/NexiClaw`.
- Validate generated MeTTa output before importing it into production knowledge stores.

## Security

- Never commit `.env` files or API keys.
- Treat transcript data as sensitive unless explicitly confirmed otherwise.
- Review generated graph output before appending it to shared or production AtomSpace files.
