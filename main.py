import streamlit as st
import pdfplumber
import time

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


JOB_ROLES = {
    "AI Engineer": [
        "Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
        "NumPy", "Pandas", "SQL", "Git", "AWS", "Docker", "REST API", "Data Science"
    ],
    "ML Engineer": [
        "Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
        "NumPy", "Pandas", "SQL", "Git", "Docker", "Kubernetes", "AWS", "Data Science"
    ],
    "Data Scientist": [
        "Python", "SQL", "Machine Learning", "Pandas", "NumPy", "Data Science",
        "Power BI", "Excel", "TensorFlow", "Communication", "Deep Learning"
    ],
    "Data Analyst": [
        "SQL", "Excel", "Power BI", "Python", "Pandas", "Data Science",
        "Communication", "NumPy"
    ],
    "Fullstack Developer": [
        "HTML", "CSS", "JavaScript", "React", "Node.js", "MongoDB", "SQL",
        "PostgreSQL", "Git", "GitHub", "REST API", "TypeScript", "Docker", "Flask"
    ],
    "Web Developer": [
        "HTML", "CSS", "JavaScript", "React", "Vue.js", "Node.js", "Git",
        "GitHub", "REST API", "TypeScript", "Angular"
    ],
    "UI/UX Developer": [
        "HTML", "CSS", "JavaScript", "Figma", "Adobe XD", "React", "Communication",
        "Git", "GitHub", "TypeScript"
    ],
    "App Developer": [
        "Java", "Kotlin", "Flutter", "React Native", "Git", "GitHub", "REST API",
        "SQL", "Firebase", "Android Studio"
    ],
    "Game Developer": [
        "C++", "C#", "Unity", "Unreal Engine", "Git", "GitHub", "Python",
        "Communication", "3D Modeling"
    ],
    "Backend Developer": [
        "Python", "Java", "Node.js", "Flask", "Django", "SQL", "MongoDB",
        "PostgreSQL", "REST API", "GraphQL", "Docker", "Kubernetes", "Git", "AWS"
    ],
    "DevOps Engineer": [
        "Docker", "Kubernetes", "AWS", "Azure", "Linux", "Git", "GitHub",
        "CI/CD", "Python", "REST API"
    ],
    "Cloud Engineer": [
        "AWS", "Azure", "Docker", "Kubernetes", "Linux", "Python", "SQL", "Git"
    ],
}

# Master skill list = union of all role skills (for text scanning)
SKILLS_LIST = sorted(set(skill for skills in JOB_ROLES.values() for skill in skills))

