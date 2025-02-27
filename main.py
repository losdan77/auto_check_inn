import glob
import re
import random
import requests
import time
import datetime
import pdfplumber
import shutil
import asyncio
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from docx import Document

from utils import USER_AGENTS, clear_result_folder, SELENIUM_HOST, SELENIUM_PORT


app = FastAPI()


@app.get('/main')
async def main(inn: str):
    inn_firm = inn
    
    # 1 -------- файл качается в докер, надо шарить папку и раскоментить парс пдфа с сайта
    try:
        first_site_info = first_site(inn = inn)
        print(first_site_info)
        
        array_inn = [inn_firm]
        array_fio = []
        for info in first_site_info[1]:
            array_inn.append(info['inn'])
            array_fio.append(f'{info['surname']} {info['name']} {info['patronymic']}')

        
        second_site_tasks = [asyncio.to_thread(second_site, inn) for inn in array_inn]
        fourth_site_tasks = [asyncio.to_thread(fourth_site, inn) for inn in array_inn]
        seven_site_tasks = [asyncio.to_thread(seven_site, inn) for inn in array_inn]
        nine_site_tasks = [asyncio.to_thread(nine_site, inn) for inn in array_inn]
        ten_site_tasks = [asyncio.to_thread(ten_site, fio) for fio in array_fio]

        (
            second_site_info,
            fourth_site_info,
            seven_site_info,
            nine_site_info,
            ten_site_info,
        ) = await asyncio.gather(
            asyncio.gather(*second_site_tasks),
            asyncio.gather(*fourth_site_tasks),
            asyncio.gather(*seven_site_tasks),
            asyncio.gather(*nine_site_tasks),
            asyncio.gather(*ten_site_tasks),
        )
        # 2 -------- данные есть и скриншот (скриншот как на 7 сайте, надо спросить норм или нет)

        # second_site_info = []
        # for inn in array_inn:
        #     info_dict = second_site(inn)
        #     second_site_info.append(info_dict)


        # 3 -------- скриншот есть (единственное спросить хватит только инн фирмы и нужны ли данные в отчет)
        third_site_info = third_site(inn_firm) 

        
        # 4 -------- данные и скриншоты есть (по скриншотам надо вопрос задать, что там еще должно быть, может перейти во внутрь карточки)
        # fourth_site_info = []
        # for inn in array_inn:
        #     info_dict = fourth_site(inn)
        #     fourth_site_info.append(info_dict)


        # 5 --------
        # five_site_info = []
        # for inn in array_inn:
        #     info_dict = {f'{inn}': five_site(inn)}
        #     five_site_info.append(info_dict)
        five_site_info = five_site(inn)


        # 7 -------- данные и скриншот есть (скриншот надо спросить пойдет или нет)
        # seven_site_info = []
        # for inn in array_inn:
        #     info_dict = seven_site(inn)
        #     seven_site_info.append(info_dict)


        # 9 -------- файл и данные есть (файл в докере)
        # nine_site_info = []
        # for inn in array_inn:
        #     info_dict = nine_site(inn)
        #     nine_site_info.append(info_dict)
        

        # 10 -------- скрины и данные есть
        # ten_site_info = []
        # for fio in array_fio:
        #     info_dict = ten_site(fio=fio)
        #     ten_site_info.append(info_dict)

    except Exception as e:
        clear_result_folder()
        return 'Запустите еще раз', e

    document = Document()
    document.add_heading(f'ИНН проверяемой фирмы: {inn_firm} - {first_site_info[0]}')
    
    document.add_paragraph('1) Обращение в ЕГРЮЛ:')
    for i in range(len(array_fio)):
        if i == 0:
            document.add_paragraph(f'{array_fio[i]} - {array_inn[i]} - директор')
        else:
            document.add_paragraph(f'{array_fio[i]} - {array_inn[i]} - учредители')
    
    document.add_paragraph('2) Обращение в РНП:')
    for info in second_site_info:
        document.add_paragraph(f'{info}')

    document.add_paragraph('4) Обращение в Федресурс:')
    for info in fourth_site_info:
        document.add_paragraph(f'{info}')

    document.add_paragraph('7) Обращение по КОАП:')
    for info in seven_site_info:
        document.add_paragraph(f'{info}')

    document.add_paragraph('9) Обращение в РИА:')
    for info in nine_site_info:
        document.add_paragraph(f'{info}')

    document.add_paragraph('10) Обращение в РЭТ:')
    for info in ten_site_info:
        document.add_paragraph(f'{info}')

    document.save(f'./result/{inn_firm}.docx')

    try:
        now_time = str(datetime.datetime.now().strftime("%Y%m%d%H%M"))
        shutil.make_archive(f'{now_time}', 'zip', './result')
        return FileResponse(path=f'{now_time}.zip', filename=f'{now_time}.zip') # подумать как удалять его
    except:
        # clear_result_folder()
        return 'Запустите еще раз'
    finally:
        # os.remove(f'{now_time}.zip')
        clear_result_folder()
        pass


random_user_agent = random.choice(USER_AGENTS)

headers = {
    'User-Agent': random.choice(USER_AGENTS)
}

download_dir = "./result" 

options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={random_user_agent}")
options.add_argument("--disable-notifications")  # Отключить уведомления
options.add_argument("--disable-popup-blocking")  # Отключить блокировку всплывающих окон

options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,  # Куда сохранять
    "download.prompt_for_download": False,  # Не показывать окно подтверждения
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})


def first_site(inn: str):
    try:
        print('-----first_site start')

        driver = webdriver.Remote(
            command_executor=f"http://{SELENIUM_HOST}:{SELENIUM_PORT}/wd/hub",
            options=options  
        )
        driver.get("https://egrul.nalog.ru/index.html")
        
        input_inn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='query']"))
        )
        print(input_inn.get_attribute('outerHTML'))
        
        input_inn.click()
        time.sleep(1)

        input_inn.send_keys(inn)
        input_inn.send_keys(Keys.RETURN)
        time.sleep(15)
        # result_title = WebDriverWait(driver, 20).until(
        #     EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'res-caption')]"))
        # ) 
        # result_info = WebDriverWait(driver, 20).until(
        #     EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'res-text')]"))
        # )
        button_for_download_pdf = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'btn-with-icon btn-excerpt op-excerpt')]"))
        )
        
        button_for_download_pdf.click()
        time.sleep(20)
        pdf_file = glob.glob("./result/ul-*.pdf")
        
        with pdfplumber.open(f'{pdf_file[0]}') as pdf:
            text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        
        firm_name_pattern = r"1 Полное наименование на русском языке(.*?)2"
        firm_name_match = re.search(firm_name_pattern, text, re.DOTALL)

        firm_name = firm_name_match.group(1).strip().replace("\n", " ").replace("\"", "'") if firm_name_match else "Не найдено"
        
    
        all_partition_pattern = r"\d+\s+Фамилия\s+([^\n]+)\s+Имя\s+([^\n]+)\s+Отчество\s+([^\n]+)\s+\d+\s+ИНН\s+(\d+)"
        all_partition_matches = re.findall(all_partition_pattern, text)
        all_partition_result = []
        
        for match in all_partition_matches:
            surname, name, patronymic, inn = match
            result_dict = {
                'surname': surname,
                'name': name,
                'patronymic': patronymic,
                'inn': inn,
            }
            all_partition_result.append(result_dict)
            
        return firm_name, all_partition_result
        
    finally:
        driver.quit()
        print('-----first_site end')


def second_site(inn: str):
    try:
        print('-----second_site start')
    
        url = f"https://zakupki.gov.ru/epz/dishonestsupplier/search/results.html?searchString={inn}&morphology=on&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&fz94=on&fz223=on&ppRf615=on"
        
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "lxml")
        result_info = soup.find(class_='search-registry-entrys-block')

        ##############################
        driver = webdriver.Remote(
            command_executor=f"http://{SELENIUM_HOST}:{SELENIUM_PORT}/wd/hub",
            options=options
        )
        driver.get(f"https://zakupki.gov.ru/epz/dishonestsupplier/search/results.html?searchString={inn}&morphology=on&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&fz94=on&fz223=on&ppRf615=one")
        
        time.sleep(5)
        driver.save_screenshot(f'./result/screenshot/second_site/{inn}.png')
        #############################
        
        if len(result_info.text) > 10:
            return {f'{inn}': 'да'}
        return {f'{inn}': 'нет'}
        
    finally:
        print('-----second_site end')


def third_site(inn: str):
    try:
        print('-----third_site start')

        driver = webdriver.Remote(
            command_executor=f"http://{SELENIUM_HOST}:{SELENIUM_PORT}/wd/hub",
            options=options  
        )
        driver.get(f"https://pb.nalog.ru/index.html")

        input_inn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[contains(@class, 'u3-editor')]"))
        )
       
        input_inn.send_keys(inn)
        input_inn.send_keys(Keys.RETURN)
        
        time.sleep(5)
        driver.save_screenshot(f'./result/screenshot/third_site/1_{inn}.png')

        name_organization = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'pb-card__title')]"))
        )
        name_organization.click()

        time.sleep(5)
        result_info = driver.find_element(By.XPATH, "//span[contains(text(), 'Сведения о лице, имеющем право без доверенности действовать от имени юридического лица')]")
        ActionChains(driver).scroll_to_element(result_info).perform()
        driver.save_screenshot(f'./result/screenshot/third_site/2_{inn}.png')
        
        time.sleep(2)
        result_info = driver.find_element(By.XPATH, "//span[contains(text(), 'Сведения о непредставлении налоговой отчетности более года')]")
        ActionChains(driver).scroll_to_element(result_info).perform()
        driver.save_screenshot(f'./result/screenshot/third_site/3_{inn}.png')

    finally:
        driver.quit()
        print('-----third_site end')


def fourth_site(inn: str):
    try:
        print('-----fourth_site start')

        driver = webdriver.Remote(
            command_executor=f"http://{SELENIUM_HOST}:{SELENIUM_PORT}/wd/hub",
            options=options  
        )
        driver.get(f"https://fedresurs.ru/entities?searchString={inn}")
        
        time.sleep(5)
        
        result = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'container full-height')]"))
        )

        driver.save_screenshot(f'./result/screenshot/fourth_site/{inn}.png')
        
        if len(result.get_attribute('outerHTML')) > 7000:
            return {f'{inn}': 'да'}
        return {f'{inn}': 'нет'}
    finally:
        driver.quit()
        print('-----fourth_site end')


def five_site(inn: str):
    try:
        print('-----five_site start')
        # inn = "5054004240"
        # proxy = "http://V84kEe:XhAdiJu5Ej@45.15.72.224:5500"
        # options.add_argument(f"--proxy-server={proxy}")
        driver = webdriver.Remote(
            command_executor=f"http://{SELENIUM_HOST}:{SELENIUM_PORT}/wd/hub",
            options=options  
        )
        
        driver.get(f"https://kad.arbitr.ru/")

        time.sleep(5)
        driver.execute_script("""
            var modal = document.querySelector('.b-browsers.js-browsers');
            if (modal) {
                modal.style.display = 'none';
            }
        """)
        
        # Попробовать закрыть всплывающее окно
        try:
            # close_button = driver.find_element(By.XPATH, "//div[contains(@class='b-promo_notification-popup_wrapper')]//a[contains(@class='b-promo_notification-popup-close js-promo_notification-popup-close')]")
            close_button = driver.find_element(By.XPATH, "//a[contains(@class,'b-promo_notification-popup-close js-promo_notification-popup-close')]")
            close_button.click()
        except Exception as e:
            print("Не удалось закрыть всплывающее окно:", e)
        driver.save_screenshot(f'./result/screenshot/five_site/01_{inn}.png')
        time.sleep(2)

        input_inn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//textarea[contains(@class, 'g-ph')]"))
        )
        print(input_inn.get_attribute('outerHTML'))

        # input_inn.click()
        time.sleep(1)

        input_inn.send_keys(inn)
        driver.save_screenshot(f'./result/screenshot/five_site/02_{inn}.png')
        input_inn.send_keys(Keys.RETURN)
        driver.save_screenshot(f'./result/screenshot/five_site/1_{inn}.png')
        
        
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Найти')]"))
        )
        print(button.get_attribute('outerHTML'))
        button.click()
        driver.save_screenshot(f'./result/screenshot/five_site/03_{inn}.png')
        time.sleep(10)
        # result_info = WebDriverWait(driver, 10).until( # не получается увидеть таблицу с результатами очень сложный сайт (нужно подумать нужна ли эта переменная)
        #     # EC.element_to_be_clickable((By.XPATH, "//div[@id='table']"))
        #     EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'b-results')]"))
        # )
        driver.save_screenshot(f'./result/screenshot/five_site/2_{inn}.png')
        # banckrot_button = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'bankruptcy')]"))
        # )
        # banckrot_button.click() # !почему то говори, что не кликабле, хотя по факту кликабле
        time.sleep(2)
        # driver.save_screenshot(f'./result/screenshot/five_site/{inn}.png')
        # print(result_info.get_attribute('outerHTML'))
        

        print('-----five_site end')
    except:
        pass
    finally:
        driver.quit()


def seven_site(inn: str):
    try:
        print('-----seven_site start')

        url = f'https://zakupki.gov.ru/epz/main/public/document/search.html?searchString={inn}&sectionId=2369&strictEqual=false'

        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "lxml")
        result_info = soup.find_all('section')[0].find(class_='docs-list')
        
        print(len(result_info.text))
        ##############################
        driver = webdriver.Remote(
            command_executor=f"http://{SELENIUM_HOST}:{SELENIUM_PORT}/wd/hub",
            options=options  
        )
        driver.get(f"https://zakupki.gov.ru/epz/main/public/document/search.html?searchString={inn}&sectionId=2369&strictEqual=false")
        time.sleep(5)
        driver.save_screenshot(f'./result/screenshot/seven_site/{inn}.png')
        #############################
        
        if len(result_info.text) > 100:
            return {f'{inn}': 'да'}
        return {f'{inn}': 'нет'}
    
    finally:
        driver.quit()
        print('-----seven_site end')


def nine_site(inn: str): # Впринципе готово (проблема по MIMA)
    try:
        print('-----nine_site start')
        # url = 'https://minjust.gov.ru/ru/activity/directions/998/'
        # response = requests.get(url, headers=headers, verify=False)

        # soup = BeautifulSoup(response.text, 'lxml')
        # pdf_src = soup.find(class_='page-block-text').find_all('a')[1]['href']
        # pdf_url = 'https://minjust.gov.ru' + pdf_src
        
        # with open(f'ckeck_pdf_url.txt', 'r') as file:
        #     last_pdf_url = file.readline()

        # if last_pdf_url != pdf_url:
        #     print('качаем')
            
        #     pdf_file = requests.get(pdf_url, headers=headers, verify=False)
        #     with open(f'reestr.pdf', 'wb') as file:
        #         file.write(pdf_file.content)

        #     with open(f'ckeck_pdf_url.txt', 'w') as file:
        #         file.write(pdf_url)

        # time.sleep(5)
        # with pdfplumber.open('reestr.pdf') as pdf:
        #     for page in pdf.pages:
        #         if inn in page.extract_text():
        #             return f'{inn} присутсвует в реестре на {page.page_number} странице'
        #     return 'нет'

        excel_file = glob.glob("./result/export.xlsx")
        if not excel_file:
            url = 'https://minjust.gov.ru/ru/pages/reestr-inostryannykh-agentov/'
            driver = webdriver.Remote(
                command_executor=f"http://{SELENIUM_HOST}:{SELENIUM_PORT}/wd/hub",
                options=options  
            )
            driver.get(url)
            button_for_download_excel = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Загрузить реестр')]"))
            )
            
            button_for_download_excel.click()
            time.sleep(20)
            driver.quit()

        excel_path = "./result/export.xlsx"
        target_inn = inn

        try:
            # Читаем Excel-файл
            df = pd.read_excel(excel_path, engine='openpyxl')
            
            # Проверяем, достаточно ли столбцов в файле
            if df.shape[1] < 9:
                print("Файл содержит меньше 9 столбцов, столбец 'I' отсутствует.")
                exit()
            
            # Получаем данные из столбца 'I' (девятый столбец, индекс 8)
            column_i = df.iloc[:, 8].astype(str)
            
            # Проверяем наличие ИНН в столбце 'I'
            if target_inn in column_i.values:
                return {f'{inn}': 'присутствует в реестре'}
            else:
                return {f'{inn}': 'нет'}

        except FileNotFoundError:
            print(f"Файл {excel_path} не найден.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
    finally:
        
        print('-----nine_site end')


def ten_site(fio: str):
    try:
        print('-----ten_site start')
        driver = webdriver.Remote(
            command_executor=f"http://{SELENIUM_HOST}:{SELENIUM_PORT}/wd/hub",
            options=options  
        )
        driver.get(f"https://www.fedsfm.ru/documents/terr-list")

        time.sleep(5)

        form_for_fio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[contains(@class, 'form-control')]"))
        )
        
        form_for_fio.send_keys(fio)
        form_for_fio.send_keys(Keys.RETURN)

        result_info = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//tbody"))
        )
        driver.save_screenshot(f'./result/screenshot/ten_site/{fio}.png')
    
        
        if len(result_info.get_attribute('outerHTML')) > 120:
            return {f'{fio}': 'да'}
        return {f'{fio}': 'нет'}
    
    finally:
        driver.quit()
        print('-----ten_site end')


# origins = [
#     'http://localhost:8000',
#     'http://localhost:3000',
#     f'http://{SELENIUM_HOST}:{SELENIUM_PORT}',
#     f'http://{SELENIUM_HOST}:{SELENIUM_PORT}',
#     '*',
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=['GET', 'POST', 'OPTIONS', 'DELETE', 'PATCH', 'PUT'],
#     allow_headers=['Content-Type',
#                    'Set-Cookie',
#                    'Access-Control-Allow-Headers',
#                    'Access-Control-Allow-Origin',
#                    'Authorization'],
# )