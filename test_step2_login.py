#!/usr/bin/env python3
"""
Test file for Step 2 - Fill email/password on login form page
This integrates with Step 4 to provide a complete login flow test
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging

# Import our implementations
from step4_navigate_and_login import step4_navigate_and_login
from step2_fill_login_form import step2_fill_login_form

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_driver(headless=False):
    """
    Initialize ChromeDriver with webdriver-manager.
    
    Args:
        headless (bool): Whether to run Chrome in headless mode
        
    Returns:
        webdriver.Chrome: Initialized Chrome driver instance
    """
    try:
        logger.info("🔍 Initializing ChromeDriver...")
        
        # Set up Chrome options
        options = webdriver.ChromeOptions()
        
        if headless:
            options.add_argument("--headless=new")
            logger.info("  - Running in headless mode")
        
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Initialize Chrome service with webdriver-manager
        service = Service(ChromeDriverManager().install())
        
        # Create and configure driver
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()
        
        # Hide webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        logger.info("✅ ChromeDriver initialized successfully")
        return driver
        
    except Exception as e:
        logger.error(f"❌ Error during driver initialization: {e}")
        raise

def test_complete_login_flow():
    """
    Test the complete login flow: Step 4 (navigate & click login) + Step 2 (fill form)
    """
    driver = None
    try:
        # Initialize driver
        driver = get_driver(headless=False)
        
        logger.info("🚀 Starting complete login flow test...")
        
        # Step 4: Navigate to main page and click LOG IN
        logger.info("📍 Executing Step 4: Navigate and click LOG IN...")
        step4_success = step4_navigate_and_login(driver)
        
        if not step4_success:
            logger.error("❌ Step 4 failed - cannot proceed to Step 2")
            return False
        
        logger.info("✅ Step 4 completed successfully")
        
        # Wait a moment for navigation
        time.sleep(2)
        
        # Step 2: Fill email/password on login form
        logger.info("📍 Executing Step 2: Fill login form...")
        step2_success = step2_fill_login_form(driver)
        
        if not step2_success:
            logger.error("❌ Step 2 failed")
            return False
        
        logger.info("✅ Step 2 completed successfully")
        
        # Keep browser open for inspection
        logger.info("🔍 Keeping browser open for 30 seconds for inspection...")
        time.sleep(30)
        
        logger.info("🎉 Complete login flow test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error during complete login flow test: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        if driver:
            driver.quit()
            logger.info("🚪 Browser closed")

def test_step2_only():
    """
    Test only Step 2 - assumes login form is already displayed
    (This would be used when you manually navigate to the login form first)
    """
    driver = None
    try:
        # Initialize driver
        driver = get_driver(headless=False)
        
        logger.info("🚀 Starting Step 2 only test...")
        logger.info("⚠️  Make sure to manually navigate to the login form first!")
        
        # Navigate to splinterlands (user should manually click login)
        driver.get("https://splinterlands.com")
        
        # Wait for user to manually click login
        input("Press Enter after you've clicked the LOGIN button and the login form is displayed...")
        
        # Step 2: Fill email/password on login form
        logger.info("📍 Executing Step 2: Fill login form...")
        step2_success = step2_fill_login_form(driver)
        
        if not step2_success:
            logger.error("❌ Step 2 failed")
            return False
        
        logger.info("✅ Step 2 completed successfully")
        
        # Keep browser open for inspection
        logger.info("🔍 Keeping browser open for 30 seconds for inspection...")
        time.sleep(30)
        
        logger.info("🎉 Step 2 only test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error during Step 2 only test: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        if driver:
            driver.quit()
            logger.info("🚪 Browser closed")

if __name__ == "__main__":
    print("Select test mode:")
    print("1. Complete login flow (Step 4 + Step 2)")
    print("2. Step 2 only (manual login button click)")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        success = test_complete_login_flow()
    elif choice == "2":
        success = test_step2_only()
    else:
        print("Invalid choice. Exiting.")
        exit(1)
    
    if success:
        print("✅ Test completed successfully!")
    else:
        print("❌ Test failed!")
