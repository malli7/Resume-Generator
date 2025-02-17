import base64
import os
import time
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def create_driver_selenium():
    """ Initializes a Chrome WebDriver instance """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222") 
    options.add_argument("--disable-software-rasterizer")
    
    ChromeDriverManager().install()

    service = ChromeService("/nix/store/chromiumDriver-unstable/bin/chromedriver")
    return webdriver.Chrome(service=service, options=options)

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
