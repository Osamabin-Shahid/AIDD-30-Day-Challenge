# 🤖 OpenAI Agents Quiz App Project Specification

**Goal:** Create a complete, multi-file Streamlit application that uses the **OpenAI Agents SDK** (via the `agents` library) and **PyPDF** for PDF Summarization and Quiz Generation.

## ⚠️ Key Constraint: Asynchronous Execution (Async)

The `openai-agents` SDK relies on `asyncio`. The `app.py` file **must** use `asyncio.run()` or a similar helper function to correctly call the asynchronous agent functions within the synchronous Streamlit environment.

## 📁 Project Structure Requirements

The code must respect the following file structure. Create the necessary files and the directory:
project/ │── app.py │── agent_tools/ │     ├── pdf_reader.py │     ├── quiz_generator.py │── uploads/ # Create this directory for temporary file storage

## 🛠️ Required Libraries

The code must assume the following dependencies are installed:
```bash
pip install streamlit pypdf openai-agents
# Note: Assume GEMINI_API_KEY is available in the environment.

📝 File 1: agent_tools/pdf_reader.py
Create a utility module with one function:
from pypdf import PdfReader

def extract_pdf_text(file_path: str) -> str:
    """Extracts all text from a given PDF file path."""
    # Implementation should use PdfReader to iterate through pages and safely
    # concatenate text. Returns the raw, combined text string.
    # Handle potential None returns from extract_text() by using 'or ""'.
    Zaroor, bhai! Aap ne jo detailed specification di thi, usko OpenAI Agents SDK ke mutabiq use karne ke liye, yeh raha woh complete prompt jise aap seedhe gemini.md file mein paste kar sakte hain.

Yeh prompt aapke Streamlit Quiz App ke liye teenon files (app.py, pdf_reader.py, aur quiz_generator.py) generate karega.

Markdown

# 🤖 OpenAI Agents Quiz App Project Specification

**Goal:** Create a complete, multi-file Streamlit application that uses the **OpenAI Agents SDK** (via the `agents` library) and **PyPDF** for PDF Summarization and Quiz Generation.

## ⚠️ Key Constraint: Asynchronous Execution (Async)

The `openai-agents` SDK relies on `asyncio`. The `app.py` file **must** use `asyncio.run()` or a similar helper function to correctly call the asynchronous agent functions within the synchronous Streamlit environment.

## 📁 Project Structure Requirements

The code must respect the following file structure. Create the necessary files and the directory:

project/ │── app.py │── agent_tools/ │     ├── pdf_reader.py │     ├── quiz_generator.py │── uploads/ # Create this directory for temporary file storage


## 🛠️ Required Libraries

The code must assume the following dependencies are installed:
```bash
pip install streamlit pypdf openai-agents
# Note: Assume OPENAI_API_KEY is available in the environment.
📝 File 1: agent_tools/pdf_reader.py
Create a utility module with one function:

Python

from pypdf import PdfReader

def extract_pdf_text(file_path: str) -> str:
    """Extracts all text from a given PDF file path."""
    # Implementation should use PdfReader to iterate through pages and safely
    # concatenate text. Returns the raw, combined text string.
    # Handle potential None returns from extract_text() by using 'or ""'.
📝 File 2: agent_tools/quiz_generator.py
Create a module containing two asynchronous functions that interact with the OpenAI Agents SDK:

1. async def run_summary_agent(raw_text: str) -> str
Imports: Must import Agent and Runner from the agents library.

Agent Definition: Define a focused Agent (e.g., "SummaryAgent") with instructions to:

Take the raw text.
Produce a clean, structured, and student-friendly summary.

Execution: Use await Runner.run(...) to execute the agent.

Model: Use a suitable OpenAI model (e.g., gpt-4o-mini).

2. async def run_quiz_generator_agent(full_pdf_text: str) -> str
Agent Definition: Define a focused Agent (e.g., "QuizAgent") instructed to:

Read the provided full_pdf_text.

Generate a mixed-style quiz (MCQs, short answers, true/false).

Output Constraint: The agent must be instructed to return the output strictly as a JSON string conforming to this schema for easy parsing:

{
  "questions": [
    {
      "id": 1,
      "type": "mcq",
      "question": "...",
      "options": ["...", "..."],
      "answer": "..."
    },
    // Include types like 'short_answer' and 'true_false' in the generated quiz structure.
  ]
}
Zaroor, bhai! Aap ne jo detailed specification di thi, usko OpenAI Agents SDK ke mutabiq use karne ke liye, yeh raha woh complete prompt jise aap seedhe gemini.md file mein paste kar sakte hain.

