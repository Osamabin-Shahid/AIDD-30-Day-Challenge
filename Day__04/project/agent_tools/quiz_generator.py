import os
from agents import Agent, Runner, RunConfig

async def run_summary_agent(raw_text: str) -> str:
    summary_agent = Agent(
        "SummaryAgent",
        "You are a helpful assistant that summarizes text. Your goal is to produce a clean, structured, and student-friendly summary of the provided text."
    )
    result = await Runner.run(summary_agent, raw_text, run_config=RunConfig(model="gemini-pro"))
    return result.final_output

async def run_quiz_generator_agent(full_pdf_text: str) -> str:
    quiz_agent = Agent(
        "QuizAgent",
        """You are a quiz generation expert. Your task is to read the provided text and generate a mixed-style quiz with multiple-choice questions (MCQs), short-answer questions, and true/false questions.

        Your output MUST be a JSON string that conforms to the following schema:
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
    result = await Runner.run(quiz_agent, full_pdf_text, run_config=RunConfig(model="gemini-pro"))
    return result.final_output