import requests
import time
import json
import mysql.connector
from  mysql.connector import Error
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Chaves, Erros, timer
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Download do Navegador Automatico
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service

# Validar a presença de qualquer elemento
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

url = "https://www.nba.com/stats/players/traditional"

top10ranking = {}

rankings = {
    '3points': {'field': 'FG3M', 'label': '3PM'},
    'points': {'field': 'PTS', 'label': 'PTS'},
    'assistants': {'field': 'AST', 'label': 'AST'},
    'rebounds': {'field': 'REB', 'label': 'REB'},
    'steals': {'field': 'STL', 'label': 'STL'},
    'blocks': {'field': 'BLK', 'label': 'BLK'}
}

def buildrank(type):

    field = rankings[type]['field']
    label = rankings[type]['label']
    
    # Aguarda elemento aparecer na tela, se caso nao aparecer em 60 segundos, retorna erro
    # Varre a pagina toda procurando o elemento
    get_field = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, f'//*[@field="{field}"]'))).click()

    element = driver.find_element('xpath', '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table')
    html_content = element.get_attribute('outerHTML')

    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    df_full = pd.read_html(str(table))[0].head(10)
    df = df_full[['Unnamed: 0', 'Player', 'Team', label]]
    df.columns = ['pos', 'player', 'team', 'total']

    return df.to_dict('records')

option = Options()
option.headless = True
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

driver.get(url)

for k in rankings:
    top10ranking[k] = buildrank(k)

driver.quit()


for i in top10ranking:
    # print(i)
    num = 0
    tabela = i
    while num < len(top10ranking[i]):
        # print(top10ranking[tabela][num]['pos'])
        con = mysql.connector.connect (host='localhost', database='nba',
        user='root', password= '')
        inserir_dados = fr"""
            UPDATE {tabela} SET player = {repr(top10ranking[tabela][num]['player'])}, team = {repr(top10ranking[tabela][num]['team'])}, total = {repr(top10ranking[tabela][num]['total'])} WHERE pos = {repr(top10ranking[tabela][num]['pos'])}
        """
        cursor = con.cursor() #"recebe informações"
        cursor.execute(inserir_dados)
        con.commit() #"para gravar no banco"
        num = num + 1

# js = json.dumps(top10ranking)
# fp = open('ranking.json', 'w')
# fp.write(js)
# fp.close()