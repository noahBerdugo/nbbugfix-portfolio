# 🔷 CryptoIdleMiner Script
# =============================

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

EMAIL = "your_email@example.com"
PASSWORD = "your_password"
URL = "https://crypto-idle-miner.com/play"


def crypto_idle_miner():
    driver = webdriver.Chrome(service=Service())
    driver.get(URL)
    wait = WebDriverWait(driver, 20)

    # Login form
    wait.until(EC.element_to_be_clickable((By.NAME, "email"))).send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]").click()

    # Wait for dashboard
    wait.until(EC.presence_of_element_located((By.ID, "dashboard")))
    print("✅ Logged into CryptoIdleMiner")

    while True:
        try:
            # Check for any claim/collect buttons and click
            collect_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Collect')]" )
            for btn in collect_buttons:
                btn.click()
                print("Collected rewards")
        except:
            pass
        time.sleep(300)  # check every 5 minutes
