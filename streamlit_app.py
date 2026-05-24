from datetime import datetime
import os

import streamlit as st

from dotenv import load_dotenv
from openai import OpenAI

from pypdf import PdfReader
from docx import Document

from system_prompts import (
    ATS_ANALYSIS_PROMPT,
    RESUME_GENERATION_PROMPT,
    COVER_LETTER_PROMPT
)

from generate_documents import (
    generate_resume_docx,
    generate_cover_letter_docx
)

# =========================
# LOAD ENV
# =========================

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Resume Automation",
    page_icon="📄",
    layout="wide"
)

# =========================
# HEADER
# =========================

st.title("📄 AI Resume Automation System")

st.markdown(
    "Generate ATS-optimized recruiter-ready resumes and cover letters."
)

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.header(
        "AI Resume Automation"
    )

    st.markdown(
        """
        ### Features
        
        - ATS Match Analysis
        - Resume Tailoring
        - Cover Letter Generation
        - DOCX Export
        - Recruiter Optimization
        """
    )

    st.divider()

    st.caption(
        "Built with Streamlit + OpenAI"
    )

# =========================
# HELPERS
# =========================

def extract_text_from_pdf(file):

    reader = PdfReader(file)

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:

            text += extracted + "\n"

    return text


def extract_text_from_docx(file):

    doc = Document(file)

    text = []

    for paragraph in doc.paragraphs:

        text.append(paragraph.text)

    return "\n".join(text)


def extract_resume_text(uploaded_file):

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".txt"):

        return uploaded_file.read().decode("utf-8")

    elif file_name.endswith(".pdf"):

        return extract_text_from_pdf(uploaded_file)

    elif file_name.endswith(".docx"):

        return extract_text_from_docx(uploaded_file)

    else:

        return None


def extract_section(text, start, end=None):

    try:

        if end:

            return (
                text
                .split(start)[1]
                .split(end)[0]
                .strip()
            )

        return (
            text
            .split(start)[1]
            .strip()
        )

    except:

        return "Not available"

# =========================
# INPUTS
# =========================

uploaded_resume = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx", "txt"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=350
)

# =========================
# BUTTONS
# =========================

col1, col2 = st.columns([1, 1])

with col1:

    generate_clicked = st.button(
        "Generate Documents"
    )

with col2:

    if st.button("New Analysis"):

        st.rerun()

# =========================
# MAIN PROCESS
# =========================

if generate_clicked:

    if not uploaded_resume:

        st.warning(
            "Please upload a resume."
        )

    elif not job_description:

        st.warning(
            "Please paste a job description."
        )

    else:

        resume_text = extract_resume_text(
            uploaded_resume
        )

        if not resume_text:

            st.error(
                "Could not process uploaded resume."
            )

            st.stop()

        with st.spinner(
            "Analyzing and generating recruiter-ready documents..."
        ):

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            # =========================
            # ATS ANALYSIS
            # =========================

            ats_prompt = f"""
RESUME:

{resume_text}


JOB DESCRIPTION:

{job_description}
"""

            ats_response = client.chat.completions.create(
                model="gpt-4.1-mini",

                messages=[
                    {
                        "role": "system",
                        "content": ATS_ANALYSIS_PROMPT
                    },
                    {
                        "role": "user",
                        "content": ats_prompt
                    }
                ],

                temperature=0.4
            )

            ats_output = (
                ats_response
                .choices[0]
                .message
                .content
            )

            ats_score = extract_section(
                ats_output,
                "===ATS_SCORE===",
                "===MATCHING_KEYWORDS==="
            )

            matching_keywords = extract_section(
                ats_output,
                "===MATCHING_KEYWORDS===",
                "===MISSING_KEYWORDS==="
            )

            missing_keywords = extract_section(
                ats_output,
                "===MISSING_KEYWORDS===",
                "===JOB_FIT_ANALYSIS==="
            )

            job_fit_analysis = extract_section(
                ats_output,
                "===JOB_FIT_ANALYSIS===",
                "===IMPROVEMENT_SUGGESTIONS==="
            )

            improvement_suggestions = extract_section(
                ats_output,
                "===IMPROVEMENT_SUGGESTIONS==="
            )

            # =========================
            # SAVE ATS ANALYSIS
            # =========================

            os.makedirs(
                "analysis",
                exist_ok=True
            )

            analysis_filename = (
                f"analysis/ats_analysis_{timestamp}.txt"
            )

            analysis_content = f"""
ATS MATCH ANALYSIS

Estimated ATS Match Score:
{ats_score}


MATCHING KEYWORDS:
{matching_keywords}


MISSING KEYWORDS:
{missing_keywords}


JOB FIT ANALYSIS:
{job_fit_analysis}


RESUME IMPROVEMENT SUGGESTIONS:
{improvement_suggestions}
"""

            with open(
                analysis_filename,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    analysis_content
                )

            # =========================
            # RESUME GENERATION
            # =========================

            resume_prompt = f"""
MASTER RESUME:

{resume_text}


JOB DESCRIPTION:

{job_description}
"""

            resume_response = client.chat.completions.create(
                model="gpt-4.1-mini",

                messages=[
                    {
                        "role": "system",
                        "content": RESUME_GENERATION_PROMPT
                    },
                    {
                        "role": "user",
                        "content": resume_prompt
                    }
                ],

                temperature=0.7
            )

            tailored_resume = (
                resume_response
                .choices[0]
                .message
                .content
                .replace("Final Resume", "")
                .strip()
            )

            # =========================
            # COVER LETTER GENERATION
            # =========================

            cover_prompt = f"""
MASTER RESUME:

{resume_text}


JOB DESCRIPTION:

{job_description}
"""

            cover_response = client.chat.completions.create(
                model="gpt-4.1-mini",

                messages=[
                    {
                        "role": "system",
                        "content": COVER_LETTER_PROMPT
                    },
                    {
                        "role": "user",
                        "content": cover_prompt
                    }
                ],

                temperature=0.7
            )

            tailored_cover_letter = (
                cover_response
                .choices[0]
                .message
                .content
                .replace("Final Cover Letter", "")
                .strip()
            )

        # =========================
        # SAVE DOCX FILES
        # =========================

        os.makedirs(
            "outputs",
            exist_ok=True
        )

        resume_filename = (
            f"outputs/resume_{timestamp}.docx"
        )

        cover_letter_filename = (
            f"outputs/cover_letter_{timestamp}.docx"
        )

        resume_path = generate_resume_docx(
            tailored_resume,
            resume_filename
        )

        cover_letter_path = generate_cover_letter_docx(
            tailored_cover_letter,
            cover_letter_filename
        )

        # =========================
        # SUCCESS MESSAGE
        # =========================

        st.success(
            "Documents generated successfully."
        )

        # =========================
        # ATS ANALYSIS UI
        # =========================

        st.subheader(
            "ATS Match Analysis"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Estimated ATS Match Score",
                ats_score
            )

            st.markdown(
                "### Matching Keywords"
            )

            st.write(
                matching_keywords
            )

        with col2:

            st.markdown(
                "### Missing Keywords"
            )

            st.write(
                missing_keywords
            )

        st.markdown(
            "### Job Fit Analysis"
        )

        st.write(
            job_fit_analysis
        )

        st.markdown(
            "### Resume Improvement Suggestions"
        )

        st.write(
            improvement_suggestions
        )

        st.divider()

        # =========================
        # DOWNLOADS
        # =========================

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                "Tailored Resume"
            )

            with st.expander(
                "Preview Resume"
            ):

                st.text_area(
                    "",
                    tailored_resume,
                    height=400
                )

            with open(
                resume_path,
                "rb"
            ) as file:

                st.download_button(
                    "Download Resume",
                    file,
                    file_name=(
                        f"Resume_{timestamp}.docx"
                    )
                )

        with col2:

            st.subheader(
                "Tailored Cover Letter"
            )

            with st.expander(
                "Preview Cover Letter"
            ):

                st.text_area(
                    "",
                    tailored_cover_letter,
                    height=400
                )

            with open(
                cover_letter_path,
                "rb"
            ) as file:

                st.download_button(
                    "Download Cover Letter",
                    file,
                    file_name=(
                        f"Cover_Letter_{timestamp}.docx"
                    )
                )