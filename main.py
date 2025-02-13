import re
import random
import requests
import time
import pdfplumber
from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

app = FastAPI()

@app.get('/main')
async def main(inn: str):
    inn_firm = inn

    # 1 -------- файл качается в докер, надо шарить папку и раскоментить парс пдфа с сайта
    first_site_info = first_site(inn = inn)

      
    array_inn = [inn_firm]
    array_fio = []
    for info in first_site_info[1]:
        array_inn.append(info['inn'])
        array_fio.append(f'{info['surname']} {info['name']} {info['patronymic']}')

    
    # 2 -------- данные есть и скриншот (скриншот как на 7 сайте, надо спросить норм или нет)
    # second_site_info = []
    # for inn in array_inn:
    #     info_dict = {f'{inn}': second_site(inn)}
    #     second_site_info.append(info_dict)


    # 3 --------
    # third_site_info = third_site(inn_firm) <- Необходимо переписать на селениум

    
    # 4 -------- данные и скриншоты есть (по скриншотам надо вопрос задать, что там еще должно быть, может перейти во внутрь карточки)
    # fourth_site_info = []
    # for inn in array_inn:
    #     info_dict = {f'{inn}': fourth_site(inn)}
    #     fourth_site_info.append(info_dict)


    # 5 --------
    five_site_info = []
    for inn in array_inn:
        info_dict = {f'{inn}': five_site(inn)}
        five_site_info.append(info_dict)


    # 7 -------- данные и скриншот есть (скриншот надо спросить пойдет или нет)
    # seven_site_info = []
    # for inn in array_inn:
    #     info_dict = {f'{inn}': seven_site(inn)}
    #     seven_site_info.append(info_dict)


    # 9 -------- файл и данные есть (файл в докере)
    # nine_site_info = []
    # for inn in array_inn:
    #     info_dict = {f'{inn}': nine_site(inn)}
    #     nine_site_info.append(info_dict)
    

    # 10 -------- скрины и данные есть
    # ten_site_info = []
    # for fio in array_fio:
    #     info_dict = {f'{fio}': ten_site(fio=fio)}
    #     ten_site_info.append(info_dict)

    return five_site_info

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

download_dir = "." 

options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={random_user_agent}")
options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,  # Куда сохранять
    "download.prompt_for_download": False,  # Не показывать окно подтверждения
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

driver = webdriver.Remote(
    command_executor="http://localhost:4444/wd/hub",
    options=options  
)


def first_site(inn: str):
    try:
        driver = webdriver.Remote(
            command_executor="http://localhost:4444/wd/hub",
            options=options  
        )
        print('-----first_site start')
        # driver.get("https://egrul.nalog.ru/index.html")
        
        # input_inn = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.XPATH, "//input[@id='query']"))
        # )
        # print(input_inn.get_attribute('outerHTML'))
        
        # input_inn.click()
        # time.sleep(1)

        # input_inn.send_keys(inn)
        # input_inn.send_keys(Keys.RETURN)
        # time.sleep(15)
        # result_title = WebDriverWait(driver, 20).until(
        #     EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'res-caption')]"))
        # ) 
        # result_info = WebDriverWait(driver, 20).until(
        #     EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'res-text')]"))
        # )
        # button_for_download_pdf = WebDriverWait(driver, 20).until(
        #     EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'btn-with-icon btn-excerpt op-excerpt')]"))
        # )
        
        # button_for_download_pdf.click()
        # print(result_title.text)
        # print(result_info.text)
        # time.sleep(20)
        # print("Заголовок страницы:", driver.title)
        with pdfplumber.open("ul-1025002033110-20250212154136.pdf") as pdf:
            text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        
        firm_name_pattern = r"1 Полное наименование на русском языке(.*?)2"
        firm_name_match = re.search(firm_name_pattern, text, re.DOTALL)

        
        
        
        
        firm_name = firm_name_match.group(1).strip().replace("\n", " ").replace("\"", "'") if firm_name_match else "Не найдено"
        
        

        # Регулярное выражение для поиска информации о каждом участнике
        all_partition_pattern = r"\d+\s+Фамилия\s+([^\n]+)\s+Имя\s+([^\n]+)\s+Отчество\s+([^\n]+)\s+\d+\s+ИНН\s+(\d+)"

        # Поиск всех совпадений
        all_partition_matches = re.findall(all_partition_pattern, text)
        
        all_partition_result = []
        # Вывод результатов
        for match in all_partition_matches:
            surname, name, patronymic, inn = match
            result_dict = {
                'surname': surname,
                'name': name,
                'patronymic': patronymic,
                'inn': inn,
            }
            all_partition_result.append(result_dict)
            

        print('-----first_site end')
        return firm_name, all_partition_result
        
    finally:
        # driver.quit()
        pass


def second_site(inn: str):
    try:
        print('-----second_site start')
        print(inn)
        bad_inn = '723011055739'
        url = f"https://zakupki.gov.ru/epz/dishonestsupplier/search/results.html?searchString={inn}&morphology=on&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&fz94=on&fz223=on&ppRf615=on"
        
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "lxml")
        result_info = soup.find(class_='search-registry-entrys-block') # search-registry-entrys-block
        no_result_info = soup.find(class_='paginator-block')
        print(1, len(result_info.text))
        print(2, len(no_result_info.text))
        ##############################
        driver = webdriver.Remote(
            command_executor="http://localhost:4444/wd/hub",
            options=options
        )
        driver.get(f"https://zakupki.gov.ru/epz/dishonestsupplier/search/results.html?searchString={inn}&morphology=on&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&fz94=on&fz223=on&ppRf615=one")
        time.sleep(5)
        driver.save_screenshot(f'./screenshot/second_site/{inn}.png')
        #############################
        print('-----second_site end')
        if len(result_info.text) > 10:
            return 'yes'
        return 'no'
        
    finally:
        pass


def third_site(inn: str):
    try:
        print('-----third_site start')
        
        bad_inn = '723011055739'
        url = f"https://pb.nalog.ru/search.html#t=1739260392651&mode=search-all&queryAll={inn}&page=1&pageSize=10"
        # https://zakupki.gov.ru/epz/dishonestsupplier/search/results.html?searchString=723011055739&morphology=on&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&fz94=on&fz223=on&ppRf615=on
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "lxml")
        result_info = soup.find(class_='pnl-search-result') # search-registry-entrys-block
        print(result_info)
        
        print('-----third_site end')
        # return result_info

    finally:
        # driver.quit()
        pass


def fourth_site(inn: str):
    try:
        driver = webdriver.Remote(
            command_executor="http://localhost:4444/wd/hub",
            options=options  
        )

        print('-----fourth_site start')
        # inn = "5054004240"
        driver.get(f"https://fedresurs.ru/entities?searchString={inn}")
        time.sleep(5)
        result = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'container full-height')]"))
        )
        driver.save_screenshot(f'./screenshot/fourth_site/{inn}.png')
        # print(result.get_attribute('outerHTML'))
        print(len(result.get_attribute('outerHTML')))
        # no-result-msg-header
        print('-----fourth_site end')
        if len(result.get_attribute('outerHTML')) > 7000:
            return 'yes'
        return 'no'
    finally:
        driver.quit()


def five_site(inn: str):
    try:
        print('-----five_site start')
        # inn = "5054004240"
        driver = webdriver.Remote(
            command_executor="http://localhost:4444/wd/hub",
            options=options  
        )
        
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
        # result_info = WebDriverWait(driver, 10).until( # не получается увидеть таблицу с результатами очень сложный сайт (нужно подумать нужна ли эта переменная)
        #     # EC.element_to_be_clickable((By.XPATH, "//div[@id='table']"))
        #     EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'b-results')]"))
        # )
        driver.save_screenshot(f'./screenshot/five_site/{inn}.png')
        banckrot_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'bankruptcy')]"))
        )
        banckrot_button.click() # !почему то говори, что не кликабле, хотя по факту кликабле
        time.sleep(2)
        driver.save_screenshot(f'./screenshot/five_site/{inn}.png')
        # print(result_info.get_attribute('outerHTML'))
        

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


def seven_site(inn: str):
    try:
        print('-----seven_site start')

        # inn = "5054004240"
        url = f'https://zakupki.gov.ru/epz/main/public/document/search.html?searchString={inn}&sectionId=2369&strictEqual=false'

        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "lxml")
        result_info = soup.find_all('section')[0].find(class_='docs-list')
        
        print(len(result_info.text))
        ##############################
        driver = webdriver.Remote(
            command_executor="http://localhost:4444/wd/hub",
            options=options  
        )
        driver.get(f"https://zakupki.gov.ru/epz/main/public/document/search.html?searchString={inn}&sectionId=2369&strictEqual=false")
        time.sleep(5)
        driver.save_screenshot(f'./screenshot/seven_site/{inn}.png')
        #############################
        print('-----seven_site end')
        if len(result_info.text) > 100:
            return 'yes'
        return 'no'
    finally:
        driver.quit()


def eight_site(): # Надо спросить
    try:
        pass
    finally:
        pass


def nine_site(inn: str): # Впринципе готово (проблема по MIMA)
    ''''''
    try:
        # inn = "253607312162"
        url = 'https://minjust.gov.ru/ru/activity/directions/998/'
        response = requests.get(url, headers=headers, verify=False)

        soup = BeautifulSoup(response.text, 'lxml')
        pdf_src = soup.find(class_='page-block-text').find_all('a')[1]['href']
        pdf_url = 'https://minjust.gov.ru' + pdf_src
        
        with open(f'ckeck_pdf_url.txt', 'r') as file:
            last_pdf_url = file.readline()

        if last_pdf_url != pdf_url:
            print('качаем')
            # Пока не надо
            # pdf_file = requests.get(pdf_url, headers=headers, verify=False)
            # with open(f'reestr.pdf', 'wb') as file:
            #     file.write(pdf_file.content)

            # with open(f'ckeck_pdf_url.txt', 'w') as file:
            #     file.write(pdf_url)

        
        with pdfplumber.open('reestr.pdf') as pdf:
            for page in pdf.pages:
                if inn in page.extract_text():
                    return f'{inn} присутсвует в реестре на {page.page_number} странице'
            return 'no'
                
    finally:
        pass


def ten_site(fio: str): # Надо спросить
    try:
        # https://www.fedsfm.ru/documents/terr-list
        print('-----ten_site start')
        driver = webdriver.Remote(
            command_executor="http://localhost:4444/wd/hub",
            options=options  
        )

        
        # inn = "5054004240"
        driver.get(f"https://www.fedsfm.ru/documents/terr-list")
        time.sleep(5)
        form_for_fio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[contains(@class, 'form-control')]"))
        )
        
        form_for_fio.send_keys(fio)
        form_for_fio.send_keys(Keys.RETURN)

        result_info = WebDriverWait(driver, 10).until(
            # EC.element_to_be_clickable((By.XPATH, "//input[contains(@class, 'form-control')]"))
            EC.element_to_be_clickable((By.XPATH, "//tbody"))
        )
        driver.save_screenshot(f'./screenshot/ten_site/{fio}.png')
        print(form_for_fio.get_attribute('outerHTML'))
        print(len(result_info.get_attribute('outerHTML')))
        print('-----ten_site start')
        if len(result_info.get_attribute('outerHTML')) > 120:
            return 'yes'
        return 'no'
    
    finally:
        driver.quit()


