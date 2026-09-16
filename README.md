# Tokenizer Application

A small, stateless web tool that tokenizes text — pasted directly, or
extracted from an uploaded `.txt`/`.pdf` file — using `tiktoken`.

See [specs/001-tokenizer-app/quickstart.md](specs/001-tokenizer-app/quickstart.md)
for full validation scenarios. Quick version:

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

## Run the backend

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

## Run the frontend

In a second terminal:

```bash
cd frontend
export TOKENIZER_API_URL=http://localhost:8000
streamlit run app.py
```

Open the URL Streamlit prints (default `http://localhost:8501`).

## Frontend Overview

The Streamlit app (`frontend/app.py`) gives users a simple way to tokenize
text and inspect the result.

### Inputs

- **Encoding dropdown** — choose which `tiktoken` encoding to tokenize with.
  Supported encodings (defined in `backend/app/core/config.py`):
  - `cl100k_base` — used by GPT-3.5-turbo and GPT-4 (~100k vocab). General-purpose, good for English and code.
  - `o200k_base` — used by GPT-4o (~200k vocab). Larger vocabulary, more efficient for non-English text and special characters.
  - `p50k_base` — used by earlier GPT-3 models and Codex (~50k vocab). Well-tuned for code.
  - `r50k_base` — the original GPT-2/GPT-3 encoding (~50k vocab). Kept for legacy comparison.

  Picking a different encoding changes the "vocabulary" used to split text, so
  the same input can produce a different number of tokens depending on which
  one is selected.

- **Input mode (radio button)** — three choices: "Paste text", "Upload TXT
  file", "Upload PDF file".
  - Paste text mode shows a text area to type/paste directly into.
  - Upload modes show a file uploader restricted to `.txt` or `.pdf`.

- **Tokenize button** — sends the text/file and chosen encoding to the
  backend for processing.

### Output

- **Extracted Text** *(file uploads only)* — a read-only text area showing
  the raw text pulled from the uploaded file, before tokenization stats.

- **Statistics** — 5 metric tiles:

  | Tile | Meaning | Computation |
  |---|---|---|
  | Characters | Total character count | `len(text)` (includes spaces/newlines) |
  | Words | Total word count | `len(text.split())` (splits on whitespace) |
  | Tokens | Number of tokens produced | `len(enc.encode(text))` |
  | Tokens/Word | Average tokens per word | `token_count / word_count` (0.0 if no words) |
  | Tokens/Character | Average tokens per character | `token_count / character_count` (0.0 if empty) |

  Ratios are displayed rounded to 2 decimal places in the UI; the backend
  returns unrounded floats.

- **Tokens** — a line-by-line breakdown of every token produced, showing:
  - `#index` — its position in the sequence
  - **ID** — the numeric token ID from the tokenizer's vocabulary
  - **Decoded** — the actual text/substring that token represents

  Because tokenization uses Byte-Pair Encoding (BPE), token boundaries are
  not fixed-length — common words/substrings seen often during training
  become single tokens, while rare or unusual text (like uncommon names) gets
  broken into smaller pieces, sometimes down to individual characters.

## Run tests

```bash
cd backend
pytest
```
