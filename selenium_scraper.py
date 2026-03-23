from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver

def scrape_enbd_faq(driver):
    print("Opening Emirates NBD FAQ page...")
    driver.get("https://www.emiratesnbd.com/en/help-and-support")
    time.sleep(5)
    print("Page loaded. Looking for FAQ sections...")
    collected = []
    try:
        wait = WebDriverWait(driver, 10)
        expandables = driver.find_elements(By.CSS_SELECTOR, 
            "button, .accordion, .faq-item, [class*='accordion'], [class*='faq'], [class*='expand'], [class*='collapse']")
        print(f"Found {len(expandables)} clickable elements")
        clicked = 0
        for element in expandables:
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.3)
                driver.execute_script("arguments[0].click();", element)
                time.sleep(0.8)
                clicked += 1
            except:
                pass
        print(f"Clicked {clicked} elements")
        time.sleep(2)
        page_text = driver.find_element(By.TAG_NAME, "body").text
        lines = [l.strip() for l in page_text.split("\n") if l.strip()]
        clean_text = "\n".join(lines)
        collected.append(clean_text)
        print(f"Collected {len(clean_text)} characters from Emirates NBD")
    except Exception as e:
        print(f"Error: {e}")
    return "\n\n".join(collected)

def scrape_fab_faq(driver):
    print("Opening FAB FAQ page...")
    driver.get("https://www.bankfab.com/en-ae/personal/help-and-support/faqs")
    time.sleep(5)
    print("Page loaded. Expanding FAB dropdowns...")
    try:
        expandables = driver.find_elements(By.CSS_SELECTOR,
            "button, .accordion, [class*='accordion'], [class*='faq'], [class*='expand'], [class*='plus'], [class*='arrow']")
        print(f"Found {len(expandables)} clickable elements")
        clicked = 0
        for element in expandables:
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.3)
                driver.execute_script("arguments[0].click();", element)
                time.sleep(0.8)
                clicked += 1
            except:
                pass
        print(f"Clicked {clicked} elements")
        time.sleep(2)
        page_text = driver.find_element(By.TAG_NAME, "body").text
        lines = [l.strip() for l in page_text.split("\n") if l.strip()]
        clean_text = "\n".join(lines)
        print(f"Collected {len(clean_text)} characters from FAB")
        return clean_text
    except Exception as e:
        print(f"Error: {e}")
        return ""

print("Starting Selenium scraper...")
print("A Chrome browser window will open automatically - do not close it")
print("")

driver = setup_driver()

try:
    enbd_text = scrape_enbd_faq(driver)
    fab_text = scrape_fab_faq(driver)
    
    combined = "=== Emirates NBD FAQ - Selenium ===\n\n" + enbd_text
    combined += "\n\n=== FAB FAQ - Selenium ===\n\n" + fab_text
    
    with open("selenium_faq.txt", "w", encoding="utf-8") as f:
        f.write(combined)
    
    print("")
    print(f"Total characters collected: {len(combined)}")
    print("Saved to selenium_faq.txt")

finally:
    driver.quit()
    print("Browser closed")