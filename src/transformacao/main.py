# Importações necessárias para este projeto
import pandas as pd
import sqlite3
from datetime import datetime

# Definição do caminho para o Json
df = pd.read_json('../data/data.jsonl', lines=True)

# Mostra todas as colunas
pd.options.display.max_columns = None

# Adição da coluna source com valor fixo
df['_source'] = 'https://lista.mercadolivre.com.br/smartphone#topkeyword'

# Adição da coluna data_coleta
df['_data_coleta'] = datetime.now()

# Tratando os valore nulos para colunas de numero e de texto
df['old_price'] = df['old_price'].fillna(0).astype(float)
df['old_price_cents'] = df['old_price_cents'].fillna(0).astype(float)
df['new_price'] = df['new_price'].fillna(0).astype(float)
df['new_price_cents'] = df['new_price_cents'].fillna(0).astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0).astype(float)

# Remove os parênteses
df['reviews_amount'] = df['reviews_amount'].str.replace('[\(\)]', '', regex=True)
df['reviews_amount'] = df['reviews_amount'].fillna(0).astype(int)

# Trata e soma o valor inteiro com os sentavos
df['old_price_total'] = df['old_price'] + df['old_price_cents'] / 100
df['new_price_total'] = df['new_price'] + df['new_price_cents'] / 100

# Remove as colunas antigas
df.drop(columns=['old_price', 'old_price_cents', 'new_price', 'new_price_cents'])

# Conecta ao banco de dados SQLite
conn = sqlite3.connect('../data/quotes.db')

# Salvando DataFrame no banco de dados
df.to_sql('mercadolivre_items', conn, if_exists='replace', index=False)

# Encerra o banco
conn.close()
print(df.head())