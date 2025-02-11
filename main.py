import random
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
    'Mozilla/5.0 (compatible; ABrowse 0.4; Syllable)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)',
    'Mozilla/5.0 (X11; Linux i686; rv:7.0a1) Gecko/20110603 SeaMonkey/2.2a1pre',
]

random_user_agent = random.choice(USER_AGENTS)

headers = {
    'User-Agent': random.choice(USER_AGENTS)
}

options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={random_user_agent}")

driver = webdriver.Remote(
    command_executor="http://localhost:4444/wd/hub",
    options=options  
)


def first_site():
    try:
        print('-----first_site start')
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
        print('-----first_site end')
    finally:
        driver.quit()


def second_site():
    try:
        print('-----second_site start')
        inn = "5054004240"
        bad_inn = '723011055739'
        url = f"https://zakupki.gov.ru/epz/dishonestsupplier/search/results.html?searchString={inn}&morphology=on&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&fz94=on&fz223=on&ppRf615=on"
        # https://zakupki.gov.ru/epz/dishonestsupplier/search/results.html?searchString=723011055739&morphology=on&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&fz94=on&fz223=on&ppRf615=on
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "lxml")
        result_info = soup.find(class_='search-registry-entrys-block') # search-registry-entrys-block
        no_result_info = soup.find(class_='paginator-block')
        print(result_info)
        print(no_result_info)
        
        print('-----second_site end')

    finally:
        # driver.quit()
        pass


def third_site():
    try:
        print('-----third_site start')
        inn = "5054004240"
        bad_inn = '723011055739'
        url = f"https://pb.nalog.ru/search.html#t=1739260392651&mode=search-all&queryAll={inn}&page=1&pageSize=10"
        # https://zakupki.gov.ru/epz/dishonestsupplier/search/results.html?searchString=723011055739&morphology=on&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&fz94=on&fz223=on&ppRf615=on
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "lxml")
        result_info = soup.find(class_='pnl-search-result') # search-registry-entrys-block
        print(result_info)
        
        print('-----third_site end')

    finally:
        # driver.quit()
        pass


def fourth_site():
    try:
        print('-----fourth_site start')
        inn = "5054004240"
        driver.get(f"https://fedresurs.ru/entities?searchString={inn}")
        result = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'container full-height')]"))
        )
        print(result.get_attribute('outerHTML'))
        

        print('-----fourth_site end')
    finally:
        driver.quit()


def five_site():
    try:
        print('-----five_site start')
        inn = "5054004240"
        
        driver.get(f"https://kad.arbitr.ru/")
        time.sleep(5)
        input_inn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//textarea[contains(@class, 'g-ph')]"))
        )
        print(input_inn.get_attribute('outerHTML'))

        # input_inn.click()
        time.sleep(1)

        input_inn.send_keys(inn)
        input_inn.send_keys(Keys.RETURN)
        time.sleep(15)
        result_info = WebDriverWait(driver, 10).until( # не получается увидеть таблицу с результатами очень сложный сайт
            # EC.element_to_be_clickable((By.XPATH, "//div[@id='table']"))
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'b-results')]"))
        )
        print(result_info.get_attribute('outerHTML'))
        

        print('-----five_site end')
    finally:
        driver.quit()


def six_site():
    try:
        print('-----six_site start')
        
        inn = "5054004240"
        url = f'https://service.nalog.ru/disqualified.html#t=1739263708368&query={inn}'

        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "lxml")
        result_info = soup.find_all(class_='nu-section__content')[1].find_all(class_='hidden')[1]
        
        print(result_info)
        
        print('-----six_site end')
    finally:
        pass


def seven_site():
    try:
        print('-----seven_site start')

        inn = "5054004240"
        url = f'https://zakupki.gov.ru/epz/main/public/document/search.html?searchString={inn}&sectionId=2369&strictEqual=false'

        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "lxml")
        result_info = soup.find_all('section')[0].find(class_='docs-list')
        
        print(result_info)

        print('-----seven_site end')
    finally:
        pass


def eight_site():
    try:
        pass
    finally:
        pass


def nine_site():
    try:
        url = 'https://minjust.gov.ru/ru/activity/directions/998/'
        response = requests.get(url, headers=headers, verify=False)

        soup = BeautifulSoup(response.text, 'lxml')
        pdf_src = soup.find(class_='page-block-text').find_all('a')[1]['href']
        pdf_url = 'https://minjust.gov.ru' + pdf_src
        print(pdf_url)

        pdf_file = requests.get(pdf_url, headers=headers, verify=False)
        with open(f'1.pdf', 'wb') as file:
            file.write(pdf_file.content)
    finally:
        pass


def ten_site():
    try:
        pass
    finally:
        pass


def main():
    # first_site()
    # second_site()
    # third_site()
    # fourth_site()
    # five_site()
    # six_site()
    # seven_site()
    # eight_site()
    nine_site()
    # ten_site()

if __name__ == '__main__':
    main()