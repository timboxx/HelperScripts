import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re



# Set up Chrome options to attach to the debugging port
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# Initialize the WebDriver to use the existing session
driver = webdriver.Chrome(options=chrome_options)

# Base URL for course content
BASE_URL = 'https://www.um.edu.mt/vle/course/view.php?id=88287'
driver.get(BASE_URL)
time.sleep(2)  # Allow time for the page to load

# Base folder to save downloaded files
BASE_FOLDER = 'course_material'

# Function to sanitize folder names
def sanitize_folder_name(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name)

# Function to download files with requests
def download_file(url, folder):
    os.makedirs(folder, exist_ok=True)
    file_name = os.path.join(folder, url.split('/')[-1])
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(file_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {file_name}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}. Error: {e}")

# Function to download files from the current resource page
def download_files_from_resource_page(folder):
    time.sleep(2)
    links = driver.find_elements(By.TAG_NAME, 'a')
    for link in links:
        href = link.get_attribute('href')
        if href and (".pdf" in href or ".mp4" in href):  # Only download PDFs and MP4s
            download_file(href, folder)

# Main function to handle traversal and downloading
def traverse_and_download():
    while True:
        # Fetch the list of subdirectory links each time to avoid stale element issues
        subdirs = driver.find_elements(By.CSS_SELECTOR, 'a.courseindex-link')
        for i in range(len(subdirs)):
            # Refresh the subdirectory elements and click each one individually
            subdirs = driver.find_elements(By.CSS_SELECTOR, 'a.courseindex-link')
            subdir = subdirs[i]
            subdir_name = sanitize_folder_name(subdir.text.strip())  # Sanitize folder name
            
            # Click the link to navigate to the subdirectory
            driver.execute_script("arguments[0].click();", subdir)
            time.sleep(2)  # Allow time for the page to load
            
            # Download files on the resource page
            subdir_folder = os.path.join(BASE_FOLDER, subdir_name)
            download_files_from_resource_page(subdir_folder)
            
            # Go back to the main page
            driver.back()
            time.sleep(2)  # Allow time for the main page to load again
            
        break  # Exit after one full loop through all subdirectories

# Start the download process
traverse_and_download()

# Close the driver when done
driver.quit()
