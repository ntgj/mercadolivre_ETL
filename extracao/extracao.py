import pandas as pd
import requests
import json
import sqlite3

# Conectar ao banco de dados SQLite
db_dir = 'database/base.db'
conn = sqlite3.connect(db_dir)
c = conn.cursor()

# Define a base URL da API do Mercado Livre
search_url = 'https://api.mercadolibre.com/sites/MLB/search?q='

# Solicita ao usuário que insira a pesquisa
search = input("Insira aqui a sua pesquisa: ")

# Codifica a pesquisa para garantir que a URL esteja correta
search_encoded = requests.utils.quote(search)

# Inicializa a página e a lista que irá armazenar os resultados
page = 1
results = []

# Loop para buscar todas as páginas
while True:
    # Faz a requisição para a API
    url = f"{search_url}{search_encoded}&offset={(page-1)*50}"
    print(f"Solicitando URL: {url}")  # Adicionado para depuração
    r = requests.get(url)
    
    # Verifica se a requisição foi bem-sucedida
    if r.status_code == 200:
        data = r.json()
        
        # Verifica se a chave 'results' está presente na resposta
        if 'results' in data:
            results += data['results']
            print(f"Página {page} processada. Total de itens coletados até agora: {len(results)}")
        else:
            print("Nenhum resultado encontrado ou formato de resposta inesperado.")
            print(f"Resposta da API: {data}")
            break
        
        # Verifica se há mais páginas a serem buscadas
        if 'paging' in data and page < data['paging']['total'] // 50 + 1:
            page += 1
        else:
            break
    else:
        print(f"Erro na requisição: {r.status_code}")
        print(f"URL solicitada: {url}")
        print(f"Resposta da API: {r.text}")
        break

# Lista para armazenar os dicionários de dados
dados_formatados = []
keys = ['price', 'title', 'condition', 'listing_type_id', 'buying_mode', 'domain_id',
         'currency_id', 'original_price', 'sale_price', 'available_quantity', 
         'accepts_mercadopago', 'attributes']

# Loop sobre os itens do JSON
for item in results:
    # Dicionário para armazenar os valores correspondentes às chaves especificadas
    item_formatado = {}
    
    # Iterar sobre as chaves especificadas
    for key in keys:
        # Verificar se a chave está presente no item
        if key in item:
            # Se a chave for 'attributes' e o valor for uma lista de dicionários, convertemos para JSON
            if key == 'attributes' and isinstance(item[key], list):
                item_formatado[key] = json.dumps(item[key])
            else:
                item_formatado[key] = item[key]
        else:
            # Se a chave não estiver presente, adicionar None
            item_formatado[key] = None
    
    # Adicionar o dicionário do item à lista de dados formatados
    dados_formatados.append(item_formatado)

# Criar dataframe Pandas a partir da lista de dicionários
df = pd.DataFrame(dados_formatados)

# Print dos dados formatados
print("Primeiros 5 itens dos dados formatados:")
print(df.head())

# Defina o nome da tabela no banco de dados
tabela = 'produtos'

# Inserir o dataframe no banco de dados
df.to_sql(tabela, conn, if_exists='replace', index=False)

# Fechar a conexão com o banco de dados
conn.close()

# Exibe a quantidade total de itens encontrados e algumas amostras
print(f"Total de itens encontrados: {len(results)}")
print(df)
