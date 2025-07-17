from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
import logging
from twocaptcha import TwoCaptcha

# ==== CONFIGURATION ====
EMAIL = "youloltubenoahberdugo@gmail.com"
PASSWORD = "Cooper123!!"
CLAIM_INTERVAL = 60 * 60  # 1 hour in seconds
CHECK_INTERVAL = 60       # check every minute if claim fails
LOGIN_URL = "https://freebitco.in"
API_KEY = "8b068697ecb2b453be7e1d438ec9be5e"
LOG_FILE = "freebitco_bot.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)
solver = TwoCaptcha(API_KEY)

def create_driver(headless=False):
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    if headless:
        options.add_argument("--headless=new")

    service = Service()
    return webdriver.Chrome(service=service, options=options)

def click_by_coordinates(driver, x, y, delay=3):
    logger.info(f"Clicking coordinates ({x}, {y}) after {delay} seconds delay.")
    time.sleep(delay)
    webdriver.ActionChains(driver).move_by_offset(x, y).click().perform()
    webdriver.ActionChains(driver).move_by_offset(-x, -y).perform()
    time.sleep(2)

def solve_captcha(driver):
    logger.info("Attempting to locate captcha on page.")
    try:
        iframe = driver.find_element(By.CSS_SELECTOR, "iframe[src*='recaptcha']")
        sitekey = iframe.get_attribute("src").split("k=")[1].split("&")[0]
        logger.info(f"Detected sitekey: {sitekey}")
        result = solver.recaptcha(sitekey=sitekey, url=LOGIN_URL)
        driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML='{result['code']}';")
        time.sleep(2)
    except NoSuchElementException:
        logger.warning("No captcha iframe detected on page.")

def login(driver):
    try:
        driver.get(LOGIN_URL)
        wait = WebDriverWait(driver, 15)
        logger.info("Navigated to login page")

        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'NO THANKS')]"))).click()
            logger.info("Clicked 'NO THANKS' via element.")
        except TimeoutException:
            logger.warning("'NO THANKS' not detected, falling back to coordinate click.")
            click_by_coordinates(driver, 606, 440, delay=7)

        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'LOGIN')]"))).click()
            logger.info("Clicked LOGIN button")
        except TimeoutException:
            logger.exception("Login button not found on main page")
            raise

        try:
            email_input = wait.until(EC.element_to_be_clickable((By.ID, "login_form_btc_address")))
            password_input = wait.until(EC.element_to_be_clickable((By.ID, "login_form_password")))
            logger.info("Found email and password input fields")
        except TimeoutException:
            logger.exception("Email or password input fields not found on login form")
            raise

        email_input.clear()
        email_input.send_keys(EMAIL)
        password_input.clear()
        password_input.send_keys(PASSWORD)
        logger.info("Filled login credentials")

        solve_captcha(driver)

        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'LOGIN!')]"))).click()
            logger.info("Clicked LOGIN! button")
        except TimeoutException:
            logger.exception("LOGIN! button not found on login form")
            raise
        
        time.sleep(5)
        click_by_coordinates(driver, 606, 440, delay=4)
        logger.info("Login process completed")
        
    except (TimeoutException, NoSuchElementException) as e:
        logger.exception("Error during login process: %s", str(e))
        raise
    except WebDriverException as e:
        logger.exception("WebDriver error during login: %s", str(e))
        raise
    except Exception as e:
        logger.exception("Unexpected error during login: %s", str(e))
        raise

def claim_free_bitcoin(driver):
    wait = WebDriverWait(driver, 10)
    try:
        roll_button = wait.until(EC.element_to_be_clickable((By.ID, "free_play_form_button")))
        roll_button.click()
        logger.info("Claimed free Bitcoin.")
        return True
    except (NoSuchElementException, TimeoutException):
        logger.warning("Roll button not found or not interactable.")
        return False

def main():
    while True:
        driver = create_driver()
        try:
            login(driver)
            success = False
            while not success:
                try:
                    success = claim_free_bitcoin(driver)
                    if not success:
                        logger.info(f"Retrying claim in {CHECK_INTERVAL} seconds.")
                        time.sleep(CHECK_INTERVAL)
                except (TimeoutException, NoSuchElementException) as e:
                    logger.exception("Error during claiming Bitcoin: %s", str(e))
            logger.info(f"Claim successful. Closing browser and waiting {CLAIM_INTERVAL} seconds for next cycle.")
        except (TimeoutException, NoSuchElementException) as e:
            logger.exception("Error in main loop: %s", str(e))
        finally:
            driver.quit()
            time.sleep(CLAIM_INTERVAL)

if __name__ == "__main__":
    main()
