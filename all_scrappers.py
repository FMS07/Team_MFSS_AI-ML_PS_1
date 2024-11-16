from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import http.client
import json

# Jooble API Configuration
JOOBLE_API_KEY = ""  # Replace with your actual API key
JOOBLE_HOST = "jooble.org"

def manage_job_cards_file():
    file_paths = ["indeed_job_cards.txt", "naukri_job_cards.txt", "foundit_job_cards.txt"]
    for i in range(len(file_paths)):
        file_path = file_paths[i]
        # Check if the file exists
        if os.path.exists(file_path):
            os.remove(file_path)  # Delete the existing file
        # Create a fresh file
        with open(file_path, 'w') as file:
            print(f"Created a new file: {file_path}")

manage_job_cards_file()

def foundit_auto_extract(jobtitle):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.foundit.in/")

    # Step 1: Enter job title
    try:
        input_search = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="heroSectionDesktop-skillsAutoComplete--input"]'))
        )
        input_search.send_keys(jobtitle)
        time.sleep(1)
    except Exception as e:
        print(f"Error entering job title: {e}")


    # Step 2: Enter location
    try:
        loc_ = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="heroSectionDesktop-locationAutoComplete--input"]'))
        )
        loc_.send_keys("Bangalore")
        time.sleep(1)
    except Exception as e:
        print(f"Error entering location: {e}")
    
    # Step 3: Click the search button
    try:
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="searchForm"]/div/button'))
        )
        search_button.click()
    except Exception as e:
        print(f"Error clicking the search button: {e}")
    
    # Step 4: Extract the text from the job cards
    try:
        # File to save the results
        time.sleep(1)
        file_name = "foundit_job_cards.txt"
        with open(file_name, "a", encoding="utf-8") as file:
            time.sleep(2)
            file.write(f"--->The below are the job descriptions for {jobtitle}\n\n")
            for i in range(2, 4):  # Loop through the first 7 elements (adjust range if needed)
                # Find elements using XPath
                elements = driver.find_elements(By.XPATH, f'//*[@id="srpContent"]/div[1]/div/div[{i}]/div')
                
                # Check if elements exist
                if not elements:
                    message = f"Div part not found for div[{i}], skipping...\n"
                    print(message)
                    continue
                
                # Extract the text of the first element
                element = elements[0]  # Take the first element in the list
                text = f"{element.text}\n\n"
                print(text)  # Print to console for debugging
                file.write(text)  # Write to the file
            file.write(f"<--Done listing the jobs for {jobtitle}\n\n")
            
    except Exception as e:
        error_message = f"Error extracting text: {e}\n"
        print(error_message)
    driver.quit()

def naukri_auto_extract(jobtitle):
    # Set up the Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    # Navigate to the Naukri login page
    driver.get("https://www.naukri.com/mnjuser/homepage")

    # Locate the email input field and enter your email
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="usernameField"]'))
    )
    email_field.send_keys("shreyanksh.btech22@rvu.edu.in")  # Replace with your actual email

    # Locate the password input field and enter your password
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="passwordField"]'))
    )
    password_field.send_keys("Testing@12")  # Replace with your actual password

    # Locate the login button and click it
    try:
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and contains(text(),"Login")]'))
        )
        login_button.click()
    except TimeoutException:
        print("Login button not found or not clickable")

    # Locate the job search input field and enter the job title
    try:
        input_search_ = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[1]/div[3]/div[2]/div[1]/div'))
        )
    except Exception as e:
        print(f"Error locating the search input: {e}")

    # Locate the search button and click it
    try:
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[1]/div[3]/div[2]/div[1]/div/button/span[1]'))
        )
        search_button.click()
    except Exception as e:
        print(f"Error clicking the search button: {e}")
    # Step 1: Select "Job" in the Job Type dropdown
    try:
        job_type_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[1]/div[3]/div[2]/div[1]/div/div/div[2]/div/div/span'))
        )
        job_type_dropdown.click()
        
        # Select "Job" option from the dropdown
        job_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="sa-dd-scrolljobType"]/div[1]/ul/li[2]'))
        )
        job_option.click()
    except Exception as e:
        print(f"Error selecting job type: {e}")

    # Step 2: Enter the job title
    try:
        input_search = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Enter keyword / designation / companies"]'))
        )
        input_search.send_keys(jobtitle)
    except Exception as e:
        print(f"Error entering job title: {e}")

    # Step 3: Enter the location
    try:
        search_button = WebDriverWait(driver, 6).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[1]/div[3]/div[2]/div[1]/div/button'))
        )
        search_button.click()
    except Exception as e:
        print(f"Error clicking the search button: {e}")

    # Step 4: Extract the files from the search results
    try:
        time.sleep(1)
        file_name = "naukri_job_cards.txt"
        # Open a file in write mode to store the results
        with open(file_name, "a", encoding="utf-8") as file:
            time.sleep(2)
            file.write(f"--->The below are the job descriptions for {jobtitle}\n\n")
            for i in range(1, 3):  # Loop through the first 7 job cards
                # Check if the specific div exists
                elements = driver.find_elements(By.XPATH, f'//*[@id="listContainer"]/div[2]/div/div[{i}]')
                
                # If elements list is empty, skip to the next iteration
                if not elements:
                    message = f"Div part not found for li[{i}], skipping...\n"
                    print(message)
                    continue
                
                # If the element exists, extract the text
                element = elements[0]  # Since `find_elements` returns a list, take the first element
                text = f"{element.text}\n\n"
                print(text)  # Optional: still print to the console if needed
                file.write(text)  # Write the text to the file
            file.write(f"<--Done listing the jobs for {jobtitle}\n\n")  
                
    except Exception as e:
        error_message = f"Error extracting text: {e}\n"
        print(error_message)
    driver.quit()
    
def indeed_auto_extract(jobtitle):
    # Set up the Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    # Navigate to the indeed page
    driver.get("https://in.indeed.com/")

    # Step 3: Enter "web designer" in the search input field
    try:
        input_search = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="text-input-what"]'))
        )
        input_search.click()
        input_search.send_keys(jobtitle)
        time.sleep(1)
    except Exception as e:
        print(f"Error entering job title: {e}")

    # Step 4: Enter "Bangalore" in the location input field

    try:
        location = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="text-input-where"]'))
        )
        location.send_keys("Bangalore")
        time.sleep(1)
    except Exception as e:
        print(f"Error entering job title: {e}")
        
    # Step 4: Locate the search button and click it
    try:
        search_button = WebDriverWait(driver, 6).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="jobsearch"]/div/div[2]/button'))
        )
        search_button.click()
    except Exception as e:
        print(f"Error clicking the search button: {e}")

    # Step 5: Geting the job descriptions
    try:
        time.sleep(2)
        file_name = "indeed_job_cards.txt"
        # Open a file in write mode to store the results
        with open(file_name, "a", encoding="utf-8") as file:
            time.sleep(1)
            file.write(f"--->The below are the job descriptions for {jobtitle}\n\n")
            for i in range(1, 3):  # Loop through the first 7 job cards
                # Check if the specific div exists
                elements = driver.find_elements(By.XPATH, f'//*[@id="mosaic-provider-jobcards"]/ul/li[{i}]/div/div/div/div/div/div')
                
                # If elements list is empty, skip to the next iteration
                if not elements:
                    message = f"Div part not found for li[{i}], skipping...\n"
                    print(message)
                    continue
                
                # If the element exists, extract the text
                element = elements[0]  # Since `find_elements` returns a list, take the first element
                text = f"{element.text}\n\n"
                print(text)  # Optional: still print to the console if needed
                file.write(text)  # Write the text to the file
            file.write(f"<--Done listing the jobs for {jobtitle}\n\n")    
    except Exception as e:
        error_message = f"Error extracting text: {e}\n"
        print(error_message)
    driver.quit()
    
def get_job_listings_from_jooble(keywords, location="bangalore", max_results=2):
    """
    Get limited job listings from Jooble API using keywords and location.
    """
    connection = http.client.HTTPSConnection(JOOBLE_HOST)
    headers = {"Content-type": "application/json"}

    # Prepare the body of the request
    body = json.dumps({"keywords": keywords, "location": location})

    # Make the API request
    connection.request("POST", f"/api/{JOOBLE_API_KEY}", body, headers)
    response = connection.getresponse()

    # Process the response
    if response.status == 200:
        data = response.read()
        job_data = json.loads(data)
        return job_data.get("jobs", [])[:max_results]  # Limit results
    else:
        print(f"Error: {response.status} {response.reason}")
        return None

def generate_job_listings(domains):
    """
    Takes a list of domains and fetches job listings for each domain from Jooble.
    """
    print("Fetching Job Listings from Jooble API...\n")
    for domain in domains:
        listings = get_job_listings_from_jooble(domain, max_results=2)
        print(f"Jobs for domain '* {domain}':")
        if listings:
            for job in listings:
                # Clean and format the job details
                job_title = job.get("title", "N/A")
                job_company = job.get("company", "N/A")
                job_location = job.get("location", "N/A")
                job_link = job.get("link", "N/A")

                print(f"- {job_title} at {job_company}")
                print(f"  Location: {job_location}")
                print(f"  Link: {job_link}\n")
        else:
            print("  No jobs found.\n")
