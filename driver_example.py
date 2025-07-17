#!/usr/bin/env python3
"""
Example demonstrating the get_driver function with proper error handling and clean exit.
This shows how to use the robust ChromeDriver initialization function.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import sys
import time

def get_driver(headless=False):
    """
    Initialize ChromeDriver with webdriver-manager.
    
    Args:
        headless (bool): Whether to run Chrome in headless mode
        
    Returns:
        webdriver.Chrome: Initialized Chrome driver instance
        
    Exits:
        System exit if driver initialization fails
    """
    try:
        print("🔍 Initializing ChromeDriver...")
        
        # Set up Chrome options
        options = webdriver.ChromeOptions()
        
        if headless:
            options.add_argument("--headless=new")
            print("  - Running in headless mode")
        
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
        
        print("✅ ChromeDriver initialized successfully")
        return driver
        
    except WebDriverException as e:
        print(f"❌ WebDriver error during initialization: {e}")
        print("💡 Please ensure Chrome browser is installed and up to date")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Unexpected error during driver initialization: {e}")
        print("💡 Please check your internet connection and try again")
        sys.exit(1)

def test_driver():
    """Test the get_driver function with a simple webpage."""
    # Initialize driver (will exit if it fails)
    driver = get_driver(headless=False)
    
    try:
        print("🔍 Testing driver with example.com...")
        
        # Navigate to a test page
        driver.get("https://example.com")
        print("✅ Successfully navigated to example.com")
        
        # Wait for page to load and find title
        wait = WebDriverWait(driver, 10)
        title_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        print(f"✅ Page title: {title_element.text}")
        
        # Keep browser open for a few seconds
        print("⏳ Keeping browser open for 5 seconds...")
        time.sleep(5)
        
    except TimeoutException:
        print("❌ Timeout waiting for page elements")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        
    finally:
        print("🔍 Closing browser...")
        driver.quit()
        print("✅ Browser closed successfully")

def test_headless_driver():
    """Test the get_driver function in headless mode."""
    # Initialize headless driver
    driver = get_driver(headless=True)
    
    try:
        print("🔍 Testing headless driver with httpbin.org...")
        
        # Navigate to a test page
        driver.get("https://httpbin.org/user-agent")
        print("✅ Successfully navigated to httpbin.org")
        
        # Get the page source to verify it worked
        page_source = driver.page_source
        if "user-agent" in page_source.lower():
            print("✅ Headless mode working correctly")
        else:
            print("❌ Headless mode test failed")
            
    except Exception as e:
        print(f"❌ Error during headless test: {e}")
        
    finally:
        print("🔍 Closing headless browser...")
        driver.quit()
        print("✅ Headless browser closed successfully")

if __name__ == "__main__":
    print("=" * 50)
    print("Testing get_driver function")
    print("=" * 50)
    
    # Test regular mode
    print("\n1. Testing regular mode:")
    test_driver()
    
    # Test headless mode
    print("\n2. Testing headless mode:")
    test_headless_driver()
    
    print("\n✅ All tests completed successfully!")
