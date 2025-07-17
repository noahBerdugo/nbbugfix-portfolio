from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

EMAIL = "noahberdugo@gmail.com"
PASSWORD = "Cooper0809!!!"
PORTFOLIO_URL = ""
BTC_ADDRESS = "3BVjgb527A5m5kPUGE5NfQemJ2KuHhtnDf"

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

def login():
    driver.get("https://laborx.com")
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log in"))).click()
    wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys(EMAIL)
    wait.until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys(PASSWORD + Keys.RETURN)
    print("[+] Logged in")
    time.sleep(5)

def find_and_apply():
    driver.get("https://laborx.com/jobs?skills=remote")
    jobs = driver.find_elements(By.CSS_SELECTOR, "a.job-item__title")
    for job in jobs:
        href = job.get_attribute("href")
        driver.get(href)
        try:
            apply_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Apply')]")))
            apply_btn.click()
            textarea = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "textarea")))
            proposal = f"""Hi, I specialize in writing & can deliver high-quality work quickly.
Portfolio: {PORTFOLIO_URL}
Payment BTC: {BTC_ADDRESS}
Looking forward to working with you!"""
            textarea.send_keys(proposal)
            submit = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Send proposal')]")))
            submit.click()
            print(f"[+] Applied to: {href}")
            time.sleep(2)
        except Exception as e:
            print(f"[!] Failed on {href}: {e}")
            continue

if __name__ == "__main__":
    login()
    find_and_apply()
    driver.quit()
