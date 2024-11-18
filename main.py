import oracledb ### pip install oracledb
from oracledb import DatabaseError 
import pandas as pd
import json
import re

with open('secret.txt', 'r', encoding='utf-8') as f:
    creds = json.load(f)   
    user = creds['user']
    pwd = creds['password']
    dsn = creds['dsn']

def criar_tabela():
    with open('create.sql','r',encoding='utf-8') as f_sql:
        sql_create = f_sql.readlines()
        
    with open('create_seq.sql','r',encoding='utf-8') as f_sql:
        leitor = f_sql.read()
        padrao = re.compile(r"CREATE OR REPLACE TRIGGER[\s\S]*?END", re.IGNORECASE)

        sql_seq = padrao.findall(leitor)
        # print(sql_seq)

    with oracledb.connect(dsn=dsn, user=user, password=pwd) as conn:
        try:
            cursor = conn.cursor()
            for create in sql_create:
                cursor.execute(create)
                
            for seq in sql_seq:    
                cursor.execute(seq)
            print("Tabelas criadas com sucesso!")
            
            conn.commit()
        except DatabaseError as dbe:
            print(dbe.args[0])
    
def menu():
    print("")