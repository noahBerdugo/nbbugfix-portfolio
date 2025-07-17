# Enhanced debug script for Splinterlands login form with dynamic content waiting
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def detailed_form_debug():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print("🔍 Enhanced debugging of login form page...")
        driver.get("https://splinterlands.com/login/email")
        wait = WebDriverWait(driver, 15)
        
        print(f"Initial page title: {driver.title}")
        print(f"Initial URL: {driver.current_url}")
        
        # Wait for dynamic content to load
        print("\n⏳ Waiting for dynamic form content...")
        time.sleep(5)
        
        # Try to wait for specific form elements
        try:
            email_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='email']")))
            print("✅ Email field found via presence_of_element_located")
        except:
            print("❌ Email field not found via presence_of_element_located")
        
        try:
            password_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
            print("✅ Password field found via presence_of_element_located")
        except:
            print("❌ Password field not found via presence_of_element_located")
        
        # Now check all input fields again
        inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"\n🔍 Found {len(inputs)} input fields after waiting:")
        for i, input_elem in enumerate(inputs, 1):
            try:
                input_type = input_elem.get_attribute("type")
                input_name = input_elem.get_attribute("name")
                input_id = input_elem.get_attribute("id")
                input_placeholder = input_elem.get_attribute("placeholder")
                input_class = input_elem.get_attribute("class")
                is_visible = input_elem.is_displayed()
                is_enabled = input_elem.is_enabled()
                
                print(f"Input {i}: type='{input_type}', name='{input_name}', id='{input_id}', placeholder='{input_placeholder}', class='{input_class}', visible={is_visible}, enabled={is_enabled}")
            except Exception as e:
                print(f"Input {i}: Error getting attributes - {e}")
        
        # Test specific selectors
        print("\n🔍 Testing specific selectors:")
        
        selectors_to_test = [
            ("input[name='email']", "Email field by name"),
            ("input[type='email']", "Email field by type"),
            ("input[type='password']", "Password field by type"),
            ("input[name='password']", "Password field by name"),
            ("button[type='submit']", "Submit button by type"),
            ("input[type='submit']", "Submit input by type"),
            ("form", "Form element")
        ]
        
        for selector, description in selectors_to_test:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"✅ {description}: Found {len(elements)} element(s) with selector '{selector}'")
                    element = elements[0]
                    print(f"   → Text: '{element.text}', Value: '{element.get_attribute('value')}', Visible: {element.is_displayed()}")
                else:
                    print(f"❌ {description}: No elements found with selector '{selector}'")
            except Exception as e:
                print(f"❌ {description}: Error with selector '{selector}' - {e}")
        
        # Try to interact with the form
        print("\n🔍 Attempting to interact with form...")
        try:
            email_field = driver.find_element(By.CSS_SELECTOR, "input[name='email']")
            password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            
            print("✅ Found email and password fields")
            print(f"Email field visible: {email_field.is_displayed()}, enabled: {email_field.is_enabled()}")
            print(f"Password field visible: {password_field.is_displayed()}, enabled: {password_field.is_enabled()}")
            
            # Test filling the form
            email_field.clear()
            email_field.send_keys("test@example.com")
            print("✅ Successfully entered email")
            
            password_field.clear()
            password_field.send_keys("testpassword")
            print("✅ Successfully entered password")
            
            # Look for submit button
            submit_buttons = driver.find_elements(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
            if submit_buttons:
                print(f"✅ Found {len(submit_buttons)} submit button(s)")
                for i, btn in enumerate(submit_buttons):
                    print(f"   Submit button {i+1}: text='{btn.text}', visible={btn.is_displayed()}, enabled={btn.is_enabled()}")
            else:
                print("❌ No submit buttons found")
                
        except Exception as e:
            print(f"❌ Error interacting with form: {e}")
        
        print("\n🔍 Keeping browser open for 30 seconds for manual inspection...")
        time.sleep(30)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    detailed_form_debug()