st.markdown("""
<style>
.main-title{ text-align:center; font-size:45px; font-weight:bold; color:#1976D2; }
.sub-title{ text-align:center; color:gray; font-size:18px; }
.skill-found { background-color: #d4edda; color: #155724; padding: 8px 12px; border-radius: 5px; margin: 3px 0; border-left: 4px solid #28a745; }
.skill-missing { background-color: #f8d7da; color: #721c24; padding: 8px 12px; border-radius: 5px; margin: 3px 0; border-left: 4px solid #dc3545; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">📄 AI Resume Analyzer</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Upload, Pick a Job Role & Analyze Instantly</p>', unsafe_allow_html=True)
st.divider()

st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose Page", ["Resume Analyzer", "About"])

if page == "Resume Analyzer":

    st.header("📤 Upload Your Resume")

    uploaded_file = st.file_uploader("Choose PDF Resume", type=["pdf"])

    st.subheader("🎯 Select Target Job Role")
    job_role = st.selectbox(
        "Type to search or pick a job role",
        options=list(JOB_ROLES.keys()),
        index=0,
        help="Start typing to search, e.g. 'AI' or 'Web'"
    )

    if uploaded_file is None:
        st.info("👈 Upload your PDF resume to start")

    else:
        st.success(f"✅ File: {uploaded_file.name}  |  🎯 Role: {job_role}")

        # ANALYZE BUTTON - User clicks to process
        if st.button("🔍 Analyze Resume Now", use_container_width=True, type="primary"):

            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()

            try:
                # Step 1: Extract text
                status_text.info("⏳ Step 1/3: Reading PDF...")
                progress_bar.progress(25)

                text = ""
                with pdfplumber.open(uploaded_file) as pdf:
                    for page in pdf.pages:
                        try:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"
                        except:
                            pass

                if not text.strip():
                    st.error("❌ Could not extract text from PDF")
                    status_text.empty()
                    progress_bar.empty()
                else:
                    # Step 2: Extract skills based on selected job role
                    status_text.info(f"⏳ Step 2/3: Scanning skills for {job_role}...")
                    progress_bar.progress(60)

                    required_skills = JOB_ROLES[job_role]

                    found = []
                    missing = []
                    text_lower = text.lower()

                    for skill in required_skills:
                        if skill.lower() in text_lower:
                            found.append(skill)
                        else:
                            missing.append(skill)

                    # Step 3: Display results
                    status_text.info("⏳ Step 3/3: Preparing results...")
                    progress_bar.progress(100)
                    time.sleep(0.5)

                    status_text.empty()
                    progress_bar.empty()
                    st.success(f"✅ Analysis Complete for {job_role}!")

                    st.divider()

                    # RESULTS
                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("📊 ATS Score")

                        total = len(found) + len(missing)
                        score = int((len(found) / total) * 100) if total > 0 else 0

                        st.metric(f"Match for {job_role}", f"{score}%")
                        st.caption(f"Found {len(found)}/{total} required skills")

                        st.subheader("✅ Skills Found")

                        if found:
                            for skill in found:
                                st.markdown(f'<div class="skill-found">✔ {skill}</div>', unsafe_allow_html=True)
                        else:
                            st.warning("No matching skills detected")

                    with col2:
                        st.subheader("❌ Missing Skills")

                        if missing:
                            for skill in missing:
                                st.markdown(f'<div class="skill-missing">✘ {skill}</div>', unsafe_allow_html=True)
                        else:
                            st.success("🎉 All required skills found!")

                        st.divider()

                        st.subheader("💡 Top Recommendations")

                        if missing:
                            top_missing = missing[:5]
                            for skill in top_missing:
                                st.write(f"✓ Learn / Add **{skill}** to your resume")
                        else:
                            st.success(f"You're excellent for {job_role}! 🚀")

                    st.divider()

                    # PREVIEW
                    st.subheader("📝 Full Resume Text")
                    with st.expander("Click to expand", expanded=False):
                        st.text_area("Extracted Text", text, height=300, disabled=True)

            except Exception as e:
                status_text.empty()
                progress_bar.empty()
                st.error(f"❌ Error: {str(e)}")

else:
    st.title("About Project")
    st.markdown("---")
    st.subheader("🔥 AI Resume Analyzer v7.0")

    st.write("""
    **Fast, job-role-aware resume analysis!**

    ✨ **Key Features:**
    - 1-click PDF upload
    - Searchable job role dropdown (AI Engineer, Fullstack Dev, ML Engineer,
      Web Dev, UI/UX Dev, App Dev, Data Scientist, Data Analyst, Game Dev & more)
    - Role-specific required skills matching
    - "Analyze" button workflow
    - 3-step progress tracking
    - ATS score based on selected role
    - Smart, role-specific recommendations

    🎯 **How It Works:**
    1. Upload your PDF resume
    2. Pick / search your target Job Role
    3. Click "Analyze Resume Now"
    4. See ATS score + found/missing skills for that role
    5. Get personalized recommendations to close the gap

    🚀 **What's New in v7.0:**
    - Job role selector added
    - Skills & scoring now role-specific instead of generic
    - Recommendations tied to the exact role you're targeting
    """)

    st.success("Ready to analyze! Upload resume → Pick role → Click Analyze ✨")