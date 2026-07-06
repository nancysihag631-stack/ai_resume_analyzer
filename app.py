import streamlit as st
import PyPDF2
from analyzer import ResumeAnalyzer

# Application Layout Directives
st.set_page_config(page_title="Enterprise Resume Profiler", page_icon="🎯", layout="wide")

def parse_pdf_stream(file_stream) -> str:
    """Extracts raw string contents safely from an uploaded PDF stream object."""
    try:
        pdf_reader = PyPDF2.PdfReader(file_stream)
        return "".join([page.extract_text() or "" for page in pdf_reader.pages])
    except Exception as e:
        st.error(f"Failed to cleanly process document stream: {str(e)}")
        return ""

ROLE_TEMPLATES = {
    "Custom (Paste your own Job Description)": "",
    "Data Analyst Intern": "Looking for an intern skilled in Python, SQL, Tableau, Excel, data cleaning, and statistical analysis. Great communication and teamwork required.",
    "Frontend Developer Intern": "Seeking a developer intern fluent in JavaScript, React, HTML, CSS, Git, and responsive engineering layout. Experience working in an Agile environment is a plus.",
    "Cloud/DevOps Intern": "Position requires knowledge of AWS cloud technologies, Linux architecture, Docker containers, basic API systems, and problem-solving skills."
}

# --- RENDER WEB PORTAL UI ---
st.title("AI Resume Diagnostic Engine 🎯")
st.caption("Clean, production-grade screening pipeline for student portfolio evaluation tracks.")
st.markdown("---")

with st.sidebar:
    st.header("1. Assets Upload")
    uploaded_file = st.file_uploader("Upload Resume (PDF format)", type=["pdf"])
    
    st.header("2. Target Profile")
    selected_role = st.selectbox("Select Target Track Role:", list(ROLE_TEMPLATES.keys()))
    jd_input = st.text_area(
        label="Job Profile Requirements Data:", 
        value=ROLE_TEMPLATES[selected_role] if selected_role != "Custom (Paste your own Job Description)" else "", 
        height=200
    )

# Primary Interaction Execution Block
if st.button("Run Deep Profile Diagnostics", type="primary"):
    if not uploaded_file or not jd_input.strip():
        st.warning("Please verify that a PDF asset has been uploaded and a valid profile description is supplied.")
    else:
        with st.spinner("Executing structural parser and similarity matching passes..."):
            # 1. Parse File Content
            extracted_text = parse_pdf_stream(uploaded_file)
            
            if extracted_text.strip():
                # 2. Compute Analytics via Backend Class
                engine = ResumeAnalyzer(extracted_text, jd_input)
                match_score = engine.calculate_match_score()
                missing_hard, missing_soft = engine.extract_keyword_gaps()
                compliance_checks = engine.check_structural_compliance()
                tone_status, verb_count = engine.evaluate_phrasing_tone()
                density_msg, density_color = engine.get_readability_metrics()
                blueprints = engine.generate_project_roadmaps(missing_hard)
                
                st.success("Telemetry Diagnostics Complete!")
                
                # --- LAYOUT ROW 1: CORE TELEMETRY METRICS ---
                m_col1, m_col2, m_col3 = st.columns(3)
                m_col1.metric("Overall Alignment Score", f"{match_score}%")
                m_col2.metric("Action Verb Tone", tone_status)
                m_col3.metric("Detected Action Tokens", f"{verb_count} words")
                
                # Render alerting framework for layout text density
                if density_color == "green": st.info(f"📊 **ATS Page-Density:** {density_msg}")
                elif density_color == "orange": st.warning(f"⚠️ **ATS Page-Density:** {density_msg}")
                else: st.error(f"🚨 **ATS Page-Density:** {density_msg}")
                    
                st.markdown("---")
                
                # --- LAYOUT ROW 2: STRUCTURAL COMPLIANCE FLAGS ---
                st.subheader("📋 Mandatory Layout Architecture Verification")
                comp_cols = st.columns(len(compliance_checks))
                for idx, (section, exists) in enumerate(compliance_checks.items()):
                    if exists:
                        comp_cols[idx].success(f"✅ {section}")
                    else:
                        comp_cols[idx].error(f"❌ {section}")
                            
                st.markdown("---")
                
                # --- LAYOUT ROW 3: WORD MATRIX GAPS ---
                g_col1, g_col2 = st.columns(2)
                with g_col1:
                    st.subheader("💡 Missing Hard Tools / Core Tech")
                    if missing_hard:
                        st.caption(", ".join([f"`{s}`" for s in missing_hard]))
                    else:
                        st.write("✅ Technical skill keywords match target criteria perfectly.")
                with g_col2:
                    st.subheader("🤝 Missing Professional / Behavioral Tags")
                    if missing_soft:
                        st.caption(", ".join([f"`{s}`" for s in missing_soft]))
                    else:
                        st.write("✅ Behavioral traits criteria completely covered.")
                
                st.markdown("---")
                
                # --- LAYOUT ROW 4: PROJECT BREAKOUT BLUEPRINTS ---
                st.subheader("🛠️ Custom Portfolio Building Roadmap")
                st.write("To maximize your matching weight for this internship role, our engineering rules suggest building one of these project architectures to display on your GitHub profile:")
                
                if blueprints:
                    for tech, descriptive_roadmap in blueprints:
                        with st.expander(f"Project Architecture to close gap: **{tech}**"):
                            st.write(f"**Action Blueprint:** {descriptive_roadmap}")
                            st.caption("Once built, reference this project directly under your 'Projects' header to eliminate the ATS keyword gap automatically.")
                else:
                    st.info("No major tool gaps found. Perfect alignment detected on core tracks.")