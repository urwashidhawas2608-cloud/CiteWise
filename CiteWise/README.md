# CiteWise — AI Citation Management Agent

A simple 3rd-year engineering project that analyzes a research paper, detects statements that may need citations, matches them to an included academic-source dataset, and generates IEEE/APA references.

## Features

- PDF/TXT upload
- Claim/sentence extraction
- Citation-need detection
- Academic source matching
- Relevance score
- IEEE and APA reference generation
- Citation coverage dashboard
- CSV export
- Agent activity log
- No API key required for the included demo

## Project structure

```text
CiteWise/
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── data/
│   ├── academic_sources.json
│   └── demo_research_paper.txt
└── src/
    ├── __init__.py
    ├── pipeline.py
    ├── search.py
    └── citations.py
```

## Run in VS Code

Open the `CiteWise` folder in VS Code.

### 1. Create a virtual environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run

```bash
streamlit run app.py
```

The terminal will show a local URL such as:

```text
http://localhost:8501
```

## Demo

Upload:

`data/demo_research_paper.txt`

Choose IEEE or APA and click **Analyze Paper**.

## Important academic-project note

The included JSON records are a **small demo dataset** for development/testing. They are not intended to be presented as a comprehensive scholarly database. For a final research-paper workflow, connect the search layer to a live academic metadata API and preserve the original metadata/DOI returned by that service.

## How the agent works

```text
Document
   ↓
Text extraction
   ↓
Claim detection
   ↓
Citation-need detection
   ↓
Academic-source retrieval
   ↓
Relevance matching
   ↓
Human review
   ↓
Citation formatting
   ↓
Reference list
```

## Future upgrade

The `src/search.py` module is intentionally isolated so it can later be replaced with:

- OpenAlex
- Crossref
- Semantic Scholar
- vector embeddings / FAISS
- an LLM-based claim verification step

without rewriting the Streamlit UI.
