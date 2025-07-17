# 🔷 CryptoIdleMiner Script
# =============================

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('coinclicker.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

EMAIL = "your_email@example.com"
PASSWORD = "your_password"
URL = "https://crypto-idle-miner.com/play"


def crypto_idle_miner():
    logger.info("Starting CryptoIdleMiner automation")
    driver = None
    try:
        driver = webdriver.Chrome(service=Service())
        driver.get(URL)
        wait = WebDriverWait(driver, 20)
        logger.info("Successfully navigated to CryptoIdleMiner")

        # Login form
        try:
            email_field = wait.until(EC.element_to_be_clickable((By.NAME, "email")))
            email_field.send_keys(EMAIL)
            logger.info("Filled email field")
        except TimeoutException:
            logger.exception("Email field not found on login page")
            return
        except Exception as e:
            logger.exception("Error filling email field: %s", str(e))
            return

        try:
            password_field = driver.find_element(By.NAME, "password")
            password_field.send_keys(PASSWORD)
            logger.info("Filled password field")
        except NoSuchElementException:
            logger.exception("Password field not found on login page")
            return
        except Exception as e:
            logger.exception("Error filling password field: %s", str(e))
            return

        try:
            sign_in_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
            sign_in_btn.click()
            logger.info("Clicked Sign In button")
        except NoSuchElementException:
            logger.exception("Sign In button not found on login page")
            return
        except Exception as e:
            logger.exception("Error clicking Sign In button: %s", str(e))
            return

        # Wait for dashboard
        try:
            wait.until(EC.presence_of_element_located((By.ID, "dashboard")))
            logger.info("Successfully logged into CryptoIdleMiner")
        except TimeoutException:
            logger.exception("Dashboard not found - login may have failed")
            return
        except Exception as e:
            logger.exception("Error waiting for dashboard: %s", str(e))
            return

        # Main collection loop
        while True:
            try:
                # Check for any claim/collect buttons and click
                collect_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Collect')]")
                if collect_buttons:
                    for btn in collect_buttons:
                        try:
                            btn.click()
                            logger.info("Collected rewards")
                        except Exception as e:
                            logger.exception("Error clicking collect button: %s", str(e))
                else:
                    logger.info("No collect buttons found")
            except Exception as e:
                logger.exception("Error in main collection loop: %s", str(e))
            
            time.sleep(300)  # check every 5 minutes
            
    except WebDriverException as e:
        logger.exception("WebDriver error in CryptoIdleMiner automation: %s", str(e))
    except Exception as e:
        logger.exception("Unexpected error in CryptoIdleMiner automation: %s", str(e))
    finally:
        if driver:
            driver.quit()
            logger.info("Browser closed")
