from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

SPLINTERLANDS_URL = "https://splinterlands.com"
EMAIL = "noahberdugo@gmail.com"
PASSWORD = "Cooper0809!!!"

def login_form_debug():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(SPLINTERLANDS_URL)
    wait = WebDriverWait(driver, 30)
    
    print("🔍 Starting login form debug...")
    
    # Wait for page to load completely
    print("⏳ Waiting for page to load...")
    time.sleep(10)
    
    # Accept cookies banner if present
    try:
        cookie_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept All')]")))
        cookie_btn.click()
        print("✅ Clicked cookie banner")
        time.sleep(2)
    except:
        print("ℹ️  No cookie banner found")
        pass
    
    # Wait for dynamic content to load
    print("⏳ Waiting for dynamic content to load...")
    time.sleep(5)
    
    # Find and click login button
    print("\n🔍 Looking for login button...")
    login_btn = None
    
    # Try different approaches to find the login button
    try:
        login_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'LOG IN')]")
        print("✅ Found LOG IN button")
    except:
        try:
            login_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
            print("✅ Found Login button")
        except:
            print("❌ Could not find login button")
            driver.quit()
            return
    
    if login_btn:
        # Scroll to button and highlight it
        driver.execute_script("arguments[0].scrollIntoView(true);", login_btn)
        driver.execute_script("arguments[0].style.border='3px solid red';", login_btn)
        time.sleep(1)
        
        # Click the login button
        print("🔍 Clicking login button...")
        login_btn.click()
        time.sleep(3)
        
        # Wait for login form to appear
        print("⏳ Waiting for login form to appear...")
        time.sleep(5)
        
        # Look for login form elements
        print("\n🔍 Analyzing login form structure...")
        
        # Check for modals
        modals = driver.find_elements(By.CSS_SELECTOR, "div[class*='modal'], .modal, [role='dialog'], [aria-modal='true']")
        print(f"Found {len(modals)} potential modal elements")
        
        # Check for any form elements
        forms = driver.find_elements(By.TAG_NAME, "form")
        print(f"Found {len(forms)} form elements")
        
        # Look for input fields
        all_inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"Found {len(all_inputs)} input elements")
        
        email_candidates = []
        password_candidates = []
        
        for i, input_elem in enumerate(all_inputs):
            try:
                input_type = input_elem.get_attribute("type")
                placeholder = input_elem.get_attribute("placeholder")
                name = input_elem.get_attribute("name")
                id_attr = input_elem.get_attribute("id")
                visible = input_elem.is_displayed()
                
                print(f"Input {i+1}: type='{input_type}', placeholder='{placeholder}', name='{name}', id='{id_attr}', visible={visible}")
                
                # Check if this might be an email field
                if visible and (input_type in ['email', 'text'] or 
                               (placeholder and any(word in placeholder.lower() for word in ['email', 'username', 'user'])) or
                               (name and any(word in name.lower() for word in ['email', 'username', 'user']))):
                    email_candidates.append((i+1, input_elem))
                    print(f"  ⭐ POTENTIAL EMAIL FIELD")
                
                # Check if this might be a password field
                if visible and input_type == 'password':
                    password_candidates.append((i+1, input_elem))
                    print(f"  ⭐ POTENTIAL PASSWORD FIELD")
                    
            except Exception as e:
                print(f"Input {i+1}: ERROR - {e}")
        
        print(f"\n🔍 Found {len(email_candidates)} email candidates and {len(password_candidates)} password candidates")
        
        # Try to fill the form
        if email_candidates and password_candidates:
            print("\n🔍 Attempting to fill login form...")
            
            try:
                # Fill email field
                email_field = email_candidates[0][1]
                email_field.clear()
                email_field.send_keys(EMAIL)
                print(f"✅ Filled email field with: {EMAIL}")
                
                # Fill password field
                password_field = password_candidates[0][1]
                password_field.clear()
                password_field.send_keys(PASSWORD)
                print("✅ Filled password field")
                
                # Look for submit button
                print("\n🔍 Looking for submit button...")
                submit_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Login') or contains(text(), 'LOG IN') or contains(text(), 'Sign in') or contains(text(), 'Submit')]")
                
                if not submit_buttons:
                    # Try to find button by type
                    submit_buttons = driver.find_elements(By.XPATH, "//button[@type='submit']")
                
                if not submit_buttons:
                    # Look for any button near the form
                    submit_buttons = driver.find_elements(By.TAG_NAME, "button")
                    # Filter for buttons that might be submit buttons
                    submit_buttons = [btn for btn in submit_buttons if btn.is_displayed() and btn.is_enabled()]
                
                print(f"Found {len(submit_buttons)} potential submit buttons")
                
                for i, btn in enumerate(submit_buttons):
                    try:
                        text = btn.text.strip()
                        btn_type = btn.get_attribute("type")
                        classes = btn.get_attribute("class")
                        print(f"Submit button {i+1}: text='{text}', type='{btn_type}', classes='{classes}'")
                        
                        # Try to identify the correct submit button
                        if text and any(word in text.upper() for word in ['LOGIN', 'SIGN IN', 'SUBMIT']):
                            print(f"  ⭐ POTENTIAL SUBMIT BUTTON: {text}")
                            
                            # Try clicking it
                            btn.click()
                            print(f"✅ Clicked submit button: {text}")
                            time.sleep(5)
                            
                            # Check if we're logged in
                            if "login" not in driver.current_url.lower():
                                print("✅ Login appears successful!")
                                break
                            else:
                                print("❌ Still on login page")
                                
                    except Exception as e:
                        print(f"Error with submit button {i+1}: {e}")
                
                # Wait and check final state
                print("\n🔍 Checking final login state...")
                time.sleep(5)
                print(f"Current URL: {driver.current_url}")
                print(f"Page title: {driver.title}")
                
                # Look for success indicators
                success_indicators = driver.find_elements(By.XPATH, "//*[contains(text(), 'Welcome') or contains(text(), 'Dashboard') or contains(text(), 'Profile')]")
                if success_indicators:
                    print("✅ Found success indicators - login likely successful!")
                else:
                    print("❌ No clear success indicators found")
                
            except Exception as e:
                print(f"❌ Error filling form: {e}")
        
        else:
            print("❌ Could not find both email and password fields")
    
    print("\n🔍 Keeping browser open for manual inspection...")
    time.sleep(30)
    
    driver.quit()

if __name__ == "__main__":
    login_form_debug()
