from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def click_when_clickable(locator, timeout=10):
    """
    Wait for an element to be clickable and then click it.
    
    Args:
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

def step4_navigate_and_login(driver):
    """
    Step 4: Navigate to main page and click "LOG IN"
    
    Args:
        driver: WebDriver instance
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Step 1: Navigate to Splinterlands main page
        logger.info("Navigating to https://splinterlands.com")
        driver.get("https://splinterlands.com")
        logger.info("Successfully navigated to Splinterlands main page")
        
        # Step 2: Wait for the top-level login button and click it
        logger.info("Waiting for LOG IN button to be clickable...")
        login_button = click_when_clickable((By.XPATH, "//button[normalize-space()='LOG IN']"))
        
        if login_button:
            logger.info("Successfully clicked LOG IN button")
            return True
        else:
            logger.error("Failed to click LOG IN button - element not found or not clickable")
            return False
            
    except TimeoutException as e:
        logger.error(f"TimeoutException occurred: {str(e)}")
        logger.error("The LOG IN button was not found within the specified timeout period")
        return False
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        return False

# Example usage:
if __name__ == "__main__":
    # Initialize WebDriver (you'll need to set up your driver)
    # driver = webdriver.Chrome()  # or your preferred driver
    
    # Uncomment the following lines when you have a driver instance:
    # success = step4_navigate_and_login(driver)
    # if success:
    #     print("Step 4 completed successfully")
    # else:
    #     print("Step 4 failed")
    # driver.quit()
    
    print("Step 4 implementation ready. Initialize a WebDriver instance and call step4_navigate_and_login(driver)")
