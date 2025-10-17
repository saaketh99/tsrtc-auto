import os
import time
import traceback
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

URL = "https://tgsrtclogistics.co.in/TSRTC/"
CONS_NUMBER = os.environ.get("CONS_NUMBER")

if not CONS_NUMBER:
    raise ValueError("CONS_NUMBER environment variable not set")

CONS_FIELD_SELECTOR = (By.ID, "awbNos")
SUBMIT_BUTTON_SELECTOR = (By.CSS_SELECTOR, "a.btn-tracking")
CONTENT_SELECTOR = (By.CSS_SELECTOR, ".contents .content")
DATA_SELECTOR = (By.CSS_SELECTOR, ".data")

chromedriver_autoinstaller.install()

def run_tracking():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.binary_location = os.environ.get("CHROME_BIN", "/usr/bin/google-chrome")

    driver = webdriver.Chrome(options=chrome_options)
    results = []

    try:
        driver.get(URL)
        wait = WebDriverWait(driver, 30)

       
        cons_field = wait.until(EC.presence_of_element_located(CONS_FIELD_SELECTOR))
        cons_field.clear()
        cons_field.send_keys(CONS_NUMBER)
        print(f"Entered consignment number: {CONS_NUMBER}")

        submit_btn = wait.until(EC.element_to_be_clickable(SUBMIT_BUTTON_SELECTOR))
        driver.execute_script("arguments[0].click();", submit_btn)


        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
            print("Switched to new window/tab for results.")

        try:
            wait.until(EC.visibility_of_element_located(CONTENT_SELECTOR))
        except TimeoutException:
            print("Tracking results container not found.")
            print(driver.page_source[:1500])
            return ["No tracking results found."]

        time.sleep(2)  
        content_blocks = driver.find_elements(*CONTENT_SELECTOR)

        if not content_blocks:
            print("No tracking content found.")
            return ["No tracking results found."]

        for block in content_blocks:
            try:
                data_div = block.find_element(*DATA_SELECTOR)
                title = data_div.find_element(By.TAG_NAME, "h1").text.strip()
                details = data_div.find_element(By.TAG_NAME, "p").text.strip()
                results.append(f"{title} -> {details}")
            except NoSuchElementException:
                continue

    except Exception as e:
        print("[ERROR] Exception occurred:")
        traceback.print_exc()
        return [f"Error: {str(e)}"]
    finally:
        driver.quit()

    return results if results else ["No tracking results found."]


if __name__ == "__main__":
    data = run_tracking()
    if not data:
        print("No output received.")
    else:
        print("\n===== TRACKING RESULTS =====")
        for r in data:
            print(r)
