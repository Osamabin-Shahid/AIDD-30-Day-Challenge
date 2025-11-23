from agents import Agent, function_tool
import os
import json
import streamlit as st # To access st.secrets or os.getenv

# Function to get API key from .env or environment variable
def get_api_key():
    return os.getenv("GEMINI_API_KEY")

class QuizGeneratorAgent:
    def __init__(self):
        api_key = get_api_key() # Get API key, but it's not directly passed to Agent constructor
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found. Please set it in .env or Streamlit secrets.")
        
        self.agent = Agent(
            # 'name' and 'description' are not direct parameters for this Agent constructor
            # 'api_key' is also not a direct parameter; the 'agents' library should pick it up from env
            model="gemini-2.5-flash", 
            tools=[], # No specific tools for this initial version, can add later for more complex logic
            instructions="You are an expert quiz generator. Your goal is to create a structured quiz in JSON format from the provided text."
        )

    def generate_quiz(self, text: str) -> dict:
        # Ensure the text is not too long for the model.
        # This will need proper chunking for very long texts.
        if len(text) > 10000: # Example limit, adjust as per model context window
            text = text[:10000] + "..."
            st.warning("Input text truncated for quiz generation due to length.")

        prompt = f"""
        Generate a quiz from the following text. The quiz should include multiple-choice questions (MCQs) and can optionally include other types of questions (e.g., short answers, true/false).

        The output MUST be a JSON object with a single key 'mcqs'. The value of 'mcqs' should be a list of MCQ objects. Each MCQ object MUST have the following structure:
        {{
            "question": "The question text",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "Correct Option Text"
        }}

        Example:
        {{
            "mcqs": [
                {{
                    "question": "What is the capital of France?",
                    "options": ["Berlin", "Madrid", "Paris", "Rome"],
                    "answer": "Paris"
                }},
                {{
                    "question": "Which planet is known as the Red Planet?",
                    "options": ["Earth", "Mars", "Jupiter", "Venus"],
                    "answer": "Mars"
                }}
            ]
        }}

        Text to generate quiz from:
        {text}
        """

        response = self.agent.run(prompt)
        
        try:
            quiz_data = json.loads(response.content)
            # Basic validation to ensure it's a dict with 'mcqs' key
            if isinstance(quiz_data, dict) and "mcqs" in quiz_data:
                return quiz_data
            else:
                raise ValueError("Generated JSON does not contain the 'mcqs' key or is not a valid structure.")
        except json.JSONDecodeError:
            raise ValueError("Agent did not return a valid JSON format for the quiz.")
        except Exception as e:
            raise ValueError(f"Error parsing quiz data: {e}")

if __name__ == "__main__":
    # Example usage (for testing)
    sample_text = "The quick brown fox jumps over the lazy dog. The dog was very lazy. Cats are also known to be lazy at times. Birds fly in the sky."
    
    try:
        quiz_generator = QuizGeneratorAgent()
        quiz = quiz_generator.generate_quiz(sample_text)
        print("Generated Quiz:")
        print(json.dumps(quiz, indent=2))
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")