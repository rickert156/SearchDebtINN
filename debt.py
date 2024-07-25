import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


inn_search = input('Введите ИНН: ')

def rosdolgi(inn_search):
    params = {'inn':f'{inn_search}'}
    print('\nИдет поиск по rosdolgi.ru ...')
    query = requests.get('https://rosdolgi.ru/nalogi', params=params)
    if query.status_code == 200:
        try:
            bs = BeautifulSoup(query.text, 'lxml')
            result_search = bs.find(attrs={'data-amount': True})
            print(f'Задолженность -{result_search["data-amount"]} | Источник: rosdolgi.ru')
        except:print(f'Налоговая задолженность по ИНН {inn_search} не найдена')
    else:print(f'Доступ запрещен: {query.status_code}')

def nalogi(inn_search):
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    print('\nИдет поиск по nalogi.online ...')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f'https://nalogi.online/?query={inn_search}')
    try:
        debts = driver.find_element(By.CLASS_NAME, 'debt.ng-scope.checked.single').text
        result_debts, ru = debts.split(' ')
        print(f'Задолженность {result_debts} | Источник: nalogi.online')
    except:
        print(f'Налоговой задолженности по ИНН {inn_search} не найдено')
    

if __name__ == '__main__':
    rosdolgi(inn_search)
    nalogi(inn_search)