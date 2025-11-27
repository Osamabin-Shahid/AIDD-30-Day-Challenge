import streamlit as st
import os
import json
import asyncio
<<<<<<< HEAD
from agent_tools.pdf_reader import extract_pdf_text
from agent_tools.quiz_generator import run_summary_agent, run_quiz_generator_agent

# Helper function to run asyncio coroutines
def run_async(coro):
    return asyncio.run(coro)

# --- Streamlit UI ---
st.title("📄 PDF Summarizer and Quiz Generator")

# Initialize session state
if 'original_pdf_text' not in st.session_state:
    st.session_state['original_pdf_text'] = ""

# --- PDF Upload and Text Extraction ---
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Save the file temporarily
    uploads_dir = "uploads"
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    
    file_path = os.path.join(uploads_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File '{uploaded_file.name}' uploaded successfully!")

    # --- Text Extraction and Summarization ---
    with st.spinner("Extracting text from PDF..."):
        try:
            raw_text = extract_pdf_text(file_path)
            st.session_state['original_pdf_text'] = raw_text
            if not raw_text.strip():
                st.warning("The PDF seems to be empty or contains no extractable text.")
            else:
                st.text_area("Extracted Text", raw_text, height=200)

                with st.spinner("Generating summary..."):
                    summary = run_async(run_summary_agent(raw_text))
                    st.subheader("📝 Summary")
                    st.write(summary)

        except Exception as e:
            st.error(f"An error occurred during text extraction or summarization: {e}")

# --- Quiz Generation ---
if st.session_state['original_pdf_text']:
    if st.button("✨ Generate Quiz"):
        with st.spinner("Generating quiz... This may take a moment."):
            try:
                quiz_json_str = run_async(run_quiz_generator_agent(st.session_state['original_pdf_text']))
                
                # Attempt to parse the JSON
                try:
                    quiz_data = json.loads(quiz_json_str)
                    questions = quiz_data.get("questions", [])

                    if not questions:
                        st.warning("The generated quiz has no questions. The agent might have returned an empty list.")
                        st.json(quiz_json_str) # Show the raw JSON for debugging
                    else:
                        st.subheader("🧠 Here's Your Quiz!")
                        for q in questions:
                            with st.expander(f"Question {q['id']}: {q['question']}"):
                                if q['type'] == 'mcq':
                                    st.radio("Options", q['options'], key=f"q_{q['id']}")
                                elif q['type'] == 'short_answer':
                                    st.text_input("Your Answer", key=f"q_{q['id']}")
                                elif q['type'] == 'true_false':
                                    st.radio("True or False?", ["True", "False"], key=f"q_{q['id']}")
                                
                                if st.button("Show Answer", key=f"ans_{q['id']}"):
                                    st.info(f"Correct Answer: {q['answer']}")
                
                except json.JSONDecodeError:
                    st.error("Failed to parse the quiz JSON. The agent may have returned a malformed response.")
                    st.text_area("Raw Agent Output (Invalid JSON)", quiz_json_str, height=150)

            except Exception as e:
                st.error(f"An error occurred during quiz generation: {e}")
else:
    st.info("Upload a PDF to get started.")

st.sidebar.header("About")
st.sidebar.info(
    "This app uses AI agents to summarize PDF documents and generate quizzes from them. "
    "Upload your PDF, and the app will extract the text, provide a summary, and create a quiz."
)
st.sidebar.markdown(
    "**Note:** Ensure your `GEMINI_API_KEY` is set as an environment variable."
)
=======
from dotenv import load_dotenv
from agent_tools.pdf_reader import extract_pdf_text
from agent_tools.quiz_generator import run_summary_agent, run_quiz_generator_agent

load_dotenv()

# Ensure GEMINI_API_KEY is available as GOOGLE_API_KEY for openai-agents' google provider
if "GEMINI_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]

def run_async(coro):
    return asyncio.run(coro)

st.title("📄 PDF Summarizer and Quiz Generator")

# Create the uploads directory if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if "original_pdf_text" not in st.session_state:
    st.session_state.original_pdf_text = ""

if uploaded_file is not None:
    try:
        # Save the uploaded file to a temporary location
        file_path = os.path.join("uploads", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Extract text from the PDF
        st.session_state.original_pdf_text = extract_pdf_text(file_path)

        if st.session_state.original_pdf_text.strip():
            st.success("Successfully extracted text from the PDF.")

            # Display the summary
            with st.spinner("Generating summary..."):
                summary = run_async(run_summary_agent(st.session_state.original_pdf_text))
                st.subheader("Summary")
                st.write(summary)
        else:
            st.warning("Could not extract any text from the PDF. The file might be empty or scanned.")

    except Exception as e:
        st.error(f"An error occurred: {e}")


if st.session_state.original_pdf_text:
    if st.button("Generate Quiz"):
        with st.spinner("Generating quiz..."):
            try:
                quiz_json_str = run_async(run_quiz_generator_agent(st.session_state.original_pdf_text))
                quiz_data = json.loads(quiz_json_str)

                st.subheader("Quiz")
                for question in quiz_data["questions"]:
                    with st.expander(f"Question {question['id']}: {question['question']}"):
                        if question["type"] == "mcq":
                            options = question["options"]
                            st.radio("Options", options, key=f"q_{question['id']}")
                            if st.button("Show Answer", key=f"ans_{question['id']}"):
                                st.info(f"Correct Answer: {question['answer']}")
                        elif question["type"] == "short_answer":
                            st.text_input("Your Answer", key=f"q_{question['id']}")
                            if st.button("Show Answer", key=f"ans_{question['id']}"):
                                st.info(f"Correct Answer: {question['answer']}")
                        elif question["type"] == "true_false":
                            st.radio("True or False?", ["True", "False"], key=f"q_{question['id']}")
                            if st.button("Show Answer", key=f"ans_{question['id']}"):
                                st.info(f"Correct Answer: {question['answer']}")
            except json.JSONDecodeError:
                st.error("Failed to parse the quiz data. The agent might have returned an invalid JSON.")
            except Exception as e:
                st.error(f"An error occurred while generating the quiz: {e}")


# {	"mcpServers": {
# 		"context7": {
# 			"command": "npx",
# 			"args": [
# 				"-y",
# 				"@upstash/context7-mcp"
# 			],
# 			"env": {
# 				"CONTEXT7_API_KEY": "ctx7sk-6aa258d4-eebf-4bb9-bb16-82c56f977724"
# 			}
# 		}
# 	}


# }
>>>>>>> 539cafef22c343296a45d89a856cc310c4bc78d3
