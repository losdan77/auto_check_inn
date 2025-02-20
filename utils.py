import os
from dotenv import load_dotenv

load_dotenv()

SELENIUM_HOST = os.getenv('SELENIUM_HOST')

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)',
    'Mozilla/5.0 (X11; Linux i686; rv:7.0a1) Gecko/20110603 SeaMonkey/2.2a1pre',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/[WEBKIT_VERSION] (KHTML, like Gecko, Mediapartners-Google) Chrome/[CHROME_VERSION] Safari/[WEBKIT_VERSION]',
]

def clear_result_folder():
    folder_name_array = ['five_site', 'fourth_site', 'second_site', 'seven_site', 'ten_site', 'third_site']
    
    for folder in folder_name_array:
        folder_path = f'./result/screenshot/{folder}'
        # Проверяем, существует ли папка
        if not os.path.exists(folder_path):
            print(f"Папка {folder_path} не существует.")
            return

        # Перебираем все элементы в папке
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            
            # Удаляем файл или папку
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)  # Удаляем файл или символическую ссылку
    
    folder_path = f'./result/'
    # Перебираем все элементы в папке
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        
        # Удаляем файл или папку
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.unlink(item_path)  # Удаляем файл или символическую ссылку
    
    return 