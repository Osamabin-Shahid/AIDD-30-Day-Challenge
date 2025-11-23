import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
from agent_tools.pdf_reader import extract_pdf_text
from agent_tools.summarizer_agent import SummarizerAgent
from agent_tools.quiz_generator_agent import QuizGeneratorAgent

# Ensure the uploads directory exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(layout="wide", page_title="Quiz App")

st.title("📄 Quiz App: PDF Summarizer & Quiz Generator")

# Initialize SummarizerAgent if not already in session state
if "summarizer" not in st.session_state:
    try:
        st.session_state["summarizer"] = SummarizerAgent()
    except ValueError as e:
        st.error(f"Configuration Error for Summarizer: {e}. Please set GEMINI_API_KEY.")
        st.stop() # Stop the app if API key is missing

# Initialize QuizGeneratorAgent if not already in session state
if "quiz_generator" not in st.session_state:
    try:
        st.session_state["quiz_generator"] = QuizGeneratorAgent()
    except ValueError as e:
        st.error(f"Configuration Error for Quiz Generator: {e}. Please set GEMINI_API_KEY.")
        st.stop() # Stop the app if API key is missing

# --- PDF Upload ---
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    # Save the uploaded file to the UPLOAD_DIR
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File '{uploaded_file.name}' uploaded successfully!")

    # Store the file path in session state
    st.session_state["pdf_file_path"] = file_path

    # Extract text from the PDF
    with st.spinner("Extracting text from PDF..."):
        pdf_text = extract_pdf_text(file_path)
    
    if pdf_text:
        st.session_state["full_pdf_text"] = pdf_text
        st.subheader("PDF Content Extracted!")
        st.write(f"First 500 characters: {pdf_text[:500]}...")
        st.success("Text extracted successfully. Now you can summarize or generate a quiz.")
    else:
        st.error("Could not extract text from the PDF. Please try another file.")
        st.session_state["full_pdf_text"] = None

else:
    st.info("Please upload a PDF file to get started.")
    st.session_state["pdf_file_path"] = None
    st.session_state["full_pdf_text"] = None

# Summarizer and Quiz Generator
if st.session_state.get("full_pdf_text"):
    st.sidebar.header("Actions")
    if st.sidebar.button("Summarize PDF"):
        with st.spinner("Generating summary..."):
            try:
                summary = st.session_state["summarizer"].summarize(st.session_state["full_pdf_text"])
                st.subheader("Summary")
                st.write(summary)
            except Exception as e:
                st.error(f"Error generating summary: {e}")

    if st.sidebar.button("Generate Quiz"):
        with st.spinner("Generating quiz..."):
            try:
                quiz_data = st.session_state["quiz_generator"].generate_quiz(st.session_state["full_pdf_text"])
                st.subheader("Generated Quiz")
                
                if "mcqs" in quiz_data and isinstance(quiz_data["mcqs"], list):
                    for i, mcq in enumerate(quiz_data["mcqs"]):
                        st.markdown(f"**Question {i+1}:** {mcq['question']}")
                        options_str = "\n".join([f"- {opt}" for opt in mcq['options']])
                        st.markdown(f"Options:\n{options_str}")
                        st.markdown(f"**Answer:** {mcq['answer']}")
                        st.markdown("---")
                else:
                    st.warning("Quiz data is not in the expected format (missing 'mcqs' key or 'mcqs' is not a list).")

            except Exception as e:
                st.error(f"Error generating quiz: {e}")
