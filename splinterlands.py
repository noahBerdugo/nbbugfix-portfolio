# ✅ Script for Splinterlands Automation (Improved login flow — correct fields)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import logging, sys, time

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

EMAIL = "noahberdugo@gmail.com"
PASSWORD = "Cooper0809!!!"
SPLINTERLANDS_URL = "https://splinterlands.com"

def splinterlands():
    logging.info("Starting Splinterlands Automation")
    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(SPLINTERLANDS_URL)
        wait = WebDriverWait(driver, 30)
        logging.info("Successfully navigated to Splinterlands")

        # Accept cookies banner if present
        try:
            cookie_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept All')]")))
            cookie_btn.click()
            logging.info("Accepted cookies banner")
            time.sleep(1)
        except TimeoutException:
            logging.info("No cookies banner found - continuing")
        except Exception as e:
            logging.exception("Error handling cookies banner: %s", str(e))

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
                logging.info("Successfully clicked Login button")
            else:
                raise NoSuchElementException("Login button not found with any selector")
        except (TimeoutException, NoSuchElementException) as e:
            logging.exception("Login button not found on main page: %s", str(e))
            return
        except Exception as e:
            logging.exception("Unexpected error clicking login button: %s", str(e))
            return

        # Wait for login modal and enter credentials
        try:
            modal = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class*='modal']")))
            logging.info("Login modal appeared")
            
            email_input = modal.find_element(By.XPATH, ".//input[@type='text' or @name='Username or Email' or @placeholder='Email']")
            password_input = modal.find_element(By.XPATH, ".//input[@type='password' or @name='password']")
            
            email_input.clear()
            email_input.send_keys(EMAIL)
            password_input.clear()
            password_input.send_keys(PASSWORD)
            logging.info("Filled login credentials")
            
            submit_btn = modal.find_element(By.XPATH, ".//button[contains(text(), 'Login') or contains(text(), 'LOG IN') or contains(text(), 'Sign in')]")
            submit_btn.click()
            logging.info("Clicked login submit button")
        except TimeoutException:
            logging.exception("Login modal not found or took too long to appear")
            return
        except NoSuchElementException as e:
            logging.exception("Login form elements not found: %s", str(e))
            return
        except Exception as e:
            logging.exception("Unexpected error filling login form: %s", str(e))
            return

        try:
            wait.until(EC.presence_of_element_located((By.ID, "main-container")))
            logging.info("Successfully logged into Splinterlands")
        except TimeoutException:
            logging.exception("Login verification failed - main container not found")
            return
        except Exception as e:
            logging.exception("Unexpected error during login verification: %s", str(e))
            return

        # Main game loop
        while True:
            try:
                # Check for daily quest or battle button
                quest_btn = driver.find_elements(By.XPATH, "//button[contains(text(), 'Claim Reward')]")
                for btn in quest_btn:
                    try:
                        btn.click()
                        logging.info("Claimed quest reward")
                    except Exception as e:
                        logging.exception("Error clicking quest reward button: %s", str(e))
            except Exception as e:
                logging.exception("Error in main game loop: %s", str(e))
            
            time.sleep(600)  # check every 10 minutes
            
    except WebDriverException as e:
        logging.exception("WebDriver error in Splinterlands automation: %s", str(e))
    except Exception as e:
        logging.exception("Unexpected error in Splinterlands automation: %s", str(e))
    finally:
        if driver:
            driver.quit()
            logging.info("Browser closed")


if __name__ == "__main__":
    splinterlands()

# =============================
# This version explicitly scopes to login modal to find fields.
# More robust for dynamically generated modals.
# EMAIL and PASSWORD already set.
# [Click here to try a new GPT!](https://f614.short.gy/Code)
