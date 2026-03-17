---
title: AI Powered Blog Summary to Spoken Audio Converter
emoji: 🎙️
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

> [!CAUTION]
> **Note:** The metadata block above is required by Hugging Face Spaces for deployment. I cannot remove this from here because if I do so, the Hugging Face deployment will not work.

# 🎙️ AI-Powered Blog Summary to Spoken Audio Converter

Turn any blog post into a podcast episode in seconds. Paste a URL, and this app scrapes the content, summarizes it using AI agents, and converts it to natural-sounding speech — all in one click.

🌐 **Hosted on Hugging Face Spaces** — accessible directly in your browser with no setup required.

---

## 🖥️ Usage

1. Open the app in your browser at `http://localhost:7860` (or via Hugging Face Spaces)
2. Paste any blog post URL into the **Blog URL** field
3. Click **Generate Podcast**
4. Wait a few moments while the AI agents scrape, summarize, and narrate the content
5. Read the generated **Blog Summary** or listen to the **Podcast Audio** directly in the browser

https://github.com/user-attachments/assets/2a4b61f7-133e-4123-bcc5-617d077b5a74

---

## 📁 Project Structure

```
├── app.py                  # Gradio UI and main application entry point
├── blog_summarizer.py      # CrewAI agents, tasks, and crew orchestration
├── pyproject.toml          # Project metadata and dependencies
├── requirements.txt        # Pip-compatible dependencies (exported from uv)
├── Dockerfile              # Container configuration
└── .env                    # API keys (not committed to version control)
```
---

## 🚀 Features

- **Automated Web Scraping** — Uses Firecrawl to extract clean article content from any blog URL, filtering out ads and navigation clutter
- **Multi-Agent Summarization** — A CrewAI pipeline with two specialized agents (a Web Content Researcher and a Content Analyst) that work sequentially to produce high-quality, podcast-ready summaries
- **Text-to-Speech Conversion** — Converts summaries to natural audio using the ElevenLabs API
- **Simple Web Interface** — A clean Gradio UI that requires zero technical knowledge to use
- **Dockerized** — Ships as a Docker container for consistent, reproducible deployment
- **Deployed on Hugging Face Spaces** — No installation needed to try the app

---

## 🧱 Architecture

```
    User Input (URL)
          │
          ▼
┌─────────────────────┐
│   Gradio Frontend   │  ← Web UI on port 7860
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Blog Scraper Agent │  ← CrewAI Agent + Firecrawl Tool
│  (Web Researcher)   │
└─────────┬───────────┘
          │  Raw blog content
          ▼
┌─────────────────────┐
│ Summarizer Agent    │  ← CrewAI Agent + Gemini 2.5 Flash LLM
│ (Content Analyst)   │
└─────────┬───────────┘
          │  Podcast-ready summary
          ▼
┌─────────────────────┐
│   ElevenLabs TTS    │  ← Converts text to MP3 audio
└─────────┬───────────┘
          │
          ▼
   Summary + Audio Output
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| LLM | Google Gemini 2.5 Flash (via LiteLLM) |
| Agent Framework | CrewAI |
| Web Scraping | Firecrawl |
| Text-to-Speech | ElevenLabs |
| Frontend | Gradio |
| Containerization | Docker |
| Hosting | Hugging Face Spaces |

---

## 📋 Prerequisites

- Python 3.11
- Docker (optional, for containerized deployment)
- API keys for:
  - [Google Gemini](https://aistudio.google.com/) (`GEMINI_API_KEY`)
  - [Firecrawl](https://firecrawl.dev/) (`FIRECRAWL_API_KEY`)
  - [ElevenLabs](https://elevenlabs.io/) (`ELEVENLABS_API_KEY`)

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/AI-Powered-Blog-Summary-to-Spoken-Audio-Converter.git
cd AI-Powered-Blog-Summary-to-Spoken-Audio-Converter
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
FIRECRAWL_API_KEY=your_firecrawl_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

### 3. Install Dependencies

Dependencies are managed with `uv`. To export them to a `requirements.txt` (e.g. for Hugging Face Spaces or Docker), run the following command in PowerShell:

```powershell
uv export --format requirements-txt | Set-Content -Encoding UTF8 requirements.txt
```

This generates a clean `requirements.txt` without hash pins, encoded in UTF-8.

Then install with pip:

```bash
pip install -r requirements.txt
```

Or install directly using uv:

```bash
pip install uv
uv sync
```

---

## ▶️ Running the App

### Option A: Local

> ⚠️ **Before running locally**, update the last line in `app.py`. Replace:
> ```python
> if __name__ == "__main__":
>     demo.launch(server_name="0.0.0.0", server_port=7860, theme="soft")
> ```
> with:
> ```python
> if __name__ == "__main__":
>     demo.launch(theme="soft")
> ```
> The `server_name` and `server_port` settings are intended for Docker/Hugging Face Spaces deployment and are not needed for local use.

```bash
python app.py
```

Then open your browser at `http://localhost:7860`.

### Option B: Docker

```bash
# Build the image
docker build -t blog-to-podcast .

# Run the container
docker run -p 7860:7860 --env-file .env blog-to-podcast
