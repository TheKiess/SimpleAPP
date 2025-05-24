import sqlite3 as lite

con = lite.connect("dados.db")

with con:
    cur = con.cursor()

    # TABELA PESSOA
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Pessoa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            contato TEXT,
            documento TEXT,
            tipo TEXT -- 'comprador', 'administrador', 'vendedor' ou 'ambos'
        )
    """)

    # TABELA PRODUTO
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Produto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT
        )
    """)

    # ESTOQUE
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_produto TEXT,
            quantidade INTEGER,
            idProduto INTEGER,
            FOREIGN KEY (idProduto) REFERENCES Produto(id)
        )
    """)

    # TABELA VENDA
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Venda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            valor REAL,
            produtos TEXT, -- pode armazenar info resumida ou string JSON
            data DATE,
            idPessoa INTEGER,
            FOREIGN KEY (idPessoa) REFERENCES Pessoa(id)
        )
    """)

    # TABELA SERVICO
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Servico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT,
            objetivo TEXT,
            data_inicio DATE,
            data_fim DATE,
            tempo TEXT, -- duração estimada ou real
            valor_final REAL,
            idPessoa INTEGER,
            FOREIGN KEY (idPessoa) REFERENCES Pessoa(id)
        )
    """)

    # TABELA DO PRODUTO COM SERVIÇO
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Utiliza (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idProduto INTEGER,
            idServico INTEGER,
            produtos_usados TEXT,
            quantidade INTEGER,
            FOREIGN KEY (idProduto) REFERENCES Produto(id),
            FOREIGN KEY (idServico) REFERENCES Servico(id)
        )
    """)