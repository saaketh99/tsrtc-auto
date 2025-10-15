import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://tgsrtclogistics.co.in/TSRTC/"
CONSIGNMENT_NUMBER = input("Enter consignment number: ").strip()
CONS_FIELD_SELECTOR = (By.ID, "awbNos")
SUBMIT_BUTTON_SELECTOR = (By.CSS_SELECTOR, "a.btn-tracking")
SPINNER_SELECTOR = (By.CSS_SELECTOR, "img.preloader__spinner")
TIMELINE_ITEMS_SELECTOR = (By.CSS_SELECTOR, ".contents .content")

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless=true") 
    chrome_options.add_argument("--window-size=1280,1024")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options
    )

    try:
        driver.get(URL)
        wait = WebDriverWait(driver, 20)
        cons_field = wait.until(EC.presence_of_element_located(CONS_FIELD_SELECTOR))
        cons_field.clear()
        cons_field.send_keys(CONSIGNMENT_NUMBER)
        print(f" Entered consignment number: {CONSIGNMENT_NUMBER}")
        try:
            wait.until(EC.invisibility_of_element_located(SPINNER_SELECTOR))
        except TimeoutException:
            pass 
        submit_btn = wait.until(EC.element_to_be_clickable(SUBMIT_BUTTON_SELECTOR))
        driver.execute_script("arguments[0].click();", submit_btn)
        print(" Submitted form")
        time.sleep(2)
        main_window = driver.current_window_handle
        all_windows = driver.window_handles

        for handle in all_windows:
            if handle != main_window:
                driver.switch_to.window(handle)
                break

        print(" Results ")
        wait.until(EC.presence_of_all_elements_located(TIMELINE_ITEMS_SELECTOR))
        time.sleep(1)  
        timeline_items = driver.find_elements(*TIMELINE_ITEMS_SELECTOR)

        if timeline_items:
            for item in timeline_items:
                try:
                    title = item.find_element(By.TAG_NAME, "h1").text.strip()
                    details = item.find_element(By.TAG_NAME, "p").text.strip()
                    print(f"{title} -> {details}\n")
                except Exception as e:
                    print(f" Could not parse an item: {e}")
        else:
            print(" No tracking results found.")
            print(driver.page_source[:2000])

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
