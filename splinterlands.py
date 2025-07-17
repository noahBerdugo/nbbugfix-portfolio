# ✅ Script for Splinterlands Automation (Improved login flow — correct fields)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging, sys, time

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

EMAIL = "noahberdugo@gmail.com"
PASSWORD = "Cooper0809!!!"
SPLINTERLANDS_URL = "https://splinterlands.com"

def splinterlands():
    logging.info("Starting Splinterlands Automation")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(SPLINTERLANDS_URL)
    wait = WebDriverWait(driver, 30)

    # Accept cookies banner if present
    try:
        cookie_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept All')]")))
        cookie_btn.click()
        time.sleep(1)
    except:
        pass

    # Wait for and click Login button (more robust)
    try:
        # First try to find the "LOG IN" button specifically
        login_btns = driver.find_elements(By.XPATH, "//button[contains(text(), 'LOG IN')]")
        if not login_btns:
            # Fallback to other login button variations
            login_btns = driver.find_elements(By.XPATH, "//button[contains(text(), 'LOGIN') or contains(text(), 'Login') or contains(text(), 'Log in') or contains(text(), 'Sign in')]")
        if not login_btns:
            # Try CSS selectors as fallback
            login_btns = driver.find_elements(By.CSS_SELECTOR, ".login-button, .button-login")
        if login_btns:
            # Wait for the button to be clickable
            wait.until(EC.element_to_be_clickable(login_btns[0]))
            driver.execute_script("arguments[0].click();", login_btns[0])
            print("✅ Clicked Login button")
        else:
            raise Exception("Login button not found")
    except Exception as e:
        print(f"❌ Could not find or click Login button: {e}")
        driver.quit()
        return

    # Wait for login modal and enter credentials
    try:
        modal = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class*='modal']")))
        email_input = modal.find_element(By.XPATH, ".//input[@type='text' or @name='Username or Email' or @placeholder='Email']")
        password_input = modal.find_element(By.XPATH, ".//input[@type='password' or @name='password']")
        email_input.clear()
        email_input.send_keys(EMAIL)
        password_input.clear()
        password_input.send_keys(PASSWORD)
        submit_btn = modal.find_element(By.XPATH, ".//button[contains(text(), 'Login') or contains(text(), 'LOG IN') or contains(text(), 'Sign in')]")
        submit_btn.click()
    except Exception as e:
        print(f"❌ Could not fill login form: {e}")
        driver.quit()
        return

    try:
        wait.until(EC.presence_of_element_located((By.ID, "main-container")))
        print("✅ Logged into Splinterlands")
    except:
        print("❌ Login may have failed.")
        driver.quit()
        return

    while True:
        try:
            # Check for daily quest or battle button
            quest_btn = driver.find_elements(By.XPATH, "//button[contains(text(), 'Claim Reward')]")
            for btn in quest_btn:
                btn.click()
                print("Claimed quest reward")
        except:
            pass
        time.sleep(600)  # check every 10 minutes


if __name__ == "__main__":
    splinterlands()

# =============================
# This version explicitly scopes to login modal to find fields.
# More robust for dynamically generated modals.
# EMAIL and PASSWORD already set.
# [Click here to try a new GPT!](https://f614.short.gy/Code)
