# Website Summarizer API

FastAPI service that:
- Scrapes readable content from a website using Playwright + Trafilatura
- Summarizes that content using a local Ollama model

## Tech Stack
- Python 3.12+
- FastAPI + Uvicorn
- Playwright (Chromium)
- Trafilatura
- Ollama Python SDK
- uv (package manager + runner)

## Project Structure
```text
website-summarizer/
|-- main.py
|-- pyproject.toml
|-- README.md
|-- .env.example
|-- LLM/
|   |-- __init__.py
|   `-- llm.py
|-- models/
|   |-- __init__.py
|   `-- summary_request.py
|-- router/
|   |-- __init__.py
|   `-- routes.py
`-- utilities/
		|-- __init__.py
		`-- scrapper.py
```

## Prerequisites
Install these first:
1. Python 3.12 or newer
2. uv: https://docs.astral.sh/uv/
3. Ollama: https://ollama.com/download

## Local Setup
1. Install dependencies:
```bash
uv sync
```

2. Install Playwright browser (Chromium):
```bash
uv run playwright install chromium
```

3. Copy environment file:
```bash
cp .env.example .env
```
On Windows PowerShell:
```powershell
Copy-Item .env.example .env
```

4. Pull and run an Ollama model locally (example: llama3):
```bash
ollama pull llama3
ollama run llama3
```

Keep the Ollama service running in the background.

## Required Keys / Environment Variables
This project does not require any external API key right now.

Supported env vars:
- `OLLAMA_MODEL` (optional): local model name to use for summaries.
	- Default: `llama3`

Example `.env`:
```env
OLLAMA_MODEL=llama3
```

## Run the API Locally
Start the FastAPI server:
```bash
uv run uvicorn main:app --reload
```

Server URLs:
- API root: `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`

## API Usage
Endpoint:
- `POST /summarize`

Request body:
```json
{
	"website_url": "https://example.com",
	"user_prompt": "Give me a short summary with key points"
}
```

Response:
```json
{
	"url": "https://example.com",
	"summary": "..."
}
```

## Push to GitHub
If this repo is not connected yet:
1. Initialize git (if needed):
```bash
git init
```
2. Create first commit:
```bash
git add .
git commit -m "Initial commit: website summarizer API"
```
3. Add your remote:
```bash
git remote add origin https://github.com/<your-username>/website-summarizer.git
```
4. Push:
```bash
git branch -M main
git push -u origin main
```

If remote already exists, just commit and push:
```bash
git add .
git commit -m "docs: setup and run instructions"
git push
```
