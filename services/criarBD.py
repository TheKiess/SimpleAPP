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
            tipo TEXT -- 'comprador', 'vendedor' ou 'ambos'
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
            nome_itens TEXT,
            idPessoa INTEGER,
            FOREIGN KEY (idPessoa) REFERENCES Pessoa(id)
        )
    """)

    # TABELA ITEM VENDA
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ItemVenda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idVenda INTEGER,
            idProduto INTEGER,
            quantidade INTEGER,
            valor_unitario REAL,
            FOREIGN KEY (idVenda) REFERENCES Venda(id),
            FOREIGN KEY (idProduto) REFERENCES Produto(id)
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
            tempo TEXT -- duração estimada ou real
        )
    """)

    # TABELA DO PRODUTO COM SERVIÇO
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Utiliza (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idProduto INTEGER,
            idServico INTEGER,
            quantidade INTEGER,
            valor REAL,
            FOREIGN KEY (idProduto) REFERENCES Produto(id),
            FOREIGN KEY (idServico) REFERENCES Servico(id)
        )
    """)

    # TABELA AGENDA
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Agenda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idPessoa INTEGER,
            idServico INTEGER,
            FOREIGN KEY (idPessoa) REFERENCES Pessoa(id),
            FOREIGN KEY (idServico) REFERENCES Servico(id)
        )
    """)