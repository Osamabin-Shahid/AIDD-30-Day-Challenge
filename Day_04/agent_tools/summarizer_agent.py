from agents import Agent, function_tool, Runner
import os
import streamlit as st

# Function to get API key from .env or environment variable
def get_api_key():
    return os.getenv("GEMINI_API_KEY")

class SummarizerAgent:
    def __init__(self):
        api_key = get_api_key()
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found. Please set it in .env or Streamlit secrets.")
        
        self.agent = Agent(
            # 'name' and 'description' are not direct parameters for this Agent constructor in openai-agents SDK
            model="gemini-pro",
            tools=[],  # No specific tools needed for simple summarization
            instructions="You are an expert summarizer. Your goal is to create a clean, structured, and student-friendly summary of the provided text."
        )

    def summarize(self, text: str) -> str:
        # Ensure the text is not too long for the model.
        # This will need proper chunking for very long texts.
        if len(text) > 10000: # Example limit, adjust as per model context window
            text = text[:10000] + "..."
            st.warning("Input text truncated for summarization due to length.")

        response = self.agent.run(
            f"Please provide a clean, structured, and student-friendly summary of the following text:\n\n{text}"
        )
        return response.content

import os
from openai import OpenAI, Agent

class SummarizerAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found. Please set it in .env")

        # OpenAI client for Gemini endpoint
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        # Correct Agent import
        self.agent = Agent(
            model="gemini-1.5-flash",
            instructions="You are an expert summarizer. Provide clear, structured, student-friendly summaries."
        )

    def summarize(self, text: str) -> str:
        if len(text) > 10000:
            text = text[:10000] + "..."

        response = self.client.responses.create(
            model="gemini-1.5-flash",
            agent=self.agent,
            input=f"Summarize the following text:\n\n{text}"
        )

        return response.output_text


if __name__ == "__main__":
    # Example usage (for testing)
    sample_text = "This is a sample document that needs to be summarized. It contains several sentences and paragraphs. The main idea is about testing the summarization capability of an AI agent. The summary should be concise and capture the key points effectively. This part is extra and should also be summarized."
    
    try:
        summarizer = SummarizerAgent()
        summary = summarizer.summarize(sample_text)
        print("Generated Summary:")
        print(summary)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
