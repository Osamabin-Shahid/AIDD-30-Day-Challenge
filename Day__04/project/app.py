import streamlit as st
import os
import json
import asyncio
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