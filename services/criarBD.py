import sqlite3 as lite

con = lite.connect("dados.db")


#Nossas TABELAS!!!

with con:
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Pessoa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            contato TEXT,
            tipo TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Categoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Receitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria_id INTEGER,
            adicionado_em DATE,
            valor REAL,
            FOREIGN KEY (categoria_id) REFERENCES Categoria(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria_id INTEGER,
            retirado_em DATE,
            valor REAL,
            FOREIGN KEY (categoria_id) REFERENCES Categoria(id)
        )
    """)