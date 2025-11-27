# import os
# import sys

# # Specific, direct imports to avoid loading problematic 'agents.scripts' module.
# # These paths are educated guesses based on common library structures and error messages.
# from agents import Agent, Runner, RunConfig,set_tracing_disabled, OpenAIChatCompletionsModel

# set_tracing_disabled(True)  # Disable tracing to avoid issues with missing modules

# # --- API Key and Provider Configuration ---

# # Check for the API key in common environment variables.
# api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("OPENAI_API_KEY")
# base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# # If no key is found, print a helpful error message and exit.
# if not api_key:
#     sys.exit(
#         "ERROR: API key not found. Please set the GEMINI_API_KEY, GOOGLE_API_KEY, or OPENAI_API_KEY environment variable."
#     )

#     client = OpenAIChatCompletionsModel(
#         api_key=api_key,
#         base_url=base_url
#     )

# # Explicitly create a provider instance configured for Gemini's OpenAI-compatible endpoint.
# gemini_provider = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",  # Use the correct model identifier for the endpoint
#     openai_client=client,
#     # api_key=api_key,
#     # base_url=base_url
# )

# async def run_summary_agent(raw_text: str) -> str:
#     """
#     Runs an agent to generate a student-friendly summary of the provided text.
#     """
#     summary_agent = Agent(
#         "SummaryAgent",
#         "You are an expert in summarizing texts. Please provide a clean, structured, and student-friendly summary of the following text:",
#     )

#     run_config = RunConfig(
#         model="models/gemini-pro",  # Use the correct model identifier for the endpoint
#         model_provider=gemini_provider
#     )
#     result = await Runner.run(summary_agent, raw_text, run_config=run_config)
#     return str(result.final_output)

# async def run_quiz_generator_agent(full_pdf_text: str) -> str:
#     """
#     Runs an agent to generate a mixed-style quiz from the provided text,
#     outputting the result as a JSON string.
#     """
#     quiz_agent = Agent(
#         "QuizAgent",
#         """
#         You are an expert quiz creator. Based on the text below, generate a mixed-style quiz 
#         (including multiple-choice questions, short answers, and true/false).

#         The output must be a single, valid JSON string conforming to this exact schema:
#         {
#           "questions": [
#             {
#               "id": 1,
#               "type": "mcq",
#               "question": "...",
#               "options": ["...", "..."],
#               "answer": "..."
#             },
#             {
#               "id": 2,
#               "type": "short_answer",
#               "question": "...",
#               "answer": "..."
#             },
#             {
#               "id": 3,
#               "type": "true_false",
#               "question": "...",
#               "answer": "True" 
#             }
#           ]
#         }
#         """,
#     )
        
#     run_config = RunConfig(
#         model="models/gemini-pro", # Use the correct model identifier for the endpoint
#         model_provider=gemini_provider
#     )
#     result = await Runner.run(quiz_agent, full_pdf_text, run_config=run_config)
#     return str(result.final_output)
import os
import sys

# Correct imports
from agents import Agent, Runner, RunConfig,OpenAIProvider, set_tracing_disabled


# Disable tracing
set_tracing_disabled(True)

# --- API Key ---

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    sys.exit("ERROR: No API key found. Please set GEMINI_API_KEY.")

# --- Gemini OpenAI-Compatible Provider ---

gemini_provider = OpenAIProvider(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# -------------------------
# Summary Agent
# -------------------------

async def run_summary_agent(raw_text: str) -> str:
    summary_agent = Agent(
        "SummaryAgent",
        "You are an expert in summarizing texts. Provide a clean, structured summary of the following text:"
    )

    run_config = RunConfig(
        model="gemini-2.0-flash",      # Correct Gemini model
        model_provider=gemini_provider
    )

    result = await Runner.run(summary_agent, raw_text, run_config=run_config)
    return str(result.final_output)

# -------------------------
# Quiz Generator Agent
# -------------------------

async def run_quiz_generator_agent(full_pdf_text: str) -> str:
    quiz_agent = Agent(
        "QuizAgent",
        """
        You are an expert quiz creator. Based on the text below, generate a mixed-style quiz
        (multiple-choice, short-answer, true/false).

        Output must be a single JSON string:
        {
          "questions": [
            {
              "id": 1,
              "type": "mcq",
              "question": "...",
              "options": ["...", "..."],
              "answer": "..."
            },
            {
              "id": 2,
              "type": "short_answer",
              "question": "...",
              "answer": "..."
            },
            {
              "id": 3,
              "type": "true_false",
              "question": "...",
              "answer": "True"
            }
          ]
        }
        """
    )

    run_config = RunConfig(
        model="gemini-2.0-flash",
        model_provider=gemini_provider
    )

    result = await Runner.run(quiz_agent, full_pdf_text, run_config=run_config)
    return str(result.final_output)
