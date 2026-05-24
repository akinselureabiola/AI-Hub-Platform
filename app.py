"""
AI Career Assistant

Analyzes a resume against a job description and generates:

- Career analysis
- Tailored recruiter-ready resume
- Tailored recruiter-ready cover letter

All outputs are saved locally.
"""

from generate_documents import (
    generate_resume_docx,
    generate_cover_letter_docx
)

import os
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def print_header(title: str) -> None:
    print(f"\n{'=' * 50}")
    print(f"{title}")
    print(f"{'=' * 50}\n")


def load_resume(filepath: str = "resume.txt") -> str:

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

    except FileNotFoundError:
        print(f"Error: '{filepath}' not found.")
        exit(1)


def get_job_description() -> str:

    print("Paste the job description below.")
    print("When finished, type END on a new line.\n")

    lines = []

    while True:

        line = input()

        if line.strip().upper() == "END":
            break

        lines.append(line)

    return "\n".join(lines)


SYSTEM_PROMPT = """
You are an experienced IT recruiter, ATS optimization specialist, and career advisor.

Rules:
1. Never invent experience or certifications.
2. Keep all writing realistic and human.
3. Avoid robotic AI phrasing.
4. Optimize for ATS naturally.
5. Sound professional but conversational.
6. Tailor the resume closely to the job description.
7. Keep the cover letter authentic and believable.
"""


def build_prompt(
    resume_text: str,
    job_description: str
) -> str:

    return f"""
Analyze this resume against the job description.

Generate FINAL recruiter-ready outputs.

Return EXACTLY in this structure.

===FINAL_RESUME===


===FINAL_COVER_LETTER===


CANDIDATE RESUME:

{resume_text}


JOB DESCRIPTION:

{job_description}
"""


def call_openai(prompt: str) -> str:

    response = client.chat.completions.create(
        model="gpt-4.1-mini",

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.7
    )

    return response.choices[0].message.content


def parse_sections(
    analysis: str
) -> tuple[str, str]:

    try:

        final_resume = (
            analysis
            .split("===FINAL_RESUME===")[1]
            .split("===FINAL_COVER_LETTER===")[0]
            .strip()
        )

        final_cover_letter = (
            analysis
            .split("===FINAL_COVER_LETTER===")[1]
            .strip()
        )

        return final_resume, final_cover_letter

    except Exception as e:

        print("\nError parsing AI response.")
        print(e)

        return "", ""


def save_outputs(
    final_resume: str,
    final_cover_letter: str
) -> None:

    os.makedirs("outputs", exist_ok=True)

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M"
    )

    # Resume path
    resume_output_path = (
        f"outputs/generated_resume_{timestamp}.docx"
    )

    # Cover letter path
    cover_letter_output_path = (
        f"outputs/generated_cover_letter_{timestamp}.docx"
    )

    # Generate formatted resume
    resume_path = generate_resume_docx(
        final_resume,
        resume_output_path
    )

    # Generate formatted cover letter
    cover_letter_path = generate_cover_letter_docx(
        final_cover_letter,
        cover_letter_output_path
    )

    print_header("FILES GENERATED SUCCESSFULLY")

    print(f"Resume:")
    print(f"  → {resume_path}")

    print()

    print(f"Cover Letter:")
    print(f"  → {cover_letter_path}")

    print()


def main():

    print_header("AI CAREER ASSISTANT")

    resume_text = load_resume()

    job_description = get_job_description()

    print("\nAnalyzing job description...")
    print("Generating recruiter-ready outputs...\n")

    prompt = build_prompt(
        resume_text,
        job_description
    )

    try:

        analysis = call_openai(prompt)

    except Exception as e:

        print(f"OpenAI API Error: {e}")
        exit(1)

    final_resume, final_cover_letter = parse_sections(
        analysis
    )

    if final_resume and final_cover_letter:

        save_outputs(
            final_resume,
            final_cover_letter
        )

    else:

        print("Could not generate outputs correctly.")


if __name__ == "__main__":
    main()