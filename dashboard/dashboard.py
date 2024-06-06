import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# Conectar ao banco de dados SQLite
db_dir = 'database/base.db'
conn = sqlite3.connect(db_dir)

# Definir a consulta SQL para buscar todos os dados da tabela 'produtos_transformados'
query = "SELECT * FROM produtos_transformados"

# Executar a consulta e carregar os dados em um DataFrame do Pandas
df = pd.read_sql_query(query, conn)

# Fechar a conexão com o banco de dados
conn.close()

# Configurar a aplicação Streamlit
st.title('Visualização de Dados do Mercado Livre')

# Descrição do dashboard
st.write("""
    Este dashboard exibe dados de produtos do Mercado Livre, incluindo preço, condição, tipo de listagem,
    modo de compra e outras informações relevantes.
""")

# Tabela de dados
st.subheader('Dados dos Produtos')
st.write(df)

# Filtros interativos
st.sidebar.header('Filtros')
condition = st.sidebar.multiselect('Condição', df['condition'].unique())
listing_type_id = st.sidebar.multiselect('Tipo de Listagem', df['listing_type_id'].unique())
buying_mode = st.sidebar.multiselect('Modo de Compra', df['buying_mode'].unique())
domain_id = st.sidebar.multiselect('Domínio', df['domain_id'].unique())
accepts_mercadopago = st.sidebar.selectbox('Aceita Mercado Pago', [True, False])

# Aplicar filtros
df_filtered = df.copy()
if condition:
    df_filtered = df_filtered[df_filtered['condition'].isin(condition)]
if listing_type_id:
    df_filtered = df_filtered[df_filtered['listing_type_id'].isin(listing_type_id)]
if buying_mode:
    df_filtered = df_filtered[df_filtered['buying_mode'].isin(buying_mode)]
if domain_id:
    df_filtered = df_filtered[df_filtered['domain_id'].isin(domain_id)]
df_filtered = df_filtered[df_filtered['accepts_mercadopago'] == accepts_mercadopago]

# Sumários Estatísticos
st.subheader('Distribuição de Preços, Estoque e Mercado Pago')
st.write(df_filtered.describe())

# Gráficos
# Gráfico de Barras da Condição do Produto
st.subheader('Gráfico de Barras da Condição do Produto')
fig_condition, ax_condition = plt.subplots()
sns.countplot(x='condition', data=df_filtered, ax=ax_condition)
st.pyplot(fig_condition)

# Histograma de Preços
st.subheader('Histograma de Preços')
fig_hist_price, ax_hist_price = plt.subplots()
ax_hist_price.hist(df_filtered['price'].dropna(), bins=20, color='skyblue', edgecolor='black')
ax_hist_price.set_xlabel('Preço')
ax_hist_price.set_ylabel('Frequência')
st.pyplot(fig_hist_price)

# Gráfico de Barras das Marcas
st.subheader('Gráfico de Barras das Marcas')
fig_bar_brand, ax_bar_brand = plt.subplots()
sns.countplot(x='Marca', data=df_filtered, ax=ax_bar_brand)
ax_bar_brand.set_xticklabels(ax_bar_brand.get_xticklabels(), rotation=45)
st.pyplot(fig_bar_brand)

# Opção de exportação de dados
st.subheader('Exportar Dados')
st.write('Baixe os dados filtrados:')
csv = df_filtered.to_csv(index=False)
st.download_button(label="Baixar CSV", data=csv, mime='text/csv')
