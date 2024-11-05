import os
import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Prompt for credentials
# GOOGLE_EMAIL = os.getenv('GOOGLE_EMAIL')  # Retrieve from environment variable or set directly here
# if not GOOGLE_EMAIL:
#     GOOGLE_EMAIL = input("Enter your Google email: ")

# GOOGLE_PASSWORD = getpass.getpass("Enter your Google password: ")  # Prompt for password securely

# Setup Chrome options (optional: headless mode)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in background without GUI
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up WebDriver (replace with path to your chromedriver if needed)
service = Service("C:\\Users\\user\\chromedriver-win64\\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

# # URLs
# LOGIN_URL = 'https://www.um.edu.mt/vle/login'
BASE_URL = 'https://www.um.edu.mt/vle/course/view.php?id=88288'

# Log in with Google
# driver.get(LOGIN_URL)
wait = WebDriverWait(driver, 10)

# Locate and click the Google Sign-In button (update selector as needed)
# google_sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign in with Google')]")))
# google_sign_in_button.click()

# Switch to Google Sign-In window
# driver.switch_to.window(driver.window_handles[1])

# # Enter Google email
# email_input = wait.until(EC.visibility_of_element_located((By.ID, "identifierId")))
# email_input.send_keys(GOOGLE_EMAIL)
# email_input.send_keys(Keys.ENTER)

# # Wait and enter Google password
# password_input = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
# password_input.send_keys(GOOGLE_PASSWORD)
# password_input.send_keys(Keys.ENTER)

# Switch back to the VLE window
driver.switch_to.window(driver.window_handles[0])

# Wait until we're redirected to course content
wait.until(EC.url_contains(BASE_URL))

# Function to download files (placeholder for actual downloading logic)
def download_file(url, folder):
    file_name = os.path.join(folder, url.split('/')[-1])
    driver.get(url)
    with open(file_name, 'wb') as f:
        f.write(driver.page_source.encode())
    print(f"Downloaded {file_name}")

# Function to get PDFs and MP4s
def get_files(folder):
    os.makedirs(folder, exist_ok=True)
    links = driver.find_elements(By.TAG_NAME, 'a')
    for link in links:
        href = link.get_attribute('href')
        if href and (href.endswith('.pdf') or href.endswith('.mp4')):
            download_file(href, folder)

# Start download process
get_files('course_material')

# Close the driver
driver.quit()
