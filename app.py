
import streamlit as st
import pandas as pd
import re
import time
import random
from pathlib import Path

st.set_page_config(
    page_title="Agent X | Multi-Agent Hiring Committee",
    page_icon="🤖",
    layout="wide"
)

# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top left, #112036 0%, #050914 40%, #02040a 100%);
    color: #eef4ff;
}
.block-container {
    max-width: 1380px;
    padding-top: 1.1rem;
    padding-bottom: 2rem;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #050814);
    border-right: 1px solid #263653;
}
h1, h2, h3, h4, p, label, li, div {
    color: #eef4ff !important;
}
h1 {
    font-size: 34px !important;
    font-weight: 900 !important;
}
h2 {
    font-size: 26px !important;
    font-weight: 850 !important;
}
h3 {
    font-size: 20px !important;
    font-weight: 800 !important;
}
p, label, div, li {
    font-size: 15px !important;
}
.panel {
    background: linear-gradient(180deg, rgba(13,25,43,.98), rgba(5,11,22,.98));
    border: 1px solid #293854;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 0 22px rgba(0,0,0,.25);
}
.panel-header {
    background: linear-gradient(90deg, #152a43, #173f48);
    padding: 13px 16px;
    border-radius: 13px;
    font-size: 18px !important;
    font-weight: 900;
    margin-bottom: 14px;
    border-left: 5px solid #37d6c2;
}
.hero {
    background: linear-gradient(135deg, rgba(20,39,61,.96), rgba(7,16,30,.99));
    border: 1px solid #37d6c2;
    border-radius: 24px;
    padding: 28px;
    margin-bottom: 18px;
    box-shadow: 0 0 30px rgba(55,214,194,.14);
}
.hero-title {
    font-size: 38px !important;
    font-weight: 950;
    margin-bottom: 6px;
}
.hero-accent {
    color: #37d6c2 !important;
}
.step-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-top: 18px;
}
.step-card {
    background: #0a1424;
    border: 1px solid #293854;
    border-radius: 16px;
    padding: 15px;
    text-align: center;
}
.metric-card {
    background: linear-gradient(180deg, #112033, #0a1424);
    border: 1px solid #293854;
    border-radius: 16px;
    padding: 16px;
    text-align: center;
    margin-bottom: 14px;
    min-height: 122px;
}
.metric-card .num {
    font-size: 31px !important;
    font-weight: 950;
    color: #31d67b !important;
    word-break: break-word;
}
.metric-card .label {
    font-size: 14px !important;
    color: #9aa8c0 !important;
}
.question-box {
    background: #07101e;
    border: 1px solid #33476b;
    border-radius: 22px;
    padding: 26px;
    min-height: 122px;
    display: flex;
    align-items: center;
    font-size: 25px !important;
    font-weight: 900;
    line-height: 1.45;
    margin-bottom: 14px;
}
.ready-box {
    background: linear-gradient(135deg, rgba(24,45,71,.95), rgba(7,16,30,.98));
    border: 1px solid #37d6c2;
    border-radius: 22px;
    padding: 34px;
    text-align: center;
    min-height: 220px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-bottom: 16px;
}
.timer-strip {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #0a1424;
    border: 1px solid #293854;
    border-radius: 18px;
    padding: 14px 18px;
    margin-bottom: 14px;
}
.timer-value {
    font-size: 32px !important;
    font-weight: 950;
    color: #32e7ff !important;
}
.answer-section {
    background: rgba(7,16,30,.72);
    border: 1px solid #293854;
    border-radius: 20px;
    padding: 19px;
    margin-top: 12px;
}
.agent-card {
    background: linear-gradient(180deg,#101b2e,#07101e);
    border: 1px solid #293854;
    border-radius: 18px;
    padding: 17px;
    min-height: 170px;
}
.agent-name {
    font-size: 17px !important;
    font-weight: 900;
    margin-bottom: 8px;
}
.agent-score {
    font-size: 31px !important;
    font-weight: 950;
    color: #37d6c2 !important;
    margin-bottom: 4px;
}
.agent-desc {
    color: #9aa8c0 !important;
    font-size: 13px !important;
    min-height: 38px;
}
.bar {
    background: #18263b;
    height: 9px;
    border-radius: 10px;
    overflow: hidden;
    margin-top: 10px;
}
.fill {
    height: 100%;
    background: linear-gradient(90deg,#37d6c2,#31d67b);
}
.result-box {
    background: rgba(55,214,194,.10);
    border: 1px solid #37d6c2;
    border-radius: 18px;
    padding: 18px;
    margin-top: 16px;
}
.warning-box {
    background: rgba(255,175,63,.10);
    border: 1px solid #ffaf3f;
    border-radius: 18px;
    padding: 18px;
    margin-top: 16px;
}
.good { color: #31d67b !important; }
.mid { color: #ffaf3f !important; }
.bad { color: #ff5b6e !important; }
.vote-pass {
    background: rgba(49,214,123,.13);
    border: 1px solid #31d67b;
    color: #31d67b !important;
    border-radius: 999px;
    padding: 6px 10px;
    font-weight: 900;
    display: inline-block;
}
.vote-review {
    background: rgba(255,175,63,.13);
    border: 1px solid #ffaf3f;
    color: #ffaf3f !important;
    border-radius: 999px;
    padding: 6px 10px;
    font-weight: 900;
    display: inline-block;
}
.vote-risk {
    background: rgba(255,91,110,.13);
    border: 1px solid #ff5b6e;
    color: #ff5b6e !important;
    border-radius: 999px;
    padding: 6px 10px;
    font-weight: 900;
    display: inline-block;
}
.candidate-mini-card {
    background: linear-gradient(180deg,#101b2e,#07101e);
    border: 1px solid #293854;
    border-radius: 18px;
    padding: 17px;
    margin-bottom: 14px;
}
.stButton>button {
    background: linear-gradient(90deg,#168274,#37d6c2) !important;
    color: white !important;
    border: 0 !important;
    border-radius: 13px !important;
    height: 49px !important;
    font-size: 15px !important;
    font-weight: 850 !important;
}
textarea, input {
    background: #08111f !important;
    color: white !important;
    border-radius: 12px !important;
    font-size: 15px !important;
}
[data-testid="stDataFrame"] {
    border-radius: 16px !important;
    overflow: hidden !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# Dataset
# =========================================================
BASE_DIR = Path(__file__).parent
DATASET_PATH = BASE_DIR / "Datathon Database.xlsx"
CANDIDATES_PATH = BASE_DIR / "candidates.csv"

@st.cache_data
def load_dataset(path: str):
    p = Path(path)

    if not p.exists():
        return None, None, None, None

    try:
        xls = pd.ExcelFile(p)
        sheet_names = xls.sheet_names

        def find_sheet(possible_names):
            normalized = {s.strip().lower(): s for s in sheet_names}
            for name in possible_names:
                key = name.strip().lower()
                if key in normalized:
                    return normalized[key]

            # fallback contains search
            for s in sheet_names:
                s_low = s.strip().lower()
                for name in possible_names:
                    n_low = name.strip().lower()
                    if n_low in s_low or s_low in n_low:
                        return s
            return None

        cv_sheet = find_sheet(["CV Database", "CV", "Structured CVs", "Structured Resumes", "Resumes", "Candidates"])
        jobs_sheet = find_sheet(["Job Descriptions", "Jobs", "Job Description", "Roles"])
        resume_sheet = find_sheet(["Resume Text", "Resume Texts", "CV Text", "CV Texts", "Resume"])
        questions_sheet = find_sheet(["General Questionnaire", "Questions", "Interview Questions", "Questionnaire"])

        # If the exact sheets are not found, use positional fallback
        if cv_sheet is None and len(sheet_names) >= 1:
            cv_sheet = sheet_names[0]
        if resume_sheet is None and len(sheet_names) >= 2:
            resume_sheet = sheet_names[1]
        if jobs_sheet is None and len(sheet_names) >= 3:
            jobs_sheet = sheet_names[2]
        if questions_sheet is None and len(sheet_names) >= 4:
            questions_sheet = sheet_names[3]

        cv_db = pd.read_excel(p, sheet_name=cv_sheet).dropna(how="all") if cv_sheet else None
        jobs = pd.read_excel(p, sheet_name=jobs_sheet).dropna(how="all") if jobs_sheet else None
        resume_text = pd.read_excel(p, sheet_name=resume_sheet).dropna(how="all") if resume_sheet else None
        questions_df = pd.read_excel(p, sheet_name=questions_sheet).dropna(how="all") if questions_sheet else None

        return cv_db, jobs, resume_text, questions_df

    except Exception:
        return None, None, None, None

cv_db, jobs_df, resume_df, questions_df = load_dataset(str(DATASET_PATH))

fallback_jobs = pd.DataFrame([
    {
        "Role": "Project Manager",
        "Field": "Management",
        "Role Summary": "Leads projects from initiation to delivery.",
        "Key Responsibilities": "Manage scope, timelines, risks, teams, and stakeholders.",
        "Required Skills": "Project management, Risk management, Stakeholder communication, Agile, Scrum, Budget tracking, Leadership, Problem solving",
        "Recommended Tools": "Jira, MS Project, Asana, Excel, PowerPoint, Confluence",
        "Evaluation Focus": "Leadership, planning, risk management, stakeholder communication."
    },
    {
        "Role": "Data Analyst",
        "Field": "Data",
        "Role Summary": "Analyzes and visualizes data to support decisions.",
        "Key Responsibilities": "Clean data, write SQL, build dashboards, analyze trends.",
        "Required Skills": "SQL, Excel, Power BI, Tableau, Data cleaning, Statistics, Dashboarding, Insight communication",
        "Recommended Tools": "SQL, Excel, Power BI, Tableau, Python",
        "Evaluation Focus": "SQL, data interpretation, dashboards, insight communication."
    },
    {
        "Role": "Financial Analyst",
        "Field": "Finance",
        "Role Summary": "Analyzes financial performance and supports business decisions.",
        "Key Responsibilities": "Financial modeling, budgeting, variance analysis, reporting.",
        "Required Skills": "Financial modeling, Excel, Forecasting, Budgeting, Analysis, Reporting, Communication",
        "Recommended Tools": "Excel, Power BI, Tableau, ERP",
        "Evaluation Focus": "Financial analysis, accuracy, reporting, business insight."
    },
    {
        "Role": "Digital Marketing Specialist",
        "Field": "Marketing",
        "Role Summary": "Plans and optimizes digital campaigns.",
        "Key Responsibilities": "Campaign planning, analytics, SEO, content, paid ads.",
        "Required Skills": "SEO, Google Ads, Analytics, Content, Social media, Campaign optimization, Communication",
        "Recommended Tools": "Google Analytics, Meta Ads, Google Ads, Excel",
        "Evaluation Focus": "Campaign performance, analytics, creativity, optimization."
    },
    {
        "Role": "Backend Developer",
        "Field": "Technology",
        "Role Summary": "Builds APIs and backend systems.",
        "Key Responsibilities": "API development, database integration, testing, performance.",
        "Required Skills": "Python, APIs, SQL, Databases, Backend development, Testing, Problem solving",
        "Recommended Tools": "Python, FastAPI, PostgreSQL, Docker, Git",
        "Evaluation Focus": "Backend logic, APIs, database design, reliability."
    }
])

if jobs_df is None or "Role" not in jobs_df.columns:
    jobs_df = fallback_jobs

QUESTION_BANK = {
    "project manager": [
        "Tell us about a project you managed under pressure.",
        "How do you handle stakeholder conflicts?",
        "Describe a situation where you led a cross-functional team.",
        "How do you manage project risks and deadlines?",
        "Describe a difficult decision you made during a project.",
        "How do you prioritize multiple projects at the same time?",
        "Tell us about a failed project and what you learned from it.",
        "How do you motivate team members during a difficult project?",
        "Describe a situation where communication failed in a project and how you fixed it.",
        "How do you track project performance and delivery progress?",
        "Tell us about a time you solved a major operational issue.",
        "Why are you suitable for a Project Manager role?"
    ],
    "data analyst": [
        "Explain a dashboard or report you created.",
        "Describe a time you found insights from data.",
        "How do you clean or validate data?",
        "Tell us about a difficult SQL problem you solved.",
        "How do you explain technical findings to non-technical users?",
        "Describe a reporting challenge you faced.",
        "How do you handle missing or inconsistent data?",
        "Tell us about a time data improved decision making.",
        "What visualization tools have you used?",
        "Describe a KPI dashboard you built.",
        "How do you ensure data accuracy?",
        "Why are you suitable for a Data Analyst role?"
    ],
    "financial analyst": [
        "Describe a financial report you created and how it supported a decision.",
        "How do you handle inaccurate or incomplete financial data?",
        "Tell us about a time you identified a financial risk.",
        "How do you explain financial insights to non-finance stakeholders?",
        "Describe your experience with budgeting or forecasting.",
        "Why are you suitable for a Financial Analyst role?"
    ],
    "digital marketing": [
        "Describe a campaign you optimized using data.",
        "How do you measure campaign success?",
        "Tell us about a time you improved conversion or engagement.",
        "How do you handle poor campaign performance?",
        "What tools do you use for digital marketing analysis?",
        "Why are you suitable for a Digital Marketing Specialist role?"
    ],
    "backend": [
        "Describe a backend system or API you built.",
        "How do you handle database performance issues?",
        "Tell us about a difficult bug you solved.",
        "How do you ensure backend reliability?",
        "Describe a time you improved system performance.",
        "Why are you suitable for a Backend Developer role?"
    ],
}

DEFAULT_QUESTIONS = [
    "Tell us about yourself and why you are interested in this role.",
    "Describe a time you worked with a team to solve a difficult problem.",
    "Give an example of a time you learned a new tool or technology quickly.",
    "Tell us about a situation where you handled pressure or a tight deadline.",
    "Describe a time you used data or evidence to make a decision.",
    "Why should we select you for this position?"
]

# =========================================================
# Session State
# =========================================================
defaults = {
    "question_index": 0,
    "evaluation": None,
    "selected_role": str(jobs_df["Role"].dropna().iloc[0]),
    "candidate_step": "upload_cv",
    "interview_stage": "locked",
    "answer_start": None,
    "stored_cv_text": "",
    "stored_candidate_name": "",
    "stored_applied_role": "",
    "pre_screen_result": None,
    "selected_questions": [],
    "submitted_candidates": [],
    "experience_required": "3-5 Years",
    "answers_history": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Load saved candidates from CSV on refresh/restart
if not st.session_state.submitted_candidates and CANDIDATES_PATH.exists():
    try:
        saved_df = pd.read_csv(CANDIDATES_PATH)
        st.session_state.submitted_candidates = saved_df.to_dict("records")
    except Exception:
        st.session_state.submitted_candidates = []

# =========================================================
# Helpers
# =========================================================
def split_terms(text):
    if pd.isna(text) or text is None:
        return []
    parts = re.split(r"[,;/\n|]+", str(text))
    return [p.strip() for p in parts if len(p.strip()) >= 2]

def normalize_text(text):
    if text is None:
        return ""
    return re.sub(r"\s+", " ", str(text).lower()).strip()

def extract_years(text):
    text_l = normalize_text(text)
    numbers = [int(x) for x in re.findall(r"(\d+)\s*\+?\s*(?:years|yrs|year)", text_l)]
    return max(numbers) if numbers else 0

def required_years_min(label):
    label = str(label)
    if "5+" in label:
        return 5
    if "3-5" in label:
        return 3
    if "1-2" in label:
        return 1
    return 0

def read_uploaded_file(uploaded_file):
    if uploaded_file is None:
        return ""
    name = uploaded_file.name.lower()
    if name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore")
    if name.endswith(".pdf"):
        try:
            from pypdf import PdfReader
            reader = PdfReader(uploaded_file)
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception:
            return ""
    if name.endswith(".docx"):
        try:
            import docx
            document = docx.Document(uploaded_file)
            return "\n".join(p.text for p in document.paragraphs)
        except Exception:
            return ""
    return ""

def get_selected_job():
    row = jobs_df[jobs_df["Role"].astype(str) == st.session_state.selected_role]
    if row.empty:
        return jobs_df.iloc[0].to_dict()
    return row.iloc[0].to_dict()

def get_role_questions(role_name, cv_text=""):
    role_l = normalize_text(role_name)
    cv_l = normalize_text(cv_text)
    for key, bank in QUESTION_BANK.items():
        if key in role_l:
            pool = list(bank)
            break
    else:
        pool = list(DEFAULT_QUESTIONS)

    # CV-aware follow-up style questions
    cv_based = []
    if "jira" in cv_l or "agile" in cv_l or "scrum" in cv_l:
        cv_based.append("Your CV mentions Agile or Jira. Describe how you used it to improve delivery.")
    if "dashboard" in cv_l or "power bi" in cv_l or "tableau" in cv_l:
        cv_based.append("Your CV mentions dashboards. Tell us how you used reporting to support a decision.")
    if "stakeholder" in cv_l:
        cv_based.append("Your CV mentions stakeholders. Describe a difficult stakeholder situation and how you handled it.")
    if "risk" in cv_l:
        cv_based.append("Your CV mentions risk management. Give an example of a risk you identified early.")

    pool = cv_based + pool
    return list(dict.fromkeys(pool))

def generate_interview_questions():
    bank = get_role_questions(st.session_state.selected_role, st.session_state.stored_cv_text)
    count = min(4, len(bank))
    st.session_state.selected_questions = random.sample(bank, count)
    st.session_state.question_index = 0
    st.session_state.answers_history = []

def timer_remaining(start_time, duration):
    if start_time is None:
        return duration
    elapsed = int(time.time() - start_time)
    return max(0, duration - elapsed)

def timer_text(seconds):
    return f"{seconds // 60:02d}:{seconds % 60:02d}"

def reset_interview_stage():
    st.session_state.interview_stage = "locked"
    st.session_state.answer_start = None

def score_interview_answer(answer):
    if not answer or not answer.strip():
        return 0
    answer_l = normalize_text(answer)
    words = len(answer_l.split())
    length_score = min(words * 1.2, 25)
    star_terms = ["situation", "task", "action", "result", "problem", "solution", "impact", "because", "therefore"]
    structure_score = min(sum(4 for t in star_terms if t in answer_l), 24)
    evidence_terms = ["improved", "reduced", "increased", "delivered", "completed", "dashboard", "data", "team", "stakeholder", "deadline", "risk", "plan"]
    evidence_score = min(sum(4 for t in evidence_terms if t in answer_l), 28)
    clarity_score = 23 if words >= 45 else 12
    return int(min(length_score + structure_score + evidence_score + clarity_score, 100))

def pre_screen_cv_only(cv_text, selected_job, candidate_role=""):
    cv_l = normalize_text(cv_text)
    required_skills = split_terms(selected_job.get("Required Skills", ""))
    tools = split_terms(selected_job.get("Recommended Tools", ""))
    role_l = normalize_text(selected_job.get("Role", ""))

    matched_skills, missing_skills = [], []
    for skill in required_skills:
        skill_l = normalize_text(skill)
        tokens = [t for t in re.split(r"[\s/()]+", skill_l) if len(t) > 2]
        if skill_l in cv_l or any(t in cv_l for t in tokens):
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    skill_score = int((len(matched_skills) / max(len(required_skills), 1)) * 100)
    matched_tools = [tool for tool in tools if normalize_text(tool) in cv_l]
    tool_score = int((len(matched_tools) / max(len(tools), 1)) * 100)

    years = extract_years(cv_text)
    min_years = required_years_min(st.session_state.experience_required)
    if years >= min_years:
        experience_score = 100
    elif years == 0:
        experience_score = 35
    else:
        experience_score = int(max(20, (years / max(min_years, 1)) * 100))

    candidate_role_l = normalize_text(candidate_role)
    role_terms = [t for t in re.split(r"\s+", role_l) if len(t) > 2]
    role_mentions = sum(1 for t in role_terms if t in cv_l or t in candidate_role_l)
    role_score = 85 if role_mentions else 40

    known_roles = ["data analyst", "financial analyst", "digital marketing", "backend developer", "frontend developer", "project manager", "business analyst", "software engineer", "accountant"]
    found_roles = [r for r in known_roles if r in cv_l or r in candidate_role_l]
    mismatch_roles = [r for r in found_roles if r not in role_l]

    risk_penalty = 0
    risk_flags = []
    if mismatch_roles and role_l not in found_roles:
        risk_penalty += 30
        risk_flags.append(f"Role mismatch detected: CV appears closer to {', '.join(mismatch_roles)}.")
    if skill_score < 70:
        risk_penalty += 20
        risk_flags.append("Required skills match is below the interview threshold.")
    if experience_score < 70:
        risk_penalty += 15
        risk_flags.append("Experience may be below the required level.")
    if len(cv_l.split()) < 40:
        risk_penalty += 20
        risk_flags.append("CV text is too short or could not be parsed properly.")
    if not risk_flags:
        risk_flags.append("CV passed the initial screening criteria.")

    pre_score = int((skill_score * 0.45) + (tool_score * 0.15) + (experience_score * 0.25) + (role_score * 0.15) - risk_penalty)
    pre_score = max(0, min(100, pre_score))

    return {
        "pre_score": pre_score,
        "status": "Eligible for Interview" if pre_score >= 65 else "Not Eligible for Interview",
        "passed": pre_score >= 65,
        "skill_score": skill_score,
        "tool_score": tool_score,
        "experience_score": experience_score,
        "role_score": role_score,
        "risk_penalty": risk_penalty,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "matched_tools": matched_tools,
        "risk_flags": risk_flags,
        "years_found": years,
    }

def evaluate_candidate(cv_text, answer, selected_job, candidate_role=""):
    cv_only = pre_screen_cv_only(cv_text, selected_job, candidate_role)
    interview_score = score_interview_answer(answer)

    fit_score = int((cv_only["pre_score"] * 0.70) + (interview_score * 0.30))
    fit_score = max(0, min(100, fit_score))

    skills_score = int((cv_only["skill_score"] * 0.75) + (cv_only["tool_score"] * 0.25))
    communication_score = interview_score
    risk_score = max(0, 100 - cv_only["risk_penalty"])

    if fit_score >= 80 and cv_only["risk_penalty"] < 25:
        recommendation = "Strong Hire"
    elif fit_score >= 60:
        recommendation = "Suitable with Reservations"
    elif fit_score >= 45:
        recommendation = "Needs Review"
    else:
        recommendation = "Not Suitable"

    strengths = []
    if cv_only["skill_score"] >= 80:
        strengths.append("Strong required-skill match")
    if cv_only["experience_score"] >= 80:
        strengths.append("Relevant experience level")
    if interview_score >= 80:
        strengths.append("Clear and structured interview answers")
    if cv_only["tool_score"] >= 60:
        strengths.append("Relevant tools found in CV")
    if not strengths:
        strengths.append("Some relevant evidence found, but not enough for a strong recommendation")

    weaknesses = []
    if cv_only["missing_skills"]:
        weaknesses.append("Missing skills: " + ", ".join(cv_only["missing_skills"][:4]))
    if cv_only["experience_score"] < 70:
        weaknesses.append("Experience may be below the role requirement")
    if interview_score < 60:
        weaknesses.append("Interview answer needs more detail and evidence")
    if not weaknesses:
        weaknesses.append("No major weakness detected")

    agent_scores = {
        "Role Fit Agent": int((cv_only["pre_score"] * 0.65) + (cv_only["role_score"] * 0.35)),
        "Knowledge & Skills Agent": skills_score,
        "Communication Agent": communication_score,
        "Risk & Uncertainty Agent": risk_score,
        "Evidence Explanation Agent": int((cv_only["skill_score"] * 0.45) + (cv_only["experience_score"] * 0.35) + (interview_score * 0.20)),
        "Final Recommendation Agent": fit_score,
    }

    return {
        "fit_score": fit_score,
        "final_score": fit_score,
        "recommendation": recommendation,
        "skills_score": skills_score,
        "communication_score": communication_score,
        "risk_score": risk_score,
        "skill_score": cv_only["skill_score"],
        "tool_score": cv_only["tool_score"],
        "experience_score": cv_only["experience_score"],
        "role_score": cv_only["role_score"],
        "interview_score": interview_score,
        "risk_penalty": cv_only["risk_penalty"],
        "matched_skills": cv_only["matched_skills"],
        "missing_skills": cv_only["missing_skills"],
        "matched_tools": cv_only["matched_tools"],
        "risk_flags": cv_only["risk_flags"],
        "agent_scores": agent_scores,
        "years_found": cv_only["years_found"],
        "strengths": strengths,
        "weaknesses": weaknesses,
    }

def vote_label(score, risk_agent=False):
    if risk_agent:
        return "LOW RISK" if score >= 75 else "CHECK" if score >= 50 else "HIGH RISK"
    if score >= 80:
        return "PASS"
    if score >= 60:
        return "REVIEW"
    return "RISK"

def vote_class(label):
    if label in ["PASS", "LOW RISK"]:
        return "vote-pass"
    if label == "REVIEW" or label == "CHECK":
        return "vote-review"
    return "vote-risk"

def render_agent_cards(agent_scores):
    agent_desc = {
        "Role Fit Agent": "Evaluates role suitability using CV, experience, and job requirements.",
        "Knowledge & Skills Agent": "Measures core skills, tools, and required knowledge.",
        "Communication Agent": "Evaluates clarity, structure, and relevance of interview answers.",
        "Risk & Uncertainty Agent": "Detects gaps, insufficient evidence, or mismatch risks.",
        "Evidence Explanation Agent": "Checks whether the decision is supported by evidence.",
        "Final Recommendation Agent": "Combines all agents into one hiring recommendation."
    }
    cols = st.columns(3)
    for i, (agent, score) in enumerate(agent_scores.items()):
        risk_agent = agent == "Risk & Uncertainty Agent"
        label = vote_label(score, risk_agent=risk_agent)
        with cols[i % 3]:
            st.markdown(f"""
            <div class="agent-card">
                <div class="agent-name">{agent}</div>
                <div class="agent-score">{score}%</div>
                <div class="agent-desc">{agent_desc.get(agent, "")}</div>
                <div class="bar"><div class="fill" style="width:{score}%"></div></div>
                <br>
                <span class="{vote_class(label)}">{label}</span>
            </div>
            """, unsafe_allow_html=True)

def save_candidate_record(evaluation):
    record = {
        "Candidate Name": st.session_state.stored_candidate_name,
        "Applied Role": st.session_state.stored_applied_role,
        "Fit Score": evaluation["fit_score"],
        "Skills Score": evaluation["skills_score"],
        "Communication Score": evaluation["communication_score"],
        "Risk Score": evaluation["risk_score"],
        "Recommendation": evaluation["recommendation"],
    }

    existing_df = pd.DataFrame(st.session_state.submitted_candidates)

    if not existing_df.empty and "Candidate Name" in existing_df.columns:
        duplicate_mask = (
            (existing_df["Candidate Name"].astype(str) == str(record["Candidate Name"])) &
            (existing_df["Applied Role"].astype(str) == str(record["Applied Role"]))
        )
        existing_df = existing_df[~duplicate_mask]
        st.session_state.submitted_candidates = existing_df.to_dict("records")

    st.session_state.submitted_candidates.append(record)

    pd.DataFrame(st.session_state.submitted_candidates).to_csv(
        CANDIDATES_PATH,
        index=False,
        encoding="utf-8-sig"
    )

def recommendation_class(rec):
    if rec == "Strong Hire":
        return "good"
    if rec in ["Suitable with Reservations", "Needs Review"]:
        return "mid"
    return "bad"

# =========================================================
# Sidebar
# =========================================================
st.sidebar.title("🤖 Agent X")
page = st.sidebar.radio(
    "Navigation",
    ["Candidate Interface", "AI Hiring War Room", "Candidate Evaluation", "Dataset Benchmark", "Project Overview"]
)

if DATASET_PATH.exists():
    st.sidebar.success("Dataset file found")
    if cv_db is not None or jobs_df is not None or resume_df is not None:
        st.sidebar.success("Dataset loaded")
    else:
        st.sidebar.warning("Dataset file found, but sheets could not be read")
else:
    st.sidebar.warning("Dataset file not found. Put Datathon Database.xlsx next to app.py")

with st.sidebar.expander("Dataset Debug"):
    st.write("App Folder:", str(BASE_DIR))
    st.write("Dataset Path:", str(DATASET_PATH))
    st.write("Dataset Exists:", DATASET_PATH.exists())
    if DATASET_PATH.exists():
        try:
            st.write("Sheets:", pd.ExcelFile(DATASET_PATH).sheet_names)
        except Exception as e:
            st.write("Excel Error:", str(e))

# =========================================================
# Candidate Interface
# =========================================================
if page == "Candidate Interface":
    selected_job = get_selected_job()

    if st.session_state.candidate_step == "upload_cv":
        st.markdown("""
        <div class="hero">
            <div class="hero-title">Multi-Agent AI Hiring Committee</div>
            <p>Upload the CV first. Only candidates with a CV screening score of 65% or above can start the interview.</p>
            <div class="step-grid">
                <div class="step-card">1<br><b>CV Screening</b></div>
                <div class="step-card">2<br><b>Role-Aware Interview</b></div>
                <div class="step-card">3<br><b>Explainable Recommendation</b></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        left, right = st.columns([1.35, 1])

        with left:
            st.markdown('<div class="panel"><div class="panel-header">Candidate Information</div>', unsafe_allow_html=True)

            candidate_name = st.text_input("Candidate Name", placeholder="Example: Sarah Johnson")
            applied_role = st.text_input("Applied Role", value=st.session_state.selected_role)

            input_mode = st.radio("CV Input Mode", ["Upload external CV", "Use dataset CV for demo"], horizontal=True)
            cv_text = ""

            if input_mode == "Upload external CV":
                uploaded_cv = st.file_uploader("Upload CV", type=["pdf", "docx", "txt"])
                if uploaded_cv is not None:
                    cv_text = read_uploaded_file(uploaded_cv)

                manual_cv_text = st.text_area("Or paste CV text here", height=180, placeholder="Paste CV text here...")
                if manual_cv_text.strip():
                    cv_text = manual_cv_text
            else:
                if resume_df is not None and "Candidate ID" in resume_df.columns:
                    options = resume_df["Candidate ID"].dropna().astype(str).tolist()
                    selected_candidate = st.selectbox("Choose dataset candidate", options)
                    selected_resume = resume_df[resume_df["Candidate ID"].astype(str) == selected_candidate].iloc[0]
                    cv_text = str(selected_resume.get("Resume Text", ""))
                    st.text_area("Dataset CV Preview", value=cv_text[:1200], height=180)
                else:
                    st.warning("Resume Text sheet was not found.")

            st.markdown("</div>", unsafe_allow_html=True)

            if st.button("Run CV Screening", use_container_width=True):
                if not candidate_name.strip():
                    st.error("Please enter candidate name.")
                elif not applied_role.strip():
                    st.error("Please enter applied role.")
                elif not cv_text.strip():
                    st.error("Please upload or paste CV text first.")
                else:
                    st.session_state.stored_candidate_name = candidate_name
                    st.session_state.stored_applied_role = applied_role
                    st.session_state.stored_cv_text = cv_text
                    st.session_state.pre_screen_result = pre_screen_cv_only(cv_text, selected_job, applied_role)
                    st.rerun()

            if st.session_state.pre_screen_result:
                pre = st.session_state.pre_screen_result
                if pre["passed"]:
                    st.success(f"CV Screening Passed: {pre['pre_score']}% - Eligible for Interview")
                    if st.button("Start Interview", use_container_width=True):
                        generate_interview_questions()
                        st.session_state.candidate_step = "interview"
                        st.session_state.evaluation = None
                        reset_interview_stage()
                        st.rerun()
                else:
                    st.error(f"CV Screening Failed: {pre['pre_score']}% - Not Eligible for Interview")
                    st.warning("This candidate cannot proceed to interview because CV fit is below 65%.")

                st.subheader("CV Screening Evidence")
                c1, c2 = st.columns(2)
                with c1:
                    st.write("Matched Skills:", pre["matched_skills"])
                    st.write("Matched Tools:", pre["matched_tools"])
                with c2:
                    st.write("Missing Skills:", pre["missing_skills"])
                    st.write("Years Found:", pre["years_found"])
                for flag in pre["risk_flags"]:
                    st.warning(flag)

        with right:
            st.markdown(f"""
            <div class="panel">
                <div class="panel-header">Target Role</div>
                <h2>{st.session_state.selected_role}</h2>
                <p>This role is selected by the evaluator/admin.</p>
                <p>Evaluation criteria are hidden from candidates.</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class="panel">
                <div class="panel-header">Required Outputs</div>
                <ul>
                    <li>Fit Score</li>
                    <li>Knowledge & Skills Score</li>
                    <li>Communication Score</li>
                    <li>Strengths & Weaknesses</li>
                    <li>Risks & Uncertainty</li>
                    <li>Final Recommendation</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    elif st.session_state.candidate_step == "interview":
        if not st.session_state.selected_questions:
            generate_interview_questions()

        current_score = st.session_state.evaluation["final_score"] if st.session_state.evaluation else 0
        current_rec = st.session_state.evaluation["recommendation"] if st.session_state.evaluation else "Pending"

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="metric-card"><div class="label">Progress</div><div class="num">{st.session_state.question_index + 1}/4</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="metric-card"><div class="label">Interview</div><div class="num">03:00</div><div class="label">Answer Time</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-card"><div class="label">Current Result</div><div class="num">{current_score}%</div><div class="label">{current_rec}</div></div>', unsafe_allow_html=True)

        current_question = st.session_state.selected_questions[st.session_state.question_index]
        answer_left = timer_remaining(st.session_state.answer_start, 180)

        if st.session_state.interview_stage == "answer" and answer_left == 0:
            st.session_state.interview_stage = "answer_done"

        st.markdown('<div class="panel"><div class="panel-header">Role-Aware Interview Question</div>', unsafe_allow_html=True)

        if st.session_state.interview_stage == "finished":
            st.markdown("""
            <div class="ready-box">
                <h2>Interview Completed Successfully ✅</h2>
                <p>The candidate completed all 4 role-aware questions.</p>
            </div>
            """, unsafe_allow_html=True)
        elif st.session_state.interview_stage == "locked":
            st.markdown("""
            <div class="ready-box">
                <h2>Ready for the next interview question?</h2>
                <p>The question is hidden. Click when ready. The 3-minute timer starts immediately.</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("I’m Ready - Show Question", use_container_width=True):
                st.session_state.interview_stage = "answer"
                st.session_state.answer_start = time.time()
                st.rerun()
        else:
            st.markdown(f'<div class="question-box">🎤 {current_question}</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="timer-strip">
                <div><b>Answer Timer</b><br><span>Timer started when candidate clicked ready.</span></div>
                <div class="timer-value">{timer_text(answer_left)}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Reset This Question", use_container_width=True):
                reset_interview_stage()
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="answer-section">', unsafe_allow_html=True)
        st.text_input("Candidate Name", value=st.session_state.stored_candidate_name, disabled=True)
        st.text_input("Applied Role", value=st.session_state.stored_applied_role, disabled=True)

        answer_key = f"answer_text_q_{st.session_state.question_index}"
        answer = st.text_area("Candidate Answer", key=answer_key, height=210, placeholder="Write the answer here using clear examples and evidence...")

        b1, b2, b3 = st.columns(3)

        with b1:
            if st.button("Analyze Candidate", use_container_width=True):
                st.session_state.evaluation = evaluate_candidate(
                    st.session_state.stored_cv_text,
                    answer,
                    selected_job,
                    st.session_state.stored_applied_role
                )

                st.session_state.answers_history.append({
                    "Question": current_question,
                    "Answer": answer,
                    "Score": st.session_state.evaluation["interview_score"],
                })

                save_candidate_record(st.session_state.evaluation)
                st.success("Candidate analysis completed.")
                st.rerun()

        with b2:
            if st.button("Next Question", use_container_width=True):
                if st.session_state.question_index < len(st.session_state.selected_questions) - 1:
                    st.session_state.question_index += 1
                    reset_interview_stage()
                    st.rerun()
                else:
                    st.session_state.interview_stage = "finished"
                    st.success("Interview Completed Successfully ✅")

        with b3:
            if st.button("Back to CV Upload", use_container_width=True):
                st.session_state.candidate_step = "upload_cv"
                st.session_state.pre_screen_result = None
                st.session_state.evaluation = None
                st.session_state.selected_questions = []
                reset_interview_stage()
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.interview_stage == "answer":
            time.sleep(1)
            st.rerun()

        if st.session_state.evaluation:
            ev = st.session_state.evaluation
            st.markdown('<div class="panel"><div class="panel-header">AI Committee Evaluation</div>', unsafe_allow_html=True)
            render_agent_cards(ev["agent_scores"])
            rec_class = recommendation_class(ev["recommendation"])
            st.markdown(f"""
            <div class="result-box">
                <h3>Final Recommendation: <span class="{rec_class}">{ev["recommendation"]}</span></h3>
                <p>Fit Score: <b>{ev["fit_score"]}%</b> | Skills Score: <b>{ev["skills_score"]}%</b> | Communication Score: <b>{ev["communication_score"]}%</b></p>
            </div>
            """, unsafe_allow_html=True)

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.subheader("Strengths")
                for item in ev["strengths"]:
                    st.success(item)
            with col_b:
                st.subheader("Weaknesses")
                for item in ev["weaknesses"]:
                    st.warning(item)
            with col_c:
                st.subheader("Risks & Uncertainty")
                for item in ev["risk_flags"]:
                    st.warning(item)
            st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# AI Hiring War Room
# =========================================================
elif page == "AI Hiring War Room":
    st.title("AI Hiring War Room")

    c1, c2, c3, c4 = st.columns(4)
    dataset_count = len(cv_db) if cv_db is not None else 0
    role_count = len(cv_db[cv_db["Role"].astype(str) == st.session_state.selected_role]) if cv_db is not None and "Role" in cv_db.columns else 0
    apps_count = len(st.session_state.submitted_candidates)
    avg_score = int(pd.DataFrame(st.session_state.submitted_candidates)["Fit Score"].mean()) if apps_count else 0

    stats = [("Dataset CVs", dataset_count), ("Role CVs", role_count), ("Applications", apps_count), ("Avg Fit Score", f"{avg_score}%")]
    for col, (label, value) in zip([c1, c2, c3, c4], stats):
        with col:
            st.markdown(f'<div class="metric-card"><div class="num">{value}</div><div class="label">{label}</div></div>', unsafe_allow_html=True)

    st.subheader("Live Candidate Applications")

    clear_col1, clear_col2 = st.columns([1, 4])
    with clear_col1:
        if st.button("Clear Saved Candidates"):
            st.session_state.submitted_candidates = []
            if CANDIDATES_PATH.exists():
                CANDIDATES_PATH.unlink()
            st.rerun()

    if st.session_state.submitted_candidates:
        df = pd.DataFrame(st.session_state.submitted_candidates)
        st.dataframe(df, use_container_width=True, height=260)

        st.subheader("Candidate Decision Cards")
        cols = st.columns(2)
        for i, row in df.iterrows():
            with cols[i % 2]:
                rec_class = recommendation_class(row["Recommendation"])
                st.markdown(f"""
                <div class="candidate-mini-card">
                    <h3>{row["Candidate Name"]}</h3>
                    <p>{row["Applied Role"]}</p>
                    <p><b>Fit Score:</b> {row["Fit Score"]}%</p>
                    <p><b>Skills:</b> {row["Skills Score"]}% | <b>Communication:</b> {row["Communication Score"]}% | <b>Risk:</b> {row["Risk Score"]}%</p>
                    <h3 class="{rec_class}">{row["Recommendation"]}</h3>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No candidates submitted yet.")

    st.subheader("Evaluation Rubric Coverage")
    rubric = pd.DataFrame({
        "Required Output": [
            "Fit Score",
            "Knowledge & Skills Score",
            "Communication Score",
            "Strengths & Weaknesses",
            "Risks & Uncertainty",
            "Final Recommendation"
        ],
        "Implemented In System": [
            "Role Fit Agent + Final Recommendation Agent",
            "Knowledge & Skills Agent",
            "Communication Agent",
            "Evidence panel after analysis",
            "Risk & Uncertainty Agent",
            "Final Recommendation Agent"
        ]
    })
    st.dataframe(rubric, use_container_width=True)

    st.divider()

    st.markdown('<div class="panel"><div class="panel-header">Internal Evaluation Criteria</div>', unsafe_allow_html=True)
    role_options = jobs_df["Role"].dropna().astype(str).tolist()
    previous_role = st.session_state.selected_role
    st.session_state.selected_role = st.selectbox(
        "Select Target Role",
        role_options,
        index=role_options.index(st.session_state.selected_role) if st.session_state.selected_role in role_options else 0
    )
    if previous_role != st.session_state.selected_role:
        st.session_state.selected_questions = []

    selected_job = get_selected_job()
    st.text_input("Job Title", value=str(selected_job.get("Role", "")), disabled=True)
    st.text_area("Role Summary", value=str(selected_job.get("Role Summary", "")), height=70, disabled=True)
    st.text_area("Required Skills", value=str(selected_job.get("Required Skills", "")), height=80, disabled=True)
    st.text_area("Recommended Tools", value=str(selected_job.get("Recommended Tools", "")), height=70, disabled=True)

    st.session_state.experience_required = st.selectbox(
        "Years of Experience Required",
        ["1-2 Years", "3-5 Years", "5+ Years"],
        index=["1-2 Years", "3-5 Years", "5+ Years"].index(st.session_state.experience_required)
    )
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# Candidate Evaluation
# =========================================================
elif page == "Candidate Evaluation":
    st.title("Detailed Candidate Evaluation")
    if not st.session_state.evaluation:
        st.warning("No evaluation yet. Analyze a candidate first.")
    else:
        ev = st.session_state.evaluation
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Fit Score", f"{ev['fit_score']}%")
        c2.metric("Skills", f"{ev['skills_score']}%")
        c3.metric("Communication", f"{ev['communication_score']}%")
        c4.metric("Risk Safety", f"{ev['risk_score']}%")
        c5.metric("Recommendation", ev["recommendation"])
        st.markdown('<div class="panel"><div class="panel-header">Agent Scores</div>', unsafe_allow_html=True)
        render_agent_cards(ev["agent_scores"])
        st.markdown("</div>", unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("Evidence")
            st.write("Matched Skills:", ev["matched_skills"])
            st.write("Matched Tools:", ev["matched_tools"])
            st.write("Years Found:", ev["years_found"])
        with col_b:
            st.subheader("Gaps")
            st.write("Missing Skills:", ev["missing_skills"])
            for flag in ev["risk_flags"]:
                st.warning(flag)

# =========================================================
# Dataset Benchmark
# =========================================================
elif page == "Dataset Benchmark":
    st.title("Dataset Benchmark")
    if cv_db is None or resume_df is None:
        st.warning("Dataset was not found.")
    else:
        selected_job = get_selected_job()
        max_rows = st.slider("Number of dataset CVs to test", 5, min(50, len(resume_df)), 15)
        results = []
        for _, row in resume_df.head(max_rows).iterrows():
            candidate_id = str(row.get("Candidate ID", ""))
            cv_text = str(row.get("Resume Text", ""))
            role = str(row.get("Role", ""))
            ev = evaluate_candidate(cv_text, "", selected_job, role)
            results.append({
                "Candidate ID": candidate_id,
                "Dataset Role": role,
                "Target Role": st.session_state.selected_role,
                "Fit Score": ev["fit_score"],
                "Recommendation": ev["recommendation"],
                "Skill Match": ev["skill_score"],
                "Risk Penalty": ev["risk_penalty"]
            })
        st.dataframe(pd.DataFrame(results), use_container_width=True)

# =========================================================
# Project Overview
# =========================================================
elif page == "Project Overview":
    st.title("Agent X: Multi-Agent AI Hiring Committee")
    st.markdown("""
    <div class="panel">
        <div class="panel-header">Project Idea</div>
        <p>
        This solution evaluates candidate suitability for a selected role using CV evidence, role requirements,
        interview answers, communication quality, risk checks, and final explainable recommendation.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### What the system delivers
    - CV screening before interview
    - 65% threshold to enter interview
    - Random 4 role-aware questions
    - CV-aware follow-up style questions
    - Fit Score, Skills Score, Communication Score
    - Strengths, Weaknesses, Risks & Uncertainty
    - Final Recommendation with evidence
    - Live AI Hiring War Room
    """)

    base_agents = {
        "Role Fit Agent": 90,
        "Knowledge & Skills Agent": 85,
        "Communication Agent": 80,
        "Risk & Uncertainty Agent": 88,
        "Evidence Explanation Agent": 86,
        "Final Recommendation Agent": 90,
    }
    render_agent_cards(base_agents)
