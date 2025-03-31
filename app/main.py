import streamlit as st
import pandas as pd
import fitz  # PyMuPDF for PDFs
import docx
import spacy
import matplotlib.pyplot as plt
import seaborn as sns
import re
import ast  # ✅ Add here (NOT inside any if/elif block)


# ✅ Must be the first command
st.set_page_config(page_title="AI Resume Matcher", layout="wide")

# ✅ Load spaCy NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


# ✅ Function to load datasets
@st.cache_data
def load_data():
    resumes = pd.read_csv("../data/resumes_dataset_powerful.csv")
    jobs = pd.read_csv("../data/job_descriptions_powerful.csv")
    matches = pd.read_csv("../output/match_results.csv")
    return resumes, jobs, matches

resumes, jobs, matches = load_data()

# ✅ Define Navigation Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🔍 Job Matching", "📂 Upload Resume", "📊 Insights Dashboard"])

# ✅ Define a Rich Skill Set
def load_skills():
    return set([
        # ✅ Programming & Data Science
        "python", "r", "java", "c++", "c#", "javascript", "sql",
        "pandas", "numpy", "matplotlib", "scikit-learn", "tensorflow", "pytorch",
        "machine learning", "deep learning", "natural language processing", "nlp",
        "computer vision", "data structures", "algorithms",

        # ✅ Data Engineering & BI Tools
        "big data", "hadoop", "spark", "airflow",
        "power bi", "tableau", "excel", "google analytics",

        # ✅ Cloud & DevOps
        "aws", "azure", "gcp", "docker", "kubernetes", "git", "ci/cd",
        
        # ✅ Business & Analytics
        "business intelligence", "stakeholder communication", "data visualization",
        "a/b testing", "data storytelling", "agile", "scrum"
    ])

# ✅ Improved Resume Processing Function
def extract_resume_details(text):
    doc = nlp(text.lower())  # Convert to lowercase for better matching
    predefined_skills = load_skills()  # Load predefined skills list
    
    # Extract words from text and match with known skills
    detected_skills = list(set([token.text for token in doc if token.text in predefined_skills]))

    # Extract experience (checking for numeric values before "years" or "months")
    experience_years = 0
    for i, token in enumerate(doc):
        if token.text.lower() in ["year", "years", "month", "months"]:
            prev_token = doc[i - 1] if i > 0 else None
            if prev_token and prev_token.text.isdigit():
                experience_years += int(prev_token.text)  # Extract number of years/months
    
    # Extract education
    education_keywords = ["bachelor", "master", "phd", "mba", "b.sc", "m.sc", "btech", "mtech", "degree"]
    education = [ent.text for ent in doc.ents if ent.label_ == "EDUCATION" or any(keyword in ent.text.lower() for keyword in education_keywords)]

    return detected_skills, experience_years, education


# ✅ 1️⃣ Job Matching Page (Polished UI)
if page.strip() == "🔍 Job Matching":
    st.title("💼 AI-Powered Resume Screening & Matching Tool")
    st.markdown("Use this interactive app to explore top candidates for roles using skills, experience, and AI-matching scores.")

    with st.sidebar:
        selected_job = st.selectbox("🎯 Select a Job Title", jobs["Job Title"].unique())
        top_n = st.slider("📌 Number of Candidates to Show", min_value=5, max_value=50, value=10)

    job_filtered = jobs[jobs["Job Title"] == selected_job].iloc[0]
    job_id = job_filtered["JobID"]

    st.markdown("---")
    st.subheader(f"📋 Job Overview: {selected_job}")
    st.markdown(f"""
    - 🏢 **Company:** {job_filtered['Company']}
    - 🌐 **Industry:** {job_filtered['Industry']}
    - 📍 **Location:** {job_filtered['Location']}
    - 📝 **Description:** {job_filtered['Description']}
    """)

    job_matches = matches[matches["JobID"] == job_id]
    top_candidates = job_matches.merge(resumes, on="CandidateID")
    top_candidates = top_candidates.sort_values(by="Final Match Score", ascending=False).head(top_n)

    st.markdown("### 🔝 Top Matching Candidates")
    cols = st.columns(2)

    for i, (_, row) in enumerate(top_candidates.iterrows()):
        with cols[i % 2]:
            st.markdown(f"#### {row['Name']} — *{row['Desired Role']}*")
            st.progress(row["Final Match Score"] / 100)
            st.write(f"✅ **Match Score:** `{row['Final Match Score']}%`")
            st.write(f"🎯 **Skill Match:** `{row['Skill Match %']}%`")
            st.write(f"📚 **Experience Match:** `{row['Experience Fit %']}%`")
            st.write(f"📍 **Location:** {row['Location']}")
            st.write(f"🕒 **Availability:** {row['Availability']}")
            st.write(f"🎓 **Education:** {row['Education']}")
            st.write(f"📜 **Certifications:** {row['Certifications']}")
            st.markdown("---")
           
           



elif page.strip() == "📂 Upload Resume":
    st.title("📂 Smart Resume Upload & AI Job Matcher for Data Roles")
    st.markdown(
        "🚀 This tool is designed specifically for **Data/Analytics job roles**.\n"
        "Upload a resume to extract skills, experience, and match with data-focused opportunities!"
    )

    uploaded_file = st.file_uploader("📎 Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

    if uploaded_file:
        st.success("✅ File uploaded successfully!")

        # Domain clarification (for transparency)
        domain_type = st.radio("What role is this resume targeting?", ["📊 Data/Analytics Roles", "🌐 Other Roles"])

        # Extract resume text
        if uploaded_file.type == "application/pdf":
            pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            resume_text = "\n".join([page.get_text("text") for page in pdf])
        else:
            doc = docx.Document(uploaded_file)
            resume_text = "\n".join([para.text for para in doc.paragraphs])

        # Extract insights
        detected_skills, experience, education = extract_resume_details(resume_text)

        # Display Resume Info
        st.subheader("🎯 Extracted Resume Insights")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("🔑 **Top Skills**")
            st.write(", ".join(detected_skills) if detected_skills else "Not detected")

        with col2:
            st.markdown("📅 **Experience**")
            st.write(f"{experience} years (Approx)")

        with col3:
            st.markdown("🎓 **Education**")
            st.write(", ".join(education) if education else "Not detected")

        # 👉 If data domain is selected
        if "Data/Analytics" in domain_type:
            st.subheader("🚀 Best Matched Job Roles")

            def match_resume_to_jobs(detected_skills):
                job_scores = []
                for _, job in jobs.iterrows():
                    job_skills = job["Required Skills"]
                    if isinstance(job_skills, str):
                        try:
                            job_skills = ast.literal_eval(job_skills)
                        except:
                            job_skills = []
                    matched = set(skill.lower() for skill in detected_skills).intersection(
                        set(skill.lower() for skill in job_skills)
                    )
                    score = len(matched) / len(job_skills) if job_skills else 0
                    job_scores.append((job["Job Title"], job["Company"], round(score * 100, 2)))
                return sorted(job_scores, key=lambda x: x[2], reverse=True)[:3]

            top_jobs = match_resume_to_jobs(detected_skills)

            for title, company, score in top_jobs:
                st.markdown(f"**💼 {title}** at *{company}* — 🎯 **Match Score:** {score}%")

        else:
            # 📝 ATS feedback for non-data roles
            st.warning("⚠️ Our matching algorithm is optimized for data-related roles only.")
            st.subheader("📋 ATS Resume Scorecard")
            word_count = len(resume_text.split())
            char_count = len(resume_text)
            bullet_points = resume_text.count("•") + resume_text.count("- ")

            st.write(f"📝 **Word Count:** {word_count}")
            st.write(f"🔢 **Characters:** {char_count}")
            st.write(f"📌 **Bullet Points Found:** {bullet_points}")

            st.markdown("### ✅ Tips to Improve Resume:")
            st.markdown("- Add technical/data skills (e.g., SQL, Python, Excel)")
            st.markdown("- Use bullet points with measurable achievements")
            st.markdown("- Keep it between 450–750 words")
            st.markdown("- Fix any grammar/spelling issues")

# ✅ 3️⃣ Insights Dashboard
elif page.strip() == "📊 Insights Dashboard":
    st.title("📊 Job Market Insights & AI Analysis")
    st.markdown("📈 Explore trends in job postings, required skills, and candidate distribution. *(Only for Data-related Roles)*")

    # ✅ 1. Job Distribution by Role
    st.subheader("📌 Job Distribution by Role")
    job_counts = jobs["Job Title"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(y=job_counts.index, x=job_counts.values, ax=ax, palette="coolwarm")
    ax.set_xlabel("Number of Job Openings")
    ax.set_ylabel("Job Role")
    st.pyplot(fig)

    # ✅ 2. Most In-Demand Skills
    st.subheader("💡 Most In-Demand Skills")

    import ast  # make sure this is at the top of your file

    def parse_skills(row):
        if isinstance(row, list):
            return row
        elif isinstance(row, str):
            try:
                return ast.literal_eval(row)
            except:
                return [s.strip() for s in row.split(",")]
        return []

    all_skills = jobs["Required Skills"].dropna().apply(parse_skills)
    flat_skills = pd.Series([skill for skills in all_skills for skill in skills])
    skill_counts = flat_skills.value_counts().head(10)

    if not skill_counts.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(y=skill_counts.index, x=skill_counts.values, ax=ax, palette="viridis")
        ax.set_xlabel("Number of Jobs Requiring Skill")
        ax.set_ylabel("Skill")
        st.pyplot(fig)
    else:
        st.warning("⚠️ Could not load skill chart: No valid skill data available.")

    # ✅ 3. Candidate Education Level Distribution
    st.subheader("🎓 Candidate Education Level")
    education_counts = resumes["Education"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(y=education_counts.index, x=education_counts.values, ax=ax, palette="pastel")
    ax.set_xlabel("Number of Candidates")
    ax.set_ylabel("Education Level")
    st.pyplot(fig)
