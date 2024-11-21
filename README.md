# Guia de uso 
## Primeiros passos
### **Instalação das bibliotecas**
Para isso você precisa abrir um novo terminal e executar os seguintes comandos:  
* **Atualize** o instalador pip
    ```bash
    python -m pip install --upgrade pip
    ```
* **Instale** as bibliotecas usadas
    ```bash
    pip install oracldb sqlalchemy
    ```
    ```bash
    pip install pandas
    ```
Para a aplicação rodar corretamente é necessário:  
* Realizar a criação do banco de dados, **utilizando o script do arquivo ```create.sql```**

* **Preencher** suas credenciais de conexão ao banco no arquivo ```secret.txt```

### Rodando a aplicação 
Abra um terminal e rode o seguinte comando:
```bash
python main.py
# ou
pyhton3 main.py
```