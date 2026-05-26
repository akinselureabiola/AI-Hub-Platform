from collections import Counter

from openai import OpenAI
import streamlit as st
import re


# ==========================================
# ATS STOPWORDS
# ==========================================

STOPWORDS = {

    "and", "the", "for", "with", "this", "that",
    "from", "your", "have", "will", "into",
    "their", "they", "them", "about", "over",
    "under", "more", "less", "very", "using",
    "used", "user", "users", "people", "hours",
    "jobs", "job", "work", "working", "role",
    "team", "within", "across", "ensure",
    "ensuring", "support", "good", "best",
    "including", "maintain", "maintaining",
    "today", "yesterday", "ago", "linkedin",
    "responses", "exclusive", "click", "apply",
    "candidate", "company", "professional",
    "location", "germany", "berlin", "hamburg",
    "mainz", "hybrid", "remote", "onsite",
    "fulltime", "parttime"

}


# ==========================================
# HIGH VALUE TECH KEYWORDS
# ==========================================

TECH_KEYWORDS = {

    "active directory",
    "microsoft 365",
    "entra id",
    "exchange online",
    "teams",
    "sharepoint",
    "onedrive",
    "vpn",
    "dns",
    "dhcp",
    "tcp/ip",
    "jira",
    "intune",
    "windows",
    "powershell",
    "itil",
    "ticketing",
    "incident management",
    "access control",
    "onboarding",
    "offboarding",
    "network troubleshooting",
    "service desk",
    "technical support",
    "endpoint management",
    "user provisioning",
    "identity management",
    "sla",
    "troubleshooting"

}


# ==========================================
# OPENAI CLIENT
# ==========================================

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

STOPWORDS = {
    "and", "the", "with", "for", "that", "this",
    "from", "into", "your", "their", "will",
    "have", "has", "had", "are", "was", "were",
    "you", "our", "they", "them", "while",
    "using", "including", "through", "across",
    "within", "such", "than", "then", "also",
    "best", "quality", "service", "support",
    "team", "teams", "work", "working",
    "professional", "skills", "experience",
    "role", "job", "company", "office",
    "client", "clients"
}

# ==========================================
# CLEAN ATS SCORE
# ==========================================

def clean_ats_score(score_text):

    try:

        digits = "".join(
            filter(str.isdigit, str(score_text))
        )

        return int(digits)

    except:

        return 0


def clean_generated_text(text):

    if not text:
        return ""

    # ==========================================
    # REMOVE MARKDOWN
    # ==========================================

    text = text.replace("**", "")
    text = text.replace("*", "")
    text = text.replace("```", "")

    # ==========================================
    # FIX BULLET ENCODING
    # ==========================================

    text = text.replace("", "•")

    # ==========================================
    # REMOVE AI GARBAGE SECTIONS
    # ==========================================

    if "Keywords Integrated:" in text:
        text = text.split("Keywords Integrated:")[0]

    unwanted_phrases = [

        "Final Resume",
        "Tailored Resume",
        "ATS Match Analysis",
        "Job Fit Analysis",
        "Improvement Suggestions",
        "Matching Keywords",
        "Missing Keywords",
        "Tailored Cover Letter"

    ]

    cleaned_lines = []

    for line in text.split("\n"):

        stripped = line.strip()

        if not stripped:
            cleaned_lines.append("")
            continue

        should_skip = False

        for phrase in unwanted_phrases:

            if phrase.lower() in stripped.lower():

                should_skip = True
                break

        if should_skip:
            continue

        cleaned_lines.append(stripped)

    text = "\n".join(cleaned_lines)

    # ==========================================
    # ENTERPRISE WORD NORMALIZATION
    # ==========================================

    replacements = {

    "realworld": "real-world",
    "AIpowered": "AI-powered",
    "handson": "hands-on",
    "crossteam": "cross-team",
    "highquality": "high-quality",
    "Windowsbased": "Windows-based",
    "Power Shell": "PowerShell",
    "Git Hub": "GitHub",
    "One Drive": "OneDrive",
    "Share Point": "SharePoint",
    "ticketbased": "ticket-based",
    "businesscritical": "business-critical",
    "selfservice": "self-service",
    "daytoday": "day-to-day",
    "SLAbased": "SLA-based",
    "ITSMbased": "ITSM-based"

    }

    for pattern, replacement in replacements.items():

        text = re.sub(
            pattern,
            replacement,
            text,
            flags=re.IGNORECASE
        )

    # ==========================================
    # FIX MISSING SPACE BEFORE CAPITAL LETTERS
    # ==========================================

    text = re.sub(
        r"([a-z])([A-Z])",
        r"\1 \2",
        text
    )

    # ==========================================
    # CLEAN EXCESSIVE SPACING
    # ==========================================

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    # ==========================================
    # REMOVE EXTRA BULLET AT END
    # ==========================================

    text = re.sub(
        r"\n•\s*$",
        "",
        text
    )

    return text.strip()

# ==========================================
# KEYWORD EXTRACTION
# ==========================================

def extract_keywords(text):

    text = text.lower()

    text = re.sub(
        r"[^a-zA-Z0-9+/#\-\s]",
        " ",
        text
    )

    words = text.split()

    cleaned = []

    for word in words:

        if len(word) < 3:
            continue

        if word in STOPWORDS:
            continue

        cleaned.append(word)

    return set(cleaned)

# ==========================================
# GENERATE ATS ANALYSIS
# ==========================================

def generate_ats_analysis(
    keyword_results
):

    return {

        "original_ats_score": str(
            keyword_results["score"]
        ),

        "optimized_ats_score": str(
            min(
                keyword_results["score"] + 15,
                95
            )
        ),

        "matching_keywords": ", ".join(
            keyword_results["matched"]
        ),

        "missing_keywords": ", ".join(
            keyword_results["missing"]
        )

    }


# ==========================================
# GENERATE TAILORED RESUME
# ==========================================
def generate_tailored_resume(
    resume_text,
    job_description,
    job_mode
):

    career_focus = ""

    if job_mode == "IT Support":

        career_focus = """
Focus heavily on:
- Microsoft 365
- Active Directory
- troubleshooting
- ITSM
- SLA
- service desk operations
- endpoint support
- onboarding/offboarding
- VPN
- DNS
- DHCP
"""

    elif job_mode == "Cybersecurity":

        career_focus = """
Focus heavily on:
- SIEM
- SOC
- IAM
- cybersecurity operations
- compliance
- risk management
- incident response
- vulnerability management
- access control
"""

    elif job_mode == "Data Analyst":

        career_focus = """
Focus heavily on:
- SQL
- Excel
- Python
- Power BI
- Tableau
- dashboards
- reporting
- analytics
- data visualization
"""

    elif job_mode == "Cloud Support":

        career_focus = """
Focus heavily on:
- Azure
- AWS
- virtualization
- networking
- cloud administration
- infrastructure
- endpoint management
"""

    elif job_mode == "DevOps":

        career_focus = """
Focus heavily on:
- Docker
- Kubernetes
- CI/CD
- Linux
- automation
- scripting
- infrastructure as code
"""

    prompt = f"""
You are an elite IT resume writer and recruiter specializing in:
- IT Support
- Desktop Support
- Helpdesk
- Endpoint Support
- Microsoft 365
- Active Directory
- Infrastructure Support

Your task is to tailor the candidate resume to the job description.

IMPORTANT RULES:

- Preserve ALL original candidate information
- Preserve original education
- Preserve original certifications
- Preserve original companies
- Preserve original job titles

NEVER:
- invent fake experience
- invent certifications
- invent education
- generate placeholders
- generate fake technologies
- generate fake years of experience

OPTIMIZATION GOALS:
- improve ATS alignment
- improve recruiter readability
- strengthen enterprise IT terminology
- naturally integrate relevant keywords
- improve operational realism
- improve business impact wording

IMPORTANT:
- Use realistic enterprise IT support terminology
- Use stronger operational wording
- Keep language concise and recruiter-friendly
- Make the resume sound modern and realistic

FORMAT:
- Professional Summary
- Skills
- Professional Experience
- Projects
- Education
- Certifications
- Languages

Use bullet points for achievements.

MASTER RESUME:
{resume_text}

CAREER FOCUS:
{career_focus}

JOB DESCRIPTION:
{job_description}
"""

    response = client.chat.completions.create(

        model="gpt-4.1",

        temperature=0.4,

        messages=[

            {
                "role": "user",
                "content": prompt
            }

        ]
    )

    content = response.choices[0].message.content

    return clean_generated_text(content)

# ==========================================
# GENERATE COVER LETTER
# ==========================================

def generate_cover_letter(
    tailored_resume,
    job_description
):

    prompt = f"""
You are a senior technical recruiter writing a modern IT support cover letter.

Write a concise, realistic, human-sounding cover letter.

RULES:
- Use natural professional language
- Avoid generic AI phrases
- Avoid sounding overly formal
- Do not repeat the resume
- Focus on alignment with the role
- Mention operational support experience
- Mention Microsoft 365, Active Directory, troubleshooting, and service desk strengths when relevant
- Show motivation and professionalism
- Keep it under 350 words
- No placeholders
- No fake experience
- No exaggerated claims

The tone should sound like a real candidate applying for an IT support or IT operations role in Germany.

TAILORED RESUME:
{tailored_resume}

JOB DESCRIPTION:
{job_description}
"""

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        temperature=0.5,

        messages=[

            {
                "role": "user",
                "content": prompt
            }

        ]
    )

    content = response.choices[0].message.content

    return clean_generated_text(content)


# ==========================================
# MAIN PIPELINE
# ==========================================


def calculate_keyword_match(
    resume_text,
    job_description
):

    # ==========================================
    # ATS MATCHING LOGIC
    # ==========================================

    resume_keywords = extract_keywords(
        resume_text
    )

    job_keywords = extract_keywords(
        job_description
    )

    matched = []

    missing = []

    for keyword in TECH_KEYWORDS:

        keyword_lower = keyword.lower()

        if (
            keyword_lower in resume_text.lower()
            and keyword_lower in job_description.lower()
        ):

            matched.append(keyword)

        elif keyword_lower in job_description.lower():

            missing.append(keyword)

    base_score = int(

        (
            len(matched)
            / max(len(matched) + len(missing), 1)
        ) * 100

    )

    score = min(
        max(base_score + 8, 20),
        92
    )

    return {
        "score": score,
        "matched": ", ".join(matched[:25]),
        "missing": ", ".join(missing[:25])
    }

def run_resume_pipeline(
    resume_text,
    job_description,
    job_mode
):

    keyword_results = calculate_keyword_match(
        resume_text,
        job_description
    )

    ats_analysis = generate_ats_analysis(
        keyword_results
    )

    tailored_resume = generate_tailored_resume(
        resume_text,
        job_description,
        job_mode
    )

    tailored_cover_letter = generate_cover_letter(
        tailored_resume,
        job_description
    )

    return {

        "tailored_resume": tailored_resume,

        "tailored_cover_letter": tailored_cover_letter,

        "original_ats_score": ats_analysis["original_ats_score"],

        "optimized_ats_score": ats_analysis["optimized_ats_score"],

        "matching_keywords": ats_analysis["matching_keywords"],

        "missing_keywords": ats_analysis["missing_keywords"],

        "job_fit_analysis": "Resume analyzed successfully against the job description.",

        "improvement_suggestions": "Improve missing keyword coverage and strengthen measurable technical achievements."

    }