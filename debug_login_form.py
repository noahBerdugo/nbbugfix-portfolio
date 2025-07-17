# Debug script for Splinterlands login form
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def debug_login_form():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print("🔍 Debugging login form page...")
        driver.get("https://splinterlands.com/login/email")
        wait = WebDriverWait(driver, 10)
        
        # Wait for page to load
        time.sleep(3)
        
        print(f"Page title: {driver.title}")
        print(f"Current URL: {driver.current_url}")
        
        # Find all input fields
        inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"\n🔍 Found {len(inputs)} input fields:")
        for i, input_elem in enumerate(inputs, 1):
            try:
                input_type = input_elem.get_attribute("type")
                input_name = input_elem.get_attribute("name")
                input_id = input_elem.get_attribute("id")
                input_placeholder = input_elem.get_attribute("placeholder")
                input_class = input_elem.get_attribute("class")
                is_visible = input_elem.is_displayed()
                
                print(f"Input {i}: type='{input_type}', name='{input_name}', id='{input_id}', placeholder='{input_placeholder}', class='{input_class}', visible={is_visible}")
            except Exception as e:
                print(f"Input {i}: Error getting attributes - {e}")
        
        # Find all buttons
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"\n🔍 Found {len(buttons)} buttons:")
        for i, button in enumerate(buttons, 1):
            try:
                button_text = button.text
                button_class = button.get_attribute("class")
                button_id = button.get_attribute("id")
                button_type = button.get_attribute("type")
                is_visible = button.is_displayed()
                is_enabled = button.is_enabled()
                
                print(f"Button {i}: text='{button_text}', class='{button_class}', id='{button_id}', type='{button_type}', visible={is_visible}, enabled={is_enabled}")
            except Exception as e:
                print(f"Button {i}: Error getting attributes - {e}")
        
        # Find all forms
        forms = driver.find_elements(By.TAG_NAME, "form")
        print(f"\n🔍 Found {len(forms)} forms:")
        for i, form in enumerate(forms, 1):
            try:
                form_action = form.get_attribute("action")
                form_method = form.get_attribute("method")
                form_class = form.get_attribute("class")
                form_id = form.get_attribute("id")
                
                print(f"Form {i}: action='{form_action}', method='{form_method}', class='{form_class}', id='{form_id}'")
            except Exception as e:
                print(f"Form {i}: Error getting attributes - {e}")
        
        # Look for specific login-related elements
        print("\n🔍 Looking for specific login elements...")
        
        email_selectors = [
            "input[type='email']",
            "input[name='email']",
            "input[placeholder*='email']",
            "input[placeholder*='Email']",
            "input[id*='email']",
            "input[name*='username']",
            "input[placeholder*='username']",
            "input[placeholder*='Username']"
        ]
        
        password_selectors = [
            "input[type='password']",
            "input[name='password']",
            "input[placeholder*='password']",
            "input[placeholder*='Password']",
            "input[id*='password']"
        ]
        
        submit_selectors = [
            "button[type='submit']",
            "input[type='submit']",
            "button:contains('Login')",
            "button:contains('Sign In')",
            "button:contains('Log In')",
            ".login-button",
            ".submit-button"
        ]
        
        for selector in email_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"✅ Found email field with selector: {selector}")
                    break
            except:
                pass
        
        for selector in password_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"✅ Found password field with selector: {selector}")
                    break
            except:
                pass
        
        for selector in submit_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"✅ Found submit button with selector: {selector}")
                    break
            except:
                pass
        
        print("\n🔍 Page source preview (first 1000 characters):")
        print(driver.page_source[:1000])
        
        print("\n🔍 Keeping browser open for 30 seconds for manual inspection...")
        time.sleep(30)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    debug_login_form()
