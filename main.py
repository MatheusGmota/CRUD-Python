import oracledb ### pip install oracledb
from oracledb import DatabaseError 
from sqlalchemy import create_engine ### pip install sqlalchemy
import pandas as pd
import json
import re

with open('secret.txt', 'r', encoding='utf-8') as f:
    creds = json.load(f)   
    user = creds['user']
    pwd = creds['password']
    dsn = creds['dsn']

engine = create_engine(f"oracle+oracledb://{user}:{pwd}@{dsn}")

def criar_tabela():
    arquivo_sql = "FIAP3.sql"
    with open(arquivo_sql, "r", encoding="utf-8") as f:
        comandos = f.read()
        
    with oracledb.connect(dsn=dsn, user=user, password=pwd) as conn:
        try:
            cursor = conn.cursor()
            for comando in comandos.split(";"):
                if comando.strip(): 
                    cursor.execute(comando)
                    
            conn.commit()
        except DatabaseError as dbe:
            print(dbe.args[0])

def obter_entrada(n_opcoes:int, texto='Selecione uma opção de ') -> int:
    o = ''
    _ = [str(i+1) for i in range(n_opcoes)]
    str_n = str(_).replace(',', ' -').replace("'", "")
    
    o = input(texto + str_n +": ").strip()
    while not o.isdigit() or o not in _:
        o = input('Opção inválida!'+ texto + str_n + ": ").strip()
    return int(o)

def obter_tipo_fonte() -> int:
    tipos_fontes = ["Solar", "Eólica", "Hidrelétrica", "Geotérmica", "Biomassa"]
    for i, tipo in enumerate(tipos_fontes):
        print(i + 1, " - ", tipo)
        
    return obter_entrada(len(tipos_fontes),"Informe o ID do tipo de fonte associado ")

def obter_regiao():
    regioes = ["Norte", "Sul", "Leste", "Oeste", "Centro-Oeste"]
    for i, regiao in enumerate(regioes):
        print(i + 1, " - ", regiao)
        
    return obter_entrada(len(regioes),"Informe o ID da região associada: ")

def inserir():
    print(100*"=")
    print("INSERIR\n")
    
    dados_projeto = {
        "DESCRICAO": [input("Informe a descrição do projeto: ")],
        "CUSTO": [float(input("Informe o custo do projeto: "))],
        "STATUS": [input("Informe o status do projeto (Concluído/Em andamento): ")],
        "ID_TIPO_FONTE": [obter_tipo_fonte()],
        "ID_REGIAO": [obter_regiao()]
    }
    
    df_projeto = pd.DataFrame(dados_projeto)
    
    dados_emissao = {
        "ID_TIPO_FONTE": [df_projeto["ID_TIPO_FONTE"].iloc[0]],
        "EMISSAO": [float(input("Informe o valor da emissão (em toneladas): "))]
    }
    
    df_emissao = pd.DataFrame(dados_emissao)
    
    try:
        df_projeto.to_sql("projetos_sustentaveis", engine, if_exists="append", index=False)
        df_emissao.to_sql("emissoes_carbono", engine, if_exists="append", index=False)
        print("Dados inseridos com sucesso")
    except DatabaseError as dbe:
        print("Erro ao inserir dados. Erro:", dbe.args[0])
    except Exception as e:
        print("Erro ao inserir dados. Erro:", e)
    
def alterar():
    print(100*"=")
    print("ALTERAR\n")
    try:
        with oracledb.connect(dsn=dsn, user=user, password=pwd) as conn:
            cursor = conn.cursor()
            
            tabela_opcoes = ["Projetos Sustentáveis", "Emissões de Carbono"]
            print("Selecione a tabela que deseja alterar:")
            for i, tabela in enumerate(tabela_opcoes):
                print(f"{i+1} - {tabela}")
            tabela_selecionada = obter_entrada(len(tabela_opcoes))
            
            if tabela_selecionada == 1:
                tabela = "projetos_sustentaveis"
                coluna_id = "ID_PROJETO"
            elif tabela_selecionada == 2:
                tabela = "emissoes_carbono"
                coluna_id = "ID_EMISSAO"
            
            id_registro = input(f"Informe o ID do registro que deseja alterar na tabela {tabela}: ").strip()
            
            print("Informe os campos que deseja atualizar (deixe em branco para não alterar):")
            campos = []
            
            if tabela == "projetos_sustentaveis":
                descricao = input("Nova descrição: ").strip()
                if descricao:
                    campos.append(f"DESCRICAO = '{descricao}'")
                
                custo = input("Novo custo: ").strip()
                if custo:
                    campos.append(f"CUSTO = {float(custo)}")
                
                status = input("Novo status (Concluído/Em andamento): ").strip()
                if status:
                    campos.append(f"STATUS = '{status}'")
                
                tipo_fonte = input("Novo ID do tipo de fonte: ").strip()
                if tipo_fonte:
                    campos.append(f"ID_TIPO_FONTE = {int(tipo_fonte)}")
                
                regiao = input("Novo ID da região: ").strip()
                if regiao:
                    campos.append(f"ID_REGIAO = {int(regiao)}")
            
            elif tabela == "emissoes_carbono":
                tipo_fonte = input("Novo ID do tipo de fonte: ").strip()
                if tipo_fonte:
                    campos.append(f"ID_TIPO_FONTE = {int(tipo_fonte)}")
                
                emissao = input("Novo valor da emissão (em toneladas): ").strip()
                if emissao:
                    campos.append(f"EMISSAO = {float(emissao)}")
            
            if campos:
                update_query = f"UPDATE {tabela} SET {', '.join(campos)} WHERE {coluna_id} = {id_registro}"
                cursor.execute(update_query)
                conn.commit()
                print("Registro atualizado com sucesso.")
            else:
                print("Nenhum campo foi alterado.")
    
    except DatabaseError as dbe:
        print("Erro ao alterar dados:", dbe.args[0])
    except Exception as e:
        print("Erro ao alterar dados:", e)

def excluir():
    print(100*"=")
    print("EXCLUIR")
    
    try:
        with oracledb.connect(dsn=dsn, user=user, password=pwd) as conn:
            cursor = conn.cursor()
            
            tabela_opcoes = ["Projetos Sustentáveis", "Emissões de Carbono"]
            print("Selecione a tabela que deseja excluir:")
            for i, tabela in enumerate(tabela_opcoes):
                print(f"{i+1} - {tabela}")
            tabela_selecionada = obter_entrada(len(tabela_opcoes))
            
            if tabela_selecionada == 1:
                tabela = "projetos_sustentaveis"
                coluna_id = "ID_PROJETO"
            elif tabela_selecionada == 2:
                tabela = "emissoes_carbono"
                coluna_id = "ID_EMISSAO"
            
            id_registro = input(f"Informe o ID do registro que deseja excluir na tabela {tabela}: ").strip()
            
            delete_query = f"DELETE FROM {tabela} WHERE {coluna_id} = {id_registro}"
            cursor.execute(delete_query)
            conn.commit()
            print("Registro excluído com sucesso.")
    
    except DatabaseError as dbe:
        print("Erro ao excluir dados:", dbe.args[0])
    except Exception as e:
        print("Erro ao excluir dados:", e)

def consultar():
    consultas = [
        "SELECT ps.id_projeto, ps.descricao, ps.custo FROM projetos_sustentaveis ps LEFT JOIN tipo_fontes tf ON ps.id_tipo_fonte = tf.id_tipo_fonte WHERE tf.id_tipo_fonte = :1 ORDER BY ps.descricao ASC", 
        "SELECT id_projeto, descricao, status, custo FROM projetos_sustentaveis WHERE custo > :1 ORDER BY id_projeto ASC",
        "SELECT id_projeto, descricao, status FROM projetos_sustentaveis WHERE status = :1 ORDER BY id_projeto ASC"
    ]
    
    print(100*"=")
    print("CONSULTAR\n")
    print("1 - Por tipo de fonte\n"
        "2 - Por custo (apareceram projetos com custos acima do valor dado)\n"
        "3 - Por status\n"
        "4 - Voltar")
    
    indice = obter_entrada(4)
    
    if indice != 4:
        sql = consultas[indice - 1]
        
        match indice: 
            case 1:
                entrada = obter_tipo_fonte()
            case 2:
                entrada = float(input("Informe o custo do projeto: "))
            case 3:
                entrada = input("Informe o status do projeto (Concluído/Em andamento): ")
        try:
            
            with oracledb.connect(dsn=dsn, user=user, password=pwd) as conn:
                cursor = conn.cursor()
                
                resposta = cursor.execute(sql, (entrada,))
                dados = resposta.fetchmany(10) 
            
            for dado in dados:
                print(str(dado).replace(", ", " - "))
        except DatabaseError as dbe:
            print("Erro:", dbe.args[0])
        except Exception as e:
            print(e)
    
        
def menu():
    print(100*"=")
    print("MENU\n")
    
    opcoes = ["Inserir", "Alterar", "Excluir", "Consultar", "Sair"]
    for i, elemento in enumerate(opcoes): 
        print(i+1, '-', elemento)
    entrada = obter_entrada(len(opcoes))
    
    match entrada:
        case 1:
            inserir()
        case 2:
            alterar()
        case 3:
            excluir()
        case 4:
            consultar()
        case _:
            print("Saindo ...")
            quit(1)
    menu()
        
menu()