import json
import mysql.connector
from  mysql.connector import Error
  
# Opening JSON file
f = open('ranking.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)
  
# Iterating through the json
# list
for i in data:
    print(i)
    num = 0
    tabela = i
    while num < len(data[i]):
        # print(data[i][num])
        con = mysql.connector.connect (host='localhost', database='nba',
        user='root', password= '')
        inserir_dados = fr"""
            INSERT INTO {tabela} (pos, player, team, total) values ({repr(data[tabela][num]['pos'])}, {repr(data[tabela][num]['player'])}, {repr(data[tabela][num]['team'])}, {repr(data[tabela][num]['total'])})
        """
        cursor = con.cursor() #"recebe informações"
        cursor.execute(inserir_dados)
        con.commit() #"para gravar no banco"
        num = num + 1
  
# Closing file
f.close()