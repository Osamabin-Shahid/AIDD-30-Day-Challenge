# Gemini CLI Spec for Quiz App (PDF Summarizer + Quiz Generator)

## Overview

This document defines the specification for a **Quiz App** built using **Gemini CLI**, **OpenAI Agents SDK**, **Streamlit**, and **PyPDF**. The app performs two main tasks:

1. **PDF Summarization** – User uploads a PDF → App extracts text using PyPDF → Gemini Agent produces a clean summary.
2. **Quiz Generation** – After summarization, user clicks **Create Quiz** → Agent reads the *original PDF*, not the summary → Generates MCQs or mixed-format quizzes.

---

## Features

### A. PDF Summarizer

* User uploads any PDF file.
* Text is extracted using **PyPDF** (PyPDF2 or pypdf recommended).
* Agent processes extracted text and returns:

  * Clean
  * Structured
  * Easy-to-understand summary
* Summary can be rendered in any UI style (card, block, container, etc.).

---

### B. Quiz Generator

* After getting the summary, user can click **Create Quiz**.
* The agent reads the **original full PDF text** for better quality output.
* It generates:

  * MCQs
  * Or mixed‑style quizzes (MCQs + short answers + true/false)

---

## Required Libraries

Make sure these are installed:

```bash
pip install streamlit pypdf
pip install openai-agents
```

---

## Folder Structure (Suggested)

```
project/
│── app.py
│── agent_tools/
│     ├── pdf_reader.py
│     ├── quiz_generator.py
│── uploads/
│── gemini.md
```

---

## Gemini CLI Expected Prompting Logic

Below is the **command specification** for `gemini.md` inside Gemini CLI:

### 1. Extract PDF Text

```python
from pypdf import PdfReader

def extract_pdf_text(file_path: str):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text
```

### 2. Run PDF Summary Agent

* Agent should accept raw text.
* Agent generates a

  * clean
  * structured
  * student-friendly summary.

### 3. Run Quiz Generator Agent

* Input: **original PDF text only**.
* Output: JSON structure containing:

  * `mcqs: [ {question, options[], answer} ]`
  * Optional `mixed_questions: [...]`

---

## Streamlit App Logic

### Upload → Extract → Summarize

1. User uploads PDF.
2. Text extracted via PyPDF.
3. Summary agent is called.
4. Streamlit displays summary.

### Generate Quiz

1. User clicks **Generate Quiz**.
2. Quiz agent processes the original PDF text.
3. Streamlit displays quiz in card-style UI.

---

## Error Handling

* Missing PDF → Show warning.
* Corrupted file → Show error.
* Empty PDF text → Ask user to upload a proper document.
* Agent failing → Retry with shorter chunks.

---

## Debug Notes

* Always verify PDF text extraction before sending to agent.
* Handle long text by chunking.
* Streamlit may require session state to store original PDF text.

---

## Final Expected Output

* A working **Gemini CLI app** with:

  * PDF summarizer
  * Quiz generator
  * Clean UI in Streamlit
  * Fully integrated OpenAI Agents SDK

This spec can be copied directly into `gemini.md`.
