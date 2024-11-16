import streamlit as st
import tempfile
from pdf_reader import extract_text_from_pdf, analyze_resume_with_llama, extract_domains_from_pdf, extract_and_limit_domains, load_job_listings_from_file, analyze_resume_with_job_listings
from all_scrappers import indeed_auto_extract, naukri_auto_extract, foundit_auto_extract, generate_job_listings, get_job_listings_from_jooble
import time
# Set the title of the app
st.title('PDF Upload App')

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
if uploaded_file is not None:
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        # Write the data of the uploaded file to the temporary file
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name  # Get the path of the saved file
    
    domains = extract_domains_from_pdf(tmp_path)
    time.sleep(2) 
    resume_text = extract_text_from_pdf(tmp_path)   
else:
    # Display an instruction message if no file is uploaded
    st.info('Please upload a PDF file.')

time.sleep(2)

# Adding a dropdown menu with no initial selection
options = ["", "Indeed", "Naukri", "Foundit", "Jooble"]  # Added an empty string as the first option
choice = st.selectbox("Choose a job site", options)

if choice:
    with st.spinner(f'Processing {choice} data...'):
        st.write(f"Selected job site: {choice}")
        if choice == "Indeed":
            for i in domains:
                indeed_auto_extract(i)
                job_listings_text = load_job_listings_from_file(indeed_job_cards.txt)
        elif choice == "Naukri":
            for i in domains:
                naukri_auto_extract(i)
                job_listings_text = load_job_listings_from_file(naukri_job_cards.txt)
        elif choice == "Foundit":
            for i in domains:
                foundit_auto_extract(i)
                job_listings_text = load_job_listings_from_file(foundit_job_cards.txt)
        elif choice == "Jooble":
            generate_job_listings(domains)
        st.success('Done processing.')
        st.write("Extraction done for domain: ", i)
        time.sleep(2)
        st.write("Analyzing resume with job listings...")
        analyzed_output = analyze_resume_with_job_listings(resume_text, job_listings_text)
        st.write(analyzed_output)
else:
    st.write("Please select a job site to proceed.")

    