import base64
import os
import time
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
import psutil 

def create_driver_selenium():
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium"  # Explicitly set Chromium path
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222") 
    options.add_argument("--disable-software-rasterizer")
    
    
    service = ChromeService("/usr/bin/chromedriver")

    return webdriver.Chrome(service=service, options=options)

def cleanup_chromedriver_processes():
    """ Kill lingering ChromeDriver processes """
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] in ['chromedriver', 'chrome']:
            proc.kill()

def HTML_to_PDF(html_content, output_pdf_path):
    """ Converts an HTML string to a PDF file using Selenium """
    temp_html_path = "temp_resume.html"

    with open(temp_html_path, "w", encoding="utf-8") as file:
        file.write(html_content)

    FilePath = f"file:///{os.path.abspath(temp_html_path).replace(os.sep, '/')}"
    driver = create_driver_selenium()

    try:
        driver.get(FilePath)
        time.sleep(2)
        pdf_base64 = driver.execute_cdp_cmd("Page.printToPDF", {"printBackground": True})
        pdf_data = base64.b64decode(pdf_base64['data'])

        with open(output_pdf_path, "wb") as pdf_file:
            pdf_file.write(pdf_data)

        print(f"\n✅ Resume saved as PDF: {output_pdf_path}")

    finally:
        driver.quit()
        os.remove(temp_html_path)
        cleanup_chromedriver_processes()
