#naukri
#working
#note auto_login("Job","Network Engineer")
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymongo

def auto_login(jobtype,jobtitle):
    # Set up the Chrome WebDriver
    options = webdriver.ChromeOptions()
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
    # Step 2: Select "Job" in the Job Type dropdown
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

    # Step 3: Enter "web designer" in the search input field
    try:
        input_search = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Enter keyword / designation / companies"]'))
        )
        input_search.send_keys("web designer")
    except Exception as e:
        print(f"Error entering job title: {e}")

    # Step 4: Locate the search button and click it
    try:
        search_button = WebDriverWait(driver, 6).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[1]/div[3]/div[2]/div[1]/div/button'))
        )
        search_button.click()
    except Exception as e:
        print(f"Error clicking the search button: {e}")

    # Step 5: Extract the files from the search results
    try:
        file_name = jobtitle + "_cards.txt"
        # Open a file in write mode to store the results
        with open(file_name, "w", encoding="utf-8") as file:
            time.sleep(2)
            for i in range(1, 8):  # Loop through the first 7 job cards
                # Check if the specific div exists
                elements = driver.find_elements(By.XPATH, f'//*[@id="listContainer"]/div[2]/div/div[{i}]')
                
                # If elements list is empty, skip to the next iteration
                if not elements:
                    message = f"Div part not found for li[{i}], skipping...\n"
                    print(message)
                    file.write(message)
                    continue
                
                # If the element exists, extract the text
                element = elements[0]  # Since `find_elements` returns a list, take the first element
                text = f"Text for li[{i}]:\n{element.text}\n\n"
                print(text)  # Optional: still print to the console if needed
                file.write(text)  # Write the text to the file
                
    except Exception as e:
        error_message = f"Error extracting text: {e}\n"
        print(error_message)
        # Append the error to the file
        with open(file_name, "a", encoding="utf-8") as file:
            file.write(error_message)