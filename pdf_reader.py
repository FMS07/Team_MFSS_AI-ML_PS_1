import os
import PyPDF2
from groq import Groq
import streamlit as st

# API Key for Groq
GROQ_API_KEY = "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"  # Replace with your actual API key

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    """
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def analyze_resume_with_llama(text):
    """
    Analyze the extracted text using the Groq API.
    """
    client = Groq(api_key=GROQ_API_KEY)

    # Prompt for analysis
    prompt = f"""
    Analyze the following resume text and identify key domains related to the skills, projects, internships, and interests mentioned.
    Limit the identified domains to 6 critically most important ones. Provide only the domain names without any numbers, descriptions, or attached explanations.

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

# def extract_domains_from_pdf(pdf_path):
#     """
#     Function to analyze PDF and extract important domains.
#     """
#     if not os.path.exists(pdf_path):
#         raise FileNotFoundError("The specified PDF file does not exist.")

#     print("Analyzing PDF to extract important domains...")
#     resume_text = extract_text_from_pdf(pdf_path)
#     analysis = analyze_resume_with_llama(resume_text)
#     domains = extract_and_limit_domains(analysis, max_domains=15)

#     print("\nImportant Domains Identified:")
#     for domain in domains:
#         print(f"- {domain}")

#     return domains
def extract_domains_from_pdf(pdf_path):
    """
    Function to analyze PDF and extract important domains.
    """
    if not os.path.exists(pdf_path):
        st.error("The specified PDF file does not exist.")
        return []  # Return an empty list or appropriate response on error

    # Using Markdown to make the text bold and st.header for the header
    #st.markdown("*Analyzing PDF to extract important domains...**", unsafe_allow_html=True)
    # Alternatively, use st.header for larger header text
    #st.header("Analyzing PDF to extract important domains...")
    
    resume_text = extract_text_from_pdf(pdf_path)
    analysis = analyze_resume_with_llama(resume_text)
    domains = extract_and_limit_domains(analysis, max_domains=15)

    # if domains:
    #     st.write("Important Domains Identified:")
    #     for domain in domains:
    #         st.write(f"{domain}")
    # else:
    #     st.write("No important domains could be identified.")

    return domains

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

# # Run PDF analysis and extract domains
# pdf_path = "/content/Shreyank_Srinivasan_Harisha_Resume_.pdf"  # Replace with your actual PDF path
# domains = extract_domains_from_pdf(pdf_path)

def load_job_listings_from_file(file_path="job_listings.txt"):
    """
    Load job listings from a text file.
    """
    with open(file_path, 'r') as file:
        return file.read()

def analyze_resume_with_job_listings(resume_text, job_listings_text):
    """
    Analyze the resume and job listings using the Groq API.
    """
    client = Groq(api_key=GROQ_API_KEY)

    # Prompt for categorization
    prompt = f"""
    You are an AI job analysis assistant. Below is a resume and a list of job listings.
    Your tasks are:
    1. For each job listing, analyze the skills required based on the job description.
    2. Compare the required skills with the resume.
    3. For each job listing, identify:
        - Strengths: The skills the user possesses that match the job requirements.
        - Areas of Improvement: The skills the user lacks based on the job requirements.
    4. Categorize each job into:
        - Must Apply
        - Good Fit
        - Neutral
        - Doesn't Align
    5. Provide the output in a beautified, structured format, clearly listing:
        - Domain
        - Job Title
        - Company
        - Category
        - Strengths
        - Areas of Improvement
        - Reason for Categorization
    6. Make sure all the job listings are covered.

    Resume:
    {resume_text}

    Job Listings:
    {job_listings_text}
    """
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None,
    )

    analysis_result = ""
    for chunk in completion:
        chunk_content = chunk.choices[0].delta.content or ""
        analysis_result += chunk_content

    # Save the result to a text file
    output_file = "job_analysis_results.txt"
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(analysis_result)

    #st.write("Job analysis results saved to:", output_file)

# def display_jobs_by_category(content):
#     """
#     Displays job analysis results in a structured format using Streamlit.
    
#     Args:
#         content (str): The content of the job analysis results
#     """
#     try:
#         # Split into main categories
#         categories = {}
#         current_category = None
#         current_job = None
        
#         # Skip the header and get to the main content
#         lines = content.split('\n')
#         for line in lines:
#             line = line.strip()
#             if not line:
#                 continue
                
#             # Main category (Web Development, Data Science, etc.)
#             if line.startswith('### '):
#                 current_category = line.replace('### ', '').strip()
#                 st.header(current_category)
                
#             # Job listing
#             elif line.startswith('#### '):
#                 job_title = line.replace('#### ', '').strip()
#                 st.subheader(job_title)
                
#             # Job details
#             elif line.startswith('* '):
#                 parts = line.replace('* ', '').split(': ', 1)
#                 if len(parts) == 2:
#                     key, value = parts
#                     st.markdown(f"**{key}:** {value}")
                    
#             # Add separator between jobs if needed
#             elif line.startswith('---'):
#                 st.markdown("---")
                
#     except Exception as e:
#         st.error(f"Error parsing job listings: {str(e)}")
#         st.text("Content that caused error:")
#         st.code(content)

def display_jobs_by_category(content):
    """
    Displays job analysis results in a structured format using Streamlit.
    
    Args:
        content (str): The content of the job analysis results
    """
    try:
        # Initialize variables
        current_category = None
        
        # Split into lines
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Detect categories (bold text with **)
            if line.startswith("**") and line.endswith("**"):
                current_category = line.replace("**", "").strip()
                st.header(current_category)

            # Detect job titles (numbered list)
            elif line[0].isdigit() and line[1] == ".":
                job_title = line.split('. ', 1)[1].strip()
                st.subheader(job_title)

            # Detect job details (lines starting with `* `)
            elif line.startswith('* '):
                parts = line.replace('* ', '').split(': ', 1)
                if len(parts) == 2:
                    key, value = parts
                    st.markdown(f"**{key}:** {value}")

            # Add separator between job sections if needed
            elif line.startswith('---'):
                st.markdown("---")

    except Exception as e:
        st.error(f"Error parsing job listings: {str(e)}")
        st.text("Content that caused error:")
        st.code(content)