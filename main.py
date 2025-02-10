import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
]

random_user_agent = random.choice(USER_AGENTS)

options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={random_user_agent}")

driver = webdriver.Remote(
    command_executor="http://localhost:4444/wd/hub",
    options=options  
)

try:
    driver.get("https://egrul.nalog.ru/index.html")
    
    input_inn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='query']"))
    )
    print(input_inn.get_attribute('outerHTML'))
    
    input_inn.click()
    time.sleep(1)

    input_inn.send_keys("5054004240")
    input_inn.send_keys(Keys.RETURN)
    
    result_title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'res-caption')]"))
    )
    # result = driver.find_element(By.XPATH, "//div[contains(@class, 'res-caption')]")   
    result_info = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'res-text')]"))
    )
    print(result_title.text)
    print(result_info.text)
    time.sleep(3)

    print("Заголовок страницы:", driver.title)
finally:
    driver.quit()
