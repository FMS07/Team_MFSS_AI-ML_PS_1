import os
import streamlit as st
import PyPDF2
from groq import Groq

# Set your API key for the Groq client here
API_KEY = "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"  # Replace with your actual Groq API key

def extract_text_from_pdf(pdf_file):
    """
    Extracts text from a PDF file.
    """
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def analyze_resume_with_llama(text):
    """
    Analyze the extracted text using the Groq API.
    """
    client = Groq(api_key=API_KEY)

    # Prompt for analysis
    prompt = f"""
    Analyze the following resume text and identify key domains related to the skills, projects, internships, and interests mentioned.
    Limit the identified domains to a maximum of 10 to 15 most important ones. Provide only the domain names without any numbers, descriptions, or attached explanations.

    Resume Text: {text}
    """
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=512,
        top_p=1,
        stream=True,
        stop=None,
    )

    # Gather output
    analysis_result = ""
    for chunk in completion:
        chunk_content = chunk.choices[0].delta.content or ""
        analysis_result += chunk_content

    return analysis_result

def extract_and_limit_domains(analysis_result, max_domains=15):
    """
    Extract important domains from the analysis result and limit to a maximum count.
    """
    domains = []
    lines = analysis_result.split("\n")

    # Extract domains and clean them
    for line in lines:
        domain = line.strip()  # Strip leading/trailing spaces
        if domain and len(domain.split()) <= 5:  # Ensure concise domain names (up to 5 words)
            domains.append(domain)

    # Limit the number of domains
    return domains[:max_domains]

# Streamlit UI
st.title("Resume Analyzer")

uploaded_file = st.file_uploader("Upload your PDF Resume", type=["pdf"])

if uploaded_file is not None:
    # Display file upload confirmation
    st.success(f"Uploaded file: {uploaded_file.name}")

    # Extract text from PDF
    with st.spinner("Extracting text from your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    # Analyze the resume using Groq API
    with st.spinner("Analyzing your resume..."):
        analysis_result = analyze_resume_with_llama(resume_text)

    # Extract and display important domains
    important_domains = extract_and_limit_domains(analysis_result, max_domains=15)
    st.header("Important Domains Identified:")
    for domain in important_domains:
        st.write(f"- {domain}")

    # Add Job buttons
    st.header("Job Search Platforms:")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Job-Joogle"):
            st.info("Feature coming soon: Job-Joogle")
    
    with col2:
        if st.button("Job-Indeed"):
            st.info("Feature coming soon: Job-Indeed")
    
    with col3:
        if st.button("Job-Naukri"):
            st.info("Feature coming soon: Job-Naukri")