Yeh prompt aapke Streamlit Quiz App ke liye teenon files (app.py, pdf_reader.py, aur quiz_generator.py) generate karega.

Markdown

# 🤖 OpenAI Agents Quiz App Project Specification

**Goal:** Create a complete, multi-file Streamlit application that uses the **OpenAI Agents SDK** (via the `agents` library) and **PyPDF** for PDF Summarization and Quiz Generation.

## ⚠️ Key Constraint: Asynchronous Execution (Async)

The `openai-agents` SDK relies on `asyncio`. The `app.py` file **must** use `asyncio.run()` or a similar helper function to correctly call the asynchronous agent functions within the synchronous Streamlit environment.

## 📁 Project Structure Requirements

The code must respect the following file structure. Create the necessary files and the directory:

project/ │── app.py │── agent_tools/ │     ├── pdf_reader.py │     ├── quiz_generator.py │── uploads/ # Create this directory for temporary file storage


## 🛠️ Required Libraries

The code must assume the following dependencies are installed:
```bash
pip install streamlit pypdf openai-agents
# Note: Assume OPENAI_API_KEY is available in the environment.
📝 File 1: agent_tools/pdf_reader.py
Create a utility module with one function:

Python

from pypdf import PdfReader

def extract_pdf_text(file_path: str) -> str:
    """Extracts all text from a given PDF file path."""
    # Implementation should use PdfReader to iterate through pages and safely
    # concatenate text. Returns the raw, combined text string.
    # Handle potential None returns from extract_text() by using 'or ""'.
📝 File 2: agent_tools/quiz_generator.py
Create a module containing two asynchronous functions that interact with the OpenAI Agents SDK:

1. async def run_summary_agent(raw_text: str) -> str
Imports: Must import Agent and Runner from the agents library.

Agent Definition: Define a focused Agent (e.g., "SummaryAgent") with instructions to:

Take the raw text.

Produce a clean, structured, and student-friendly summary.

Execution: Use await Runner.run(...) to execute the agent.

Model: Use a suitable OpenAI model (e.g., gpt-4o-mini).

2. async def run_quiz_generator_agent(full_pdf_text: str) -> str
Agent Definition: Define a focused Agent (e.g., "QuizAgent") instructed to:

Read the provided full_pdf_text.

Generate a mixed-style quiz (MCQs, short answers, true/false).

Output Constraint: The agent must be instructed to return the output strictly as a JSON string conforming to this schema for easy parsing:

JSON

{
  "questions": [
    {
      "id": 1,
      "type": "mcq",
      "question": "...",
      "options": ["...", "..."],
      "answer": "..."
    },
    // Include types like 'short_answer' and 'true_false' in the generated quiz structure.
  ]
}
📝 File 3: app.py (Streamlit UI and Logic)
Create the main Streamlit application logic:

1. Setup and Imports
Import streamlit, os, json, and asyncio.

Import functions from agent_tools/pdf_reader.py and agent_tools/quiz_generator.py.

Define a helper function: def run_async(coro): return asyncio.run(coro) to execute agent calls.

Use Streamlit Session State (st.session_state) to store the original_pdf_text.

2. Upload → Extract → Summarize Logic
Use st.file_uploader for PDF files.

On File Upload: a. Save the file temporarily (into the uploads/ directory). b. Extract raw text via extract_pdf_text(). c. Store raw text in session state (st.session_state['original_pdf_text']). d. Use the run_async wrapper to call run_summary_agent() and display the result.

3. Generate Quiz Logic
Display the "Generate Quiz" button, conditional on the text being in session state.

On Button Click: a. Call the run_async wrapper for run_quiz_generator_agent(), passing the stored original_pdf_text. b. Parse the JSON output string received from the agent. c. Display the quiz using clean, card-style UI elements (e.g., using st.expander or st.info).

4. Error Handling
Implement robust error handling for:

File corruption/Empty PDF.

JSON parsing failure (if agent returns bad JSON).

Use appropriate Streamlit messages (st.warning, st.error).

END OF COMPLETE PROJECT SPECIFICATION. Generate the complete Python code for all three files (app.py, agent_tools/pdf_reader.py, and agent_tools/quiz_generator.py) based on this specification.