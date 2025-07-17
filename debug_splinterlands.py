from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

SPLINTERLANDS_URL = "https://splinterlands.com"

def debug_splinterlands():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(SPLINTERLANDS_URL)
    wait = WebDriverWait(driver, 30)
    
    print("🔍 Analyzing page structure...")
    
    # Wait for page to load
    time.sleep(5)
    
    # Accept cookies banner if present
    try:
        cookie_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept All') or contains(text(), 'Accept') or contains(text(), 'OK')]")))
        cookie_btn.click()
        print("✅ Clicked cookie banner")
        time.sleep(2)
    except:
        print("ℹ️  No cookie banner found")
        pass
    
    # Debug: Print page title and current URL
    print(f"Page title: {driver.title}")
    print(f"Current URL: {driver.current_url}")
    
    # Debug: Look for all buttons on the page
    print("\n🔍 All buttons found:")
    buttons = driver.find_elements(By.TAG_NAME, "button")
    for i, button in enumerate(buttons):
        try:
            text = button.text.strip()
            classes = button.get_attribute("class")
            id_attr = button.get_attribute("id")
            visible = button.is_displayed()
            print(f"Button {i+1}: text='{text}', classes='{classes}', id='{id_attr}', visible={visible}")
        except:
            pass
    
    # Debug: Look for all links that might be login buttons
    print("\n🔍 All links found:")
    links = driver.find_elements(By.TAG_NAME, "a")
    for i, link in enumerate(links):
        try:
            text = link.text.strip()
            href = link.get_attribute("href")
            classes = link.get_attribute("class")
            visible = link.is_displayed()
            if any(word in text.lower() for word in ['login', 'sign', 'log']):
                print(f"Link {i+1}: text='{text}', href='{href}', classes='{classes}', visible={visible}")
        except:
            pass
    
    # Debug: Look for elements with login-related text
    print("\n🔍 Elements containing 'login' text:")
    try:
        login_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Login') or contains(text(), 'LOG IN') or contains(text(), 'Sign in') or contains(text(), 'Sign In')]")
        for i, elem in enumerate(login_elements):
            try:
                text = elem.text.strip()
                tag = elem.tag_name
                classes = elem.get_attribute("class")
                id_attr = elem.get_attribute("id")
                visible = elem.is_displayed()
                print(f"Element {i+1}: tag='{tag}', text='{text}', classes='{classes}', id='{id_attr}', visible={visible}")
            except:
                pass
    except Exception as e:
        print(f"Error finding login elements: {e}")
    
    # Debug: Look for common login button selectors
    print("\n🔍 Testing common login selectors:")
    selectors = [
        ("CSS", ".login-button"),
        ("CSS", ".button-login"),
        ("CSS", "[data-testid='login-button']"),
        ("CSS", "#login-button"),
        ("CSS", ".btn-login"),
        ("CSS", ".login-btn"),
        ("XPATH", "//button[contains(@class, 'login')]"),
        ("XPATH", "//a[contains(@class, 'login')]"),
        ("XPATH", "//button[contains(text(), 'Login')]"),
        ("XPATH", "//a[contains(text(), 'Login')]"),
        ("XPATH", "//button[contains(text(), 'Sign in')]"),
        ("XPATH", "//a[contains(text(), 'Sign in')]"),
    ]
    
    for selector_type, selector in selectors:
        try:
            if selector_type == "CSS":
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
            else:
                elements = driver.find_elements(By.XPATH, selector)
            
            if elements:
                print(f"✅ Found {len(elements)} elements with {selector_type} selector: {selector}")
                for i, elem in enumerate(elements):
                    try:
                        text = elem.text.strip()
                        visible = elem.is_displayed()
                        print(f"  Element {i+1}: text='{text}', visible={visible}")
                    except:
                        pass
            else:
                print(f"❌ No elements found with {selector_type} selector: {selector}")
        except Exception as e:
            print(f"❌ Error with {selector_type} selector {selector}: {e}")
    
    # Keep browser open for manual inspection
    print("\n🔍 Browser will stay open for 30 seconds for manual inspection...")
    time.sleep(30)
    
    driver.quit()

if __name__ == "__main__":
    debug_splinterlands()
