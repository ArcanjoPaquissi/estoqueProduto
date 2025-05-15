import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT not null,
            categoria TEXT not null,
            quantidade INTEGER not null,
            preco REAL not null
)
'''
)
conn.commit()
conn.close()
print("Banco de dados criado com sucesso")