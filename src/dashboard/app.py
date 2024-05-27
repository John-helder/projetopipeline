import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect('../data/quotes.db')

df = pd.read_sql_query('SELECT * FROM mercadolivre_items', conn)
conn.close()

st.title('Pesquisa de mercado - Celulares no Mercado Livre')

col1, col2, col3 = st.columns(3)

total_items = df.shape[0]
col1.metric(label="Valor total de itens", value=total_items)

unique_brands = df['barnd'].nunique()
col2.metric(label='Numnero de marcas unicas', value=unique_brands)

average_new_price = df['new_price'].mean()
col3.metric(label='Preço médio (R$)', value=f"{average_new_price:.2f}")

st.subheader('Marcas mais encontradas até a pagina 10')
col1, col2 = st.columns([4, 2])
pages_10_brands = df['barnd'].value_counts().sort_values(ascending=False)
col1.bar_chart(pages_10_brands)
col2.write(pages_10_brands)

st.subheader('Preço médio por marca')
col1, col2 = st.columns([4, 2])
price_mean_brands = df.groupby('barnd')['new_price'].mean().sort_values(ascending=False)
col1.bar_chart(price_mean_brands)
col2.write(price_mean_brands)

st.subheader('Satisfação por marca')
col1, col2 = st.columns([4, 2])
df_no_reviews = df[df['reviews_rating_number'] > 0]
satisfacion_by_brand = df_no_reviews.groupby('barnd')['reviews_rating_number'].mean().sort_values(ascending=False)
col1.bar_chart(satisfacion_by_brand)
col2.write(satisfacion_by_brand)
