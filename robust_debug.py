from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

SPLINTERLANDS_URL = "https://splinterlands.com"

def robust_debug():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(SPLINTERLANDS_URL)
    wait = WebDriverWait(driver, 30)
    
    print("🔍 Starting robust debug...")
    
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
    
    # Print page info
    print(f"Page title: {driver.title}")
    print(f"Current URL: {driver.current_url}")
    
    # Look for ALL buttons again
    print("\n🔍 All buttons found:")
    buttons = driver.find_elements(By.TAG_NAME, "button")
    print(f"Total buttons found: {len(buttons)}")
    
    login_candidates = []
    
    for i, button in enumerate(buttons):
        try:
            text = button.text.strip()
            classes = button.get_attribute("class")
            id_attr = button.get_attribute("id")
            visible = button.is_displayed()
            enabled = button.is_enabled()
            
            print(f"Button {i+1}: text='{text}', classes='{classes}', id='{id_attr}', visible={visible}, enabled={enabled}")
            
            # Check if this might be a login button
            if text and any(word in text.upper() for word in ['LOG', 'LOGIN', 'SIGN']):
                login_candidates.append((i+1, button, text))
                print(f"  ⭐ POTENTIAL LOGIN BUTTON: {text}")
                
        except Exception as e:
            print(f"Button {i+1}: ERROR - {e}")
    
    print(f"\n🔍 Found {len(login_candidates)} potential login buttons")
    
    # Try each login candidate
    for candidate_num, button, text in login_candidates:
        print(f"\n🔍 Testing candidate {candidate_num}: '{text}'")
        
        try:
            # Scroll to button
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(1)
            
            # Highlight the button
            driver.execute_script("arguments[0].style.border='3px solid red';", button)
            time.sleep(1)
            
            # Try to click
            if button.is_displayed() and button.is_enabled():
                button.click()
                print(f"✅ Clicked button: {text}")
                time.sleep(3)
                
                # Check if modal appeared
                try:
                    modal = driver.find_element(By.CSS_SELECTOR, "div[class*='modal'], .modal, [role='dialog']")
                    print("✅ Modal appeared!")
                    
                    # Look for login form elements
                    try:
                        email_inputs = modal.find_elements(By.XPATH, ".//input[@type='email' or @type='text' or contains(@placeholder, 'email') or contains(@placeholder, 'Email')]")
                        password_inputs = modal.find_elements(By.XPATH, ".//input[@type='password']")
                        
                        print(f"Email inputs found: {len(email_inputs)}")
                        print(f"Password inputs found: {len(password_inputs)}")
                        
                        if email_inputs and password_inputs:
                            print("✅ This appears to be the login modal!")
                            
                            # Keep browser open for inspection
                            print("🔍 Keeping browser open for 30 seconds to inspect login form...")
                            time.sleep(30)
                            break
                    except:
                        print("❌ No login form found in modal")
                        
                except:
                    print("❌ No modal appeared")
                    
            else:
                print(f"❌ Button not clickable: visible={button.is_displayed()}, enabled={button.is_enabled()}")
                
        except Exception as e:
            print(f"❌ Error testing button {candidate_num}: {e}")
    
    # Also try using WebDriverWait for the login button
    print("\n🔍 Trying WebDriverWait approach...")
    try:
        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'LOG IN') or contains(text(), 'Login') or contains(text(), 'SIGN IN')]")))
        print("✅ Found login button with WebDriverWait")
        login_btn.click()
        print("✅ Clicked login button")
        
        # Wait for modal
        modal = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class*='modal'], .modal, [role='dialog']")))
        print("✅ Login modal appeared")
        
    except Exception as e:
        print(f"❌ WebDriverWait approach failed: {e}")
    
    print("\n🔍 Keeping browser open for final inspection...")
    time.sleep(30)
    
    driver.quit()

if __name__ == "__main__":
    robust_debug()
