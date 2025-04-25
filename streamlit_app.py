import streamlit as st
import pandas as pd
from resume_parser import extract_text_from_pdf, extract_candidate_data
from utils import get_keywords_from_jd, calculate_match_score
from database import insert_candidate_data

st.set_page_config(page_title="AI Resume Screening", layout="wide")

st.title("🧠 AI-Powered Resume Screening for HR")
st.markdown("Upload resumes and enter a job description to screen candidates using AI")

# --- Job Description Input ---
job_description = st.text_area("📄 Enter Job Description Here")

# --- File Upload ---
uploaded_files = st.file_uploader("📤 Upload Resume PDFs", type="pdf", accept_multiple_files=True)

# --- Main Logic ---
resume_data = []

if uploaded_files and job_description:
    jd_keywords = get_keywords_from_jd(job_description)

    with st.spinner("🔍 Screening resumes..."):
        for file in uploaded_files:
            text = extract_text_from_pdf(file)
            data = extract_candidate_data(text, jd_keywords)
            data["match_score"] = round(calculate_match_score(text, job_description) * 100, 2)
            data["filename"] = file.name

            try:
                insert_candidate_data(data)
            except Exception as e:
                st.error(f"DB error: {e}")

            resume_data.append(data)

    # --- Show Results ---
    if resume_data:
        df = pd.DataFrame(resume_data)

        # --- Filter by Score ---
        st.subheader("🔎 Filter by Match Score")
        min_score = st.slider("Show candidates with score above:", 0, 100, 50)
        filtered_df = df[df["match_score"] >= min_score]

        # --- Display Filtered Results with Preview ---
        st.subheader("📊 Resume Screening Results")

# Sort by match score
        filtered_df = filtered_df.sort_values(by="match_score", ascending=False)

        for idx, row in filtered_df.iterrows():
          with st.expander(f"{row['filename']} | Score: {row['match_score']}%"):
            st.markdown(f"**Name:** {row['name']}")
            st.markdown(f"**Email:** {row['email']}")
            st.markdown(f"**Phone:** {row['phone']}")
            st.markdown(f"**Matched Keywords:** `{row['matched_keywords']}`")
            st.markdown("---")
            st.markdown("#### 📄 Full Resume Text")
            st.write(row["full_resume"])


        # --- Download Option (Optional) ---
        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Filtered Results", data=csv, file_name="filtered_candidates.csv", mime="text/csv")

elif not uploaded_files:
    st.info("Please upload at least one resume PDF.")
elif not job_description.strip():
    st.info("Please enter a job description.")
