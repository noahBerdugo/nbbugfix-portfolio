from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Reusable helper for WebDriverWait
wait = WebDriverWait(driver, 15)

def click_when_clickable(locator):
    """
    Waits for an element to be clickable and then clicks it.

    :param locator: Locator of the element to be clicked.
    :return: The WebElement after it has been clicked.
    """
    el = wait.until(EC.element_to_be_clickable(locator))
    el.click()
    return el


def send_keys_when_visible(locator, keys):
    """
    Waits for an element to be visible, clears it, and then sends keys to it.

    :param locator: Locator of the element for sending keys.
    :param keys: The keys to send to the element.
    :return: The WebElement after keys have been sent.
    """
    el = wait.until(EC.visibility_of_element_located(locator))
    el.clear()
    el.send_keys(keys)
    return el

