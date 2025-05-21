import sqlite3
 
conn = sqlite3.connect("database.db")
cursor = conn.cursor()
 
tabela = 'produtos'  # ou 'usuarios'
 
cursor.execute(f"PRAGMA table_info({tabela});")
colunas = [col[1] for col in cursor.fetchall()]
 
cursor.execute(f"SELECT * FROM {tabela};")
registros = cursor.fetchall()
 
print(f"Dados da tabela '{tabela}':")
print(" | ".join(colunas))
print("-" * 40)
for registro in registros:
    print(" | ".join(str(c) for c in registro))
cursor.executescript(
    '''
    CREATE TABLE if not exists produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT not null,
            categoria TEXT not null,
            quantidade INTEGER not null,
            preco REAL not null
);
'''
)
conn.commit()
conn.close()
# print("Banco de dados criado com sucesso")