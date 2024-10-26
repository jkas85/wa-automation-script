import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

directory_to_watch = os.path.join(os.path.dirname(__file__), "pdf")
pdf_file = "sample.pdf"
whatsapp_group_name = "test12345"

def setup_whatsapp():
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=./User_Data")  # Keeps you logged in between sessions
    driver = webdriver.Chrome(options=options)
    driver.get("https://web.whatsapp.com")

    print("Scan the QR code to login to WhatsApp Web")
    # this line "waits" for you to scan the QR code
    time.sleep(20)  
    return driver


def send_file_via_whatsapp(driver, file_path):
    # Locate the group chat
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true" and @data-tab="3"]')
    search_box.click()
    search_box.send_keys(whatsapp_group_name)
    time.sleep(2)
    search_box.send_keys(Keys.ENTER)
    time.sleep(1)

    # Attach the file
    attachment_box = driver.find_element(By.XPATH, '//span[@data-icon="plus"]')
    attachment_box.click()
    
    file_input = driver.find_element(By.XPATH, '//input[@accept="*"]')
    file_input.send_keys(file_path)
    

    # this line "waits" for the file to be uploaded to whatsapp. You might adjust this line based on the file size and upload speed
    time.sleep(5)
    send_button = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
    send_button.click()
    print(f"Sent updated file: {file_path} to {whatsapp_group_name}.")

class PDFUpdateHandler(FileSystemEventHandler):
    def __init__(self, driver):
        self.driver = driver
        self.last_modified = None

    def on_modified(self, event):
        if event.src_path.endswith(pdf_file):
            current_mod_time = os.path.getmtime(event.src_path)
            
            # Check if this is a new modification
            if not self.last_modified or self.last_modified < current_mod_time:
                self.last_modified = current_mod_time
                print(f"Detected update for {pdf_file}. Sending via WhatsApp...")
                send_file_via_whatsapp(self.driver, event.src_path)

# Main Function to Set Up Monitoring
def monitor_directory():
    driver = setup_whatsapp()  # Set up WhatsApp Web in browser

    event_handler = PDFUpdateHandler(driver)
    observer = Observer()
    observer.schedule(event_handler, directory_to_watch, recursive=False)
    
    observer.start()
    print(f"Monitoring directory: {directory_to_watch} for changes to {pdf_file}...")

    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    driver.quit()

if __name__ == "__main__":
    monitor_directory()
