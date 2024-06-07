import pandas as pd
import sqlite3
import json

# Conectar ao banco de dados SQLite
db_dir = 'database/base.db'
conn = sqlite3.connect(db_dir)

# Definir a consulta SQL para buscar todos os dados da tabela 'produtos'
query = "SELECT * FROM produtos"

# Executar a consulta e carregar os dados em um DataFrame do Pandas
df = pd.read_sql_query(query, conn)

# Fechar a conexão com o banco de dados
conn.close()

# Converter os valores JSON da coluna 'attributes' em dicionários
df['attributes'] = df['attributes'].apply(lambda x: json.loads(x))

# Criar colunas individuais para cada atributo em 'attributes'
for row in df['attributes']:
    for attribute in row:
        df[attribute['name']] = attribute['value_name']

# Drop da coluna original 'attributes'
df.drop(columns=['attributes'], inplace=True)

# Salvar os dados transformados de volta no banco de dados
conn = sqlite3.connect(db_dir)
df.to_sql('produtos_transformados', conn, if_exists='replace', index=False)
conn.close()