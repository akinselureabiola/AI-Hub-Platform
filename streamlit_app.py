import os
from datetime import datetime

import streamlit as st

from dotenv import load_dotenv
from openai import OpenAI

from generate_documents import (
    generate_resume_docx,
    generate_cover_letter_docx
)

from file_utils import (
    extract_resume_text
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
    page_title="AI Resume Assistant",
    page_icon="📄",
    layout="wide"
)

# =========================
# SESSION STATE
# =========================

if "generated" not in st.session_state:

    st.session_state.generated = False

# =========================
# PAGE HEADER
# =========================

st.title(
    "📄 AI Resume Assistant"
)

st.markdown(
    """
Upload your resume and paste a job description to generate:

- ATS analysis
- Tailored resume
- Tailored cover letter
"""
)

# =========================
# FILE UPLOAD
# =========================

uploaded_resume = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx", "txt"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=300
)

generate_clicked = st.button(
    "Generate Documents"
)

# =========================
# SYSTEM PROMPT
# =========================

SYSTEM_PROMPT = """
You are an experienced IT recruiter and ATS optimization specialist.

Your tasks:

1. Analyze the resume against the job description
2. Provide a realistic ATS score
3. Identify matching keywords
4. Identify missing keywords
5. Provide realistic improvement suggestions
6. Generate a recruiter-ready tailored resume
7. Generate a tailored professional cover letter

IMPORTANT RULES:

- Be realistic with ATS scoring
- Do NOT inflate scores
- Prioritize technical alignment
- Avoid robotic AI wording
- Keep all writing natural and human
- Never invent fake experience
- Tailor closely to the job description
- Keep resume recruiter-friendly

Return EXACTLY in this format:

===ATS_SCORE===
[score]

===MATCHING_KEYWORDS===
[keywords]

===MISSING_KEYWORDS===
[keywords]

===IMPROVEMENT_SUGGESTIONS===
[suggestions]

===TAILORED_RESUME===
[resume]

===COVER_LETTER===
[cover letter]
"""

# =========================
# HELPER FUNCTIONS
# =========================

def extract_section(
    text,
    start,
    end=None
):

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


def clean_ats_score(score_text):

    try:

        import re

        match = re.search(r"\d+", score_text)

        if match:

            score = int(match.group())

            return min(max(score, 0), 100)

        return 0

    except:

        return 0

# =========================
# MAIN PROCESS
# =========================

if generate_clicked:

    if not uploaded_resume:

        st.warning(
            "Please upload a resume."
        )

        st.stop()

    if not job_description:

        st.warning(
            "Please paste a job description."
        )

        st.stop()

    resume_text = extract_resume_text(
        uploaded_resume
    )

    if not resume_text:

        st.error(
            "Could not process uploaded resume."
        )

        st.stop()

    try:

        with st.spinner(
            "Generating recruiter-ready documents..."
        ):

            prompt = f"""
RESUME:

{resume_text}

JOB DESCRIPTION:

{job_description}
"""

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

                temperature=0.6
            )

            output = (
                response
                .choices[0]
                .message
                .content
            )

            # =========================
            # EXTRACT RESULTS
            # =========================

            ats_score = extract_section(
                output,
                "===ATS_SCORE===",
                "===MATCHING_KEYWORDS==="
            )

            matching_keywords = extract_section(
                output,
                "===MATCHING_KEYWORDS===",
                "===MISSING_KEYWORDS==="
            )

            missing_keywords = extract_section(
                output,
                "===MISSING_KEYWORDS===",
                "===IMPROVEMENT_SUGGESTIONS==="
            )

            improvement_suggestions = extract_section(
                output,
                "===IMPROVEMENT_SUGGESTIONS===",
                "===TAILORED_RESUME==="
            )

            tailored_resume = extract_section(
                output,
                "===TAILORED_RESUME===",
                "===COVER_LETTER==="
            )

            cover_letter = extract_section(
                output,
                "===COVER_LETTER==="
            )

            # =========================
            # GENERATE DOCX FILES
            # =========================

            os.makedirs(
                "outputs",
                exist_ok=True
            )

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
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

            cover_letter_path = (
                generate_cover_letter_docx(
                    cover_letter,
                    cover_letter_filename
                )
            )

            # =========================
            # SAVE TO SESSION STATE
            # =========================

            st.session_state.generated = True

            st.session_state.ats_score = (
                ats_score
            )

            st.session_state.matching_keywords = (
                matching_keywords
            )

            st.session_state.missing_keywords = (
                missing_keywords
            )

            st.session_state.improvement_suggestions = (
                improvement_suggestions
            )

            st.session_state.tailored_resume = (
                tailored_resume
            )

            st.session_state.cover_letter = (
                cover_letter
            )

            st.session_state.resume_path = (
                resume_path
            )

            st.session_state.cover_letter_path = (
                cover_letter_path
            )

            st.session_state.timestamp = (
                timestamp
            )

    except Exception as error:

        st.error(
            f"Generation failed: {error}"
        )

# =========================
# DISPLAY RESULTS
# =========================

if st.session_state.generated:

    st.success(
        "Documents generated successfully."
    )

    score = clean_ats_score(
        st.session_state.ats_score
    )

    col1, col2 = st.columns(2)

    # =========================
    # LEFT COLUMN
    # =========================

    with col1:

        st.metric(
            "ATS Match Score",
            f"{score}%"
        )

        safe_score = min(max(int(score), 0), 100)

        st.progress(safe_score)

        if score >= 80:

            st.success(
                "Strong ATS Match"
            )

        elif score >= 65:

            st.warning(
                "Moderate ATS Match"
            )

        else:

            st.error(
                "Low ATS Match"
            )

        st.markdown(
            "### Matching Keywords"
        )

        st.write(
            st.session_state.matching_keywords
        )

    # =========================
    # RIGHT COLUMN
    # =========================

    with col2:

        st.markdown(
            "### Missing Keywords"
        )

        st.write(
            st.session_state.missing_keywords
        )

    # =========================
    # IMPROVEMENTS
    # =========================

    st.markdown(
        "### Improvement Suggestions"
    )

    st.write(
        st.session_state.improvement_suggestions
    )

    st.divider()

    # =========================
    # DOCUMENTS
    # =========================

    col1, col2 = st.columns(2)

    # =========================
    # RESUME
    # =========================

    with col1:

        st.subheader(
            "Tailored Resume"
        )

        with st.expander(
            "Preview Resume"
        ):

            st.text_area(
                "Resume",
                st.session_state.tailored_resume,
                height=400,
                label_visibility="collapsed"
            )

        with open(
            st.session_state.resume_path,
            "rb"
        ) as file:

            st.download_button(
                "Download Resume",
                file,
                file_name=(
                    f"Resume_{st.session_state.timestamp}.docx"
                )
            )

    # =========================
    # COVER LETTER
    # =========================

    with col2:

        st.subheader(
            "Cover Letter"
        )

        with st.expander(
            "Preview Cover Letter"
        ):

            st.text_area(
                "Cover Letter",
                st.session_state.cover_letter,
                height=400,
                label_visibility="collapsed"
            )

        with open(
            st.session_state.cover_letter_path,
            "rb"
        ) as file:

            st.download_button(
                "Download Cover Letter",
                file,
                file_name=(
                    f"Cover_Letter_{st.session_state.timestamp}.docx"
                )
            )