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

# Verificar o número total de registros carregados
print(f"Total de registros carregados: {len(df)}")

# Exibir os nomes das colunas disponíveis
print(df.columns)

# Exibir as primeiras linhas do DataFrame antes da transformação
print("Primeiras 5 linhas antes da transformação:")
print(df.head())

# Transformação dos dados da coluna 'attributes'
# Converter os valores JSON da coluna 'attributes' em dicionários
df['attributes'] = df['attributes'].apply(lambda x: json.loads(x))

# Criar colunas individuais para cada atributo em 'attributes'
for row in df['attributes']:
    for attribute in row:
        df[attribute['name']] = attribute['value_name']

# Excluir a coluna original 'attributes'
df.drop(columns=['attributes'], inplace=True)

# Exibir as primeiras linhas do DataFrame após a transformação
print("Primeiras 5 linhas após a transformação:")
print(df.head())

# Salvar os dados transformados de volta ao banco de dados
conn = sqlite3.connect(db_dir)
df.to_sql('produtos_transformados', conn, if_exists='replace', index=False)
conn.close()

# Também podemos salvar os dados transformados em um arquivo CSV
df.to_csv('transformed_data.csv', index=False)

# Exibir uma mensagem de conclusão
print("Transformação concluída e dados salvos.")
