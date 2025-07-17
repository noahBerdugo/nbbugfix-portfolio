from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

SPLINTERLANDS_URL = "https://splinterlands.com"

def test_login_button():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    try:
        driver.get(SPLINTERLANDS_URL)
        wait = WebDriverWait(driver, 30)
        
        print("🔍 Testing login button click...")
        
        # Wait for page to load
        time.sleep(5)
        
        # Accept cookies banner if present
        try:
            cookie_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept All')]")))
            cookie_btn.click()
            print("✅ Clicked cookie banner")
            time.sleep(2)
        except:
            print("ℹ️  No cookie banner found")
            pass
        
        # Test different approaches to find and click the login button
        print("\n🔍 Testing different login button selectors...")
        
        # Test 1: Exact text match
        try:
            login_btn = driver.find_element(By.XPATH, "//button[text()='LOG IN']")
            if login_btn.is_displayed():
                print("✅ Found login button with exact text match")
                print(f"Button text: '{login_btn.text}'")
                print(f"Button classes: '{login_btn.get_attribute('class')}'")
                
                # Try clicking
                try:
                    login_btn.click()
                    print("✅ Successfully clicked login button")
                    time.sleep(3)
                    
                    # Check if modal appeared
                    try:
                        modal = driver.find_element(By.CSS_SELECTOR, "div[class*='modal']")
                        print("✅ Login modal appeared")
                        
                        # Keep browser open to see the modal
                        print("🔍 Keeping browser open for 30 seconds to inspect modal...")
                        time.sleep(30)
                        
                    except:
                        print("❌ No login modal found")
                        
                except Exception as e:
                    print(f"❌ Failed to click login button: {e}")
                    
            else:
                print("❌ Login button found but not visible")
                
        except Exception as e:
            print(f"❌ Could not find login button with exact text: {e}")
        
        # Test 2: Contains text match
        try:
            login_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'LOG IN')]")
            if login_btn.is_displayed():
                print("✅ Found login button with contains text match")
                print(f"Button text: '{login_btn.text}'")
                print(f"Button classes: '{login_btn.get_attribute('class')}'")
                
                # Try clicking with JavaScript
                try:
                    driver.execute_script("arguments[0].click();", login_btn)
                    print("✅ Successfully clicked login button with JavaScript")
                    time.sleep(3)
                    
                    # Check if modal appeared
                    try:
                        modal = driver.find_element(By.CSS_SELECTOR, "div[class*='modal']")
                        print("✅ Login modal appeared")
                    except:
                        print("❌ No login modal found")
                        
                except Exception as e:
                    print(f"❌ Failed to click login button with JavaScript: {e}")
                    
            else:
                print("❌ Login button found but not visible")
                
        except Exception as e:
            print(f"❌ Could not find login button with contains text: {e}")
        
        # Test 3: Try all buttons with "LOG IN" text
        try:
            login_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'LOG IN')]")
            print(f"Found {len(login_buttons)} buttons with 'LOG IN' text")
            
            for i, btn in enumerate(login_buttons):
                print(f"Button {i+1}: text='{btn.text}', visible={btn.is_displayed()}, enabled={btn.is_enabled()}")
                if btn.is_displayed() and btn.is_enabled():
                    try:
                        # Scroll to button
                        driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                        time.sleep(1)
                        
                        # Click with JavaScript
                        driver.execute_script("arguments[0].click();", btn)
                        print(f"✅ Clicked button {i+1} successfully")
                        time.sleep(3)
                        
                        # Check if modal appeared
                        try:
                            modal = driver.find_element(By.CSS_SELECTOR, "div[class*='modal']")
                            print("✅ Login modal appeared")
                            break
                        except:
                            print("❌ No login modal found after clicking")
                            
                    except Exception as e:
                        print(f"❌ Failed to click button {i+1}: {e}")
                        
        except Exception as e:
            print(f"❌ Error finding login buttons: {e}")
        
        print("\n🔍 Keeping browser open for manual inspection...")
        time.sleep(30)
        
    finally:
        driver.quit()
        print("🔍 Browser closed")

if __name__ == "__main__":
    test_login_button()
