import sqlite3 as lite

con = lite.connect("dados.db")

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
            data DATE,
            idPessoa INTEGER,
            tipo TEXT,
            motivo TEXT,
            valor REAL,
            categoria_id INTEGER,
            FOREIGN KEY (idPessoa) REFERENCES Pessoa(id),
            FOREIGN KEY (categoria_id) REFERENCES Categoria(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Tarefa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idPessoa INTEGER,
            objetivo TEXT,
            valor REAL,
            data_recebida DATE,
            data_entregue DATE,
            status TEXT DEFAULT 'ativo',
            FOREIGN KEY (idPessoa) REFERENCES Pessoa(id)
        )
    """)