# Transcript Insights

AI-powered call transcript analyzer for pharmacy benefits management.

**[Live Demo](https://transcript-insights.streamlit.app)** ← Try it out!

## Features

- Upload call transcripts
- Generate actionable insights with Azure OpenAI
- Extract summaries, action items, sentiment, and escalation risk
- Export results as JSON

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

Create `.streamlit/secrets.toml`:
```toml
AOAI_VERSION = "2024-08-01-preview"
AOAI_KEY = "<your-key>"
AOAI_ENDPOINT = "https://<your-resource>.openai.azure.com/"
```

Create `.streamlit/config.toml`:
```toml
[client]
showSidebarNavigation = false
```

## Usage

1. Upload a `.txt` transcript file
2. Click "Analyze"
3. Review insights and export as JSON

## Tech Stack

- Python 3.12
- Streamlit
- Azure OpenAI (GPT-4o-mini)
- Pydantic for structured outputs

## Use Case

Built for automating call center documentation in PBM environments. Reduces agent workload and surfaces actionable insights from customer service calls.