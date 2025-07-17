from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Credentials
EMAIL = "noahberdugo@gmail.com"
PASSWORD = "Cooper0809!!!"

def send_keys_when_visible(driver, locator, keys, timeout=10):
    """
    Wait for an element to be visible and then send keys to it.
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (By.TYPE, "selector")
        keys: String to send to the element
        timeout: Maximum time to wait in seconds
    
    Returns:
        WebElement if successful, None if timeout
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        element.clear()
        element.send_keys(keys)
        return element
    except TimeoutException:
        logger.error(f"Timeout: Element {locator} not visible within {timeout} seconds")
        return None

def click_when_clickable(driver, locator, timeout=10):
    """
    Wait for an element to be clickable and then click it.
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (By.TYPE, "selector")
        timeout: Maximum time to wait in seconds
    
    Returns:
        WebElement if successful, None if timeout
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
        return element
    except TimeoutException:
        logger.error(f"Timeout: Element {locator} not clickable within {timeout} seconds")
        return None

def wait_for_login_page_or_form(driver, timeout=30):
    """
    Wait until URL contains '/login/email' OR the email field is present.
    
    Args:
        driver: WebDriver instance
        timeout: Maximum time to wait in seconds
    
    Returns:
        bool: True if login page/form is ready, False otherwise
    """
    try:
        # Check if URL contains '/login/email' or email field is present
        wait = WebDriverWait(driver, timeout)
        
        # Try to wait for URL to contain '/login/email'
        try:
            wait.until(lambda d: '/login/email' in d.current_url)
            logger.info("URL contains '/login/email' - login page detected")
            return True
        except TimeoutException:
            logger.info("URL doesn't contain '/login/email', checking for email field...")
        
        # If URL check fails, try to find email field
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='email']")))
            logger.info("Email field found - login form detected")
            return True
        except TimeoutException:
            logger.info("Email field with name='email' not found, trying alternative selectors...")
        
        # Try alternative email field selectors
        email_selectors = [
            "input[type='email']",
            "input[placeholder*='email' i]",
            "input[placeholder*='Email' i]",
            "input[name*='email' i]",
            "input[name*='Email' i]"
        ]
        
        for selector in email_selectors:
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                logger.info(f"Email field found using selector: {selector}")
                return True
            except TimeoutException:
                continue
        
        logger.error("Neither URL '/login/email' nor email field found within timeout")
        return False
        
    except Exception as e:
        logger.error(f"Error waiting for login page/form: {str(e)}")
        return False

def step2_fill_login_form(driver):
    """
    Step 2: Fill email/password on login form page
    
    Args:
        driver: WebDriver instance
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Step 1: Wait until URL contains '/login/email' OR the email field is present
        logger.info("Waiting for login page or email field to be present...")
        if not wait_for_login_page_or_form(driver):
            logger.error("Login page/form not detected within timeout")
            return False
        
        # Give the form a moment to fully load
        time.sleep(2)
        
        # Step 2: Populate credentials
        logger.info("Attempting to fill email field...")
        
        # Try to find and fill email field
        email_filled = False
        email_selectors = [
            "input[name='email']",
            "input[type='email']",
            "input[placeholder*='email' i]",
            "input[placeholder*='Email' i]",
            "input[name*='email' i]",
            "input[name*='Email' i]"
        ]
        
        for selector in email_selectors:
            try:
                email_element = send_keys_when_visible(driver, (By.CSS_SELECTOR, selector), EMAIL)
                if email_element:
                    logger.info(f"Successfully filled email field using selector: {selector}")
                    email_filled = True
                    break
            except Exception as e:
                logger.debug(f"Failed to fill email with selector {selector}: {str(e)}")
                continue
        
        if not email_filled:
            logger.error("Failed to fill email field with any selector")
            return False
        
        # Fill password field
        logger.info("Attempting to fill password field...")
        password_element = send_keys_when_visible(driver, (By.CSS_SELECTOR, "input[type='password']"), PASSWORD)
        
        if not password_element:
            logger.error("Failed to fill password field")
            return False
        
        logger.info("Successfully filled password field")
        
        # Step 3: Submit the form
        logger.info("Attempting to submit the form...")
        submit_button = click_when_clickable(driver, (By.CSS_SELECTOR, "button[type='submit']"))
        
        if not submit_button:
            logger.error("Failed to click submit button")
            return False
        
        logger.info("Successfully clicked submit button")
        
        # Step 4: Optionally confirm successful login
        logger.info("Waiting for login confirmation...")
        time.sleep(3)
        
        # Check for success indicators
        success_indicators = [
            "Welcome",
            "Dashboard",
            "Profile", 
            "Logout",
            "My Account",
            "Battle"
        ]
        
        found_success = False
        for indicator in success_indicators:
            try:
                element = driver.find_element(By.XPATH, f"//*[contains(text(), '{indicator}')]")
                if element.is_displayed():
                    logger.info(f"Login success indicator found: {indicator}")
                    found_success = True
                    break
            except:
                continue
        
        # Also check if URL changed to indicate successful login
        current_url = driver.current_url
        if '/login' not in current_url or 'dashboard' in current_url.lower():
            logger.info(f"URL changed to: {current_url} - indicating successful login")
            found_success = True
        
        if found_success:
            logger.info("Login appears successful!")
            return True
        else:
            logger.warning("Login may have failed - no clear success indicators found")
            logger.info(f"Current URL: {current_url}")
            logger.info(f"Page title: {driver.title}")
            return False
            
    except Exception as e:
        logger.error(f"Unexpected error in step2_fill_login_form: {str(e)}")
        return False

# Example usage:
if __name__ == "__main__":
    # Initialize WebDriver (you'll need to set up your driver)
    # driver = webdriver.Chrome()  # or your preferred driver
    
    # Uncomment the following lines when you have a driver instance:
    # success = step2_fill_login_form(driver)
    # if success:
    #     print("Step 2 completed successfully")
    # else:
    #     print("Step 2 failed")
    # driver.quit()
    
    print("Step 2 implementation ready. Initialize a WebDriver instance and call step2_fill_login_form(driver)")
