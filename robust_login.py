from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys

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

SPLINTERLANDS_URL = "https://splinterlands.com"
EMAIL = "noahberdugo@gmail.com"
PASSWORD = "Cooper0809!!!"

def robust_login():
    # Initialize driver using get_driver function
    driver = None
    try:
        driver = get_driver(headless=False)
        wait = WebDriverWait(driver, 30)
        
        print("🔍 Starting robust login process...")
        
        # Navigate to site
        try:
            driver.get(SPLINTERLANDS_URL)
            print(f"✅ Navigated to {SPLINTERLANDS_URL}")
        except WebDriverException as e:
            print(f"❌ Failed to navigate to {SPLINTERLANDS_URL}: {e}")
            return
        
        # Wait for page to load completely
        try:
            print("⏳ Waiting for page to load completely...")
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(5)
        except TimeoutException:
            print("❌ Page failed to load completely")
            return
        
        # Accept cookies if present
        try:
            cookie_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept All') or contains(text(), 'Accept') or contains(text(), 'OK')]")))
            cookie_btn.click()
            print("✅ Accepted cookies")
            time.sleep(2)
        except TimeoutException:
            print("ℹ️  No cookie banner found")
        except Exception as e:
            print(f"❌ Error handling cookies: {e}")
        
        # Wait for dynamic content to load
        print("⏳ Waiting for dynamic content...")
        time.sleep(5)
        
        # Try multiple strategies to find the login button
        login_btn = None
        strategies = [
            ("LOG IN exact text", "//button[text()='LOG IN']"),
            ("LOG IN contains text", "//button[contains(text(), 'LOG IN')]"),
            ("Login contains text", "//button[contains(text(), 'Login')]"),
            ("Sign in contains text", "//button[contains(text(), 'Sign in')]"),
            ("Login CSS class", "button[class*='login']"),
            ("Login data attribute", "button[data-testid*='login']"),
        ]
        
        for strategy_name, selector in strategies:
            try:
                print(f"🔍 Trying strategy: {strategy_name}")
                if selector.startswith("//"):
                    login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                else:
                    login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                print(f"✅ Found login button using: {strategy_name}")
                break
            except TimeoutException:
                print(f"❌ Strategy failed: {strategy_name}")
                continue
            except Exception as e:
                print(f"❌ Error with strategy {strategy_name}: {e}")
                continue
        
        if not login_btn:
            print("❌ Login button not found on main page")
            # List all buttons for debugging
            print("🔍 Listing all buttons for debugging:")
            try:
                buttons = driver.find_elements(By.TAG_NAME, "button")
                for i, btn in enumerate(buttons):
                    try:
                        text = btn.text.strip()
                        if text:
                            print(f"  Button {i+1}: '{text}'")
                    except Exception:
                        pass
            except Exception as e:
                print(f"❌ Error listing buttons: {e}")
            return
        
        # Scroll to and highlight the login button
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", login_btn)
            driver.execute_script("arguments[0].style.border='3px solid red';", login_btn)
            time.sleep(1)
        except Exception as e:
            print(f"❌ Error highlighting login button: {e}")
        
        # Click the login button
        try:
            print("🔍 Clicking login button...")
            login_btn.click()
            time.sleep(3)
        except Exception as e:
            print(f"❌ Error clicking login button: {e}")
            return
        
        # Wait for login form to appear
        print("⏳ Waiting for login form to appear...")
        
        # Try different selectors for the login form/modal
        form_selectors = [
            "div[class*='modal']",
            ".modal",
            "[role='dialog']",
            "[aria-modal='true']",
            "form",
            "div[class*='login']",
            "div[class*='auth']"
        ]
        
        login_form = None
        for selector in form_selectors:
            try:
                login_form = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
                print(f"✅ Found login form using selector: {selector}")
                break
            except TimeoutException:
                continue
            except Exception as e:
                print(f"❌ Error with form selector {selector}: {e}")
                continue
        
        if not login_form:
            print("❌ Login form not found on page")
            print("🔍 Checking current page state...")
            print(f"Current URL: {driver.current_url}")
            print(f"Page title: {driver.title}")
            return
        
        # Look for input fields within the form
        print("🔍 Looking for input fields...")
        
        # Try to find email field
        email_field = None
        email_selectors = [
            "input[type='email']",
            "input[type='text']",
            "input[placeholder*='email' i]",
            "input[placeholder*='username' i]",
            "input[name*='email' i]",
            "input[name*='username' i]",
            "input[name*='user' i]"
        ]
        
        for selector in email_selectors:
            try:
                email_field = login_form.find_element(By.CSS_SELECTOR, selector)
                if email_field.is_displayed():
                    print(f"✅ Found email field using: {selector}")
                    break
            except NoSuchElementException:
                continue
            except Exception as e:
                print(f"❌ Error with email selector {selector}: {e}")
                continue
        
        # Try to find password field
        password_field = None
        try:
            password_field = login_form.find_element(By.CSS_SELECTOR, "input[type='password']")
            if password_field.is_displayed():
                print("✅ Found password field")
        except NoSuchElementException:
            print("❌ Password field not found in login form")
        except Exception as e:
            print(f"❌ Error finding password field: {e}")
        
        # Fill the form if we found both fields
        if email_field and password_field:
            print("🔍 Filling login form...")
            
            try:
                # Clear and fill email field
                email_field.clear()
                email_field.send_keys(EMAIL)
                print(f"✅ Filled email field with: {EMAIL}")
            except Exception as e:
                print(f"❌ Error filling email field: {e}")
                return
            
            try:
                # Clear and fill password field
                password_field.clear()
                password_field.send_keys(PASSWORD)
                print("✅ Filled password field")
            except Exception as e:
                print(f"❌ Error filling password field: {e}")
                return
            
            # Look for submit button
            print("🔍 Looking for submit button...")
            submit_btn = None
            
            # Try XPath selectors for submit button
            xpath_selectors = [
                ".//button[contains(text(), 'Login')]",
                ".//button[contains(text(), 'LOG IN')]",
                ".//button[contains(text(), 'Sign in')]",
                ".//button[@type='submit']",
                ".//input[@type='submit']"
            ]
            
            for selector in xpath_selectors:
                try:
                    submit_btn = login_form.find_element(By.XPATH, selector)
                    if submit_btn.is_displayed() and submit_btn.is_enabled():
                        print(f"✅ Found submit button using: {selector}")
                        break
                except NoSuchElementException:
                    continue
                except Exception as e:
                    print(f"❌ Error with submit selector {selector}: {e}")
                    continue
            
            if submit_btn:
                try:
                    # Click submit button
                    print("🔍 Clicking submit button...")
                    submit_btn.click()
                    time.sleep(5)
                except Exception as e:
                    print(f"❌ Error clicking submit button: {e}")
                    return
                
                # Check if login was successful
                print("🔍 Checking login result...")
                print(f"Current URL: {driver.current_url}")
                print(f"Page title: {driver.title}")
                
                # Look for success indicators
                success_indicators = [
                    "Welcome",
                    "Dashboard",
                    "Profile",
                    "Logout",
                    "My Account"
                ]
                
                found_success = False
                for indicator in success_indicators:
                    try:
                        element = driver.find_element(By.XPATH, f"//*[contains(text(), '{indicator}')]")
                        if element.is_displayed():
                            print(f"✅ Found success indicator: {indicator}")
                            found_success = True
                            break
                    except NoSuchElementException:
                        continue
                    except Exception as e:
                        print(f"❌ Error checking success indicator {indicator}: {e}")
                        continue
                
                if found_success:
                    print("✅ Login appears successful!")
                else:
                    print("❌ Login may have failed - no success indicators found")
                
            else:
                print("❌ Submit button not found in login form")
        else:
            print("❌ Could not find both email and password fields")
            if not email_field:
                print("  - Email field not found")
            if not password_field:
                print("  - Password field not found")
        
        # Keep browser open for inspection
        print("\n🔍 Keeping browser open for 30 seconds for inspection...")
        time.sleep(30)
        
    except (TimeoutException, NoSuchElementException) as e:
        print(f"❌ Selenium error during login process: {e}")
        import traceback
        traceback.print_exc()
    except WebDriverException as e:
        print(f"❌ WebDriver error during login process: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"❌ Unexpected error during login process: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if driver:
            driver.quit()
            print("🔍 Browser closed")

if __name__ == "__main__":
    robust_login()
