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
    
    # MOVIMENTAÇÃO DO ESTOQUE
    cur.execute("""
        CREATE TABLE IF NOT EXISTS MovimentacaoEstoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idEstoque INTEGER,
            quantidade_movimentada INTEGER,
            data_movimentacao DATE,
            FOREIGN KEY (idEstoque) REFERENCES Estoque(id)
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

    # TABELA DO HISTORICO DE PAGAMENTO
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS HistoricoPagamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idServico INTEGER,
            valor_pago REAL,
            data_pagamento TEXT,
            FOREIGN KEY (idServico) REFERENCES Servico(id)
        )
    """)
    
    #TABELA DO HISTORICO DE MOVIMENTAÇÃO COMPRA -> ESTOQUE

    cur.execute("""
        CREATE TABLE IF NOT EXISTS MovimentacaoCompra (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idProduto INTEGER,
            idEstoque INTEGER,
            idVenda INTEGER,
            quantidade INTEGER,
            tipo_movimentacao TEXT, -- 'entrada' ou 'saida'
            data DATE,
            FOREIGN KEY (idProduto) REFERENCES Produto(id),
            FOREIGN KEY (idEstoque) REFERENCES Estoque(id),
            FOREIGN KEY (idVenda) REFERENCES Venda(id)
        )
    """)

    #TABELA DO HISTORICO DE MOVIMENTAÇÃO DO ESTOQUE -> SERVIÇO

    cur.execute("""
        CREATE TABLE IF NOT EXISTS MovimentacaoEstoqueServico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idProduto INTEGER,
            idEstoque INTEGER,
            idServico INTEGER,
            quantidade INTEGER,
            tipo_movimentacao TEXT, -- 'entrada' ou 'saida'
            data DATE,
            FOREIGN KEY (idProduto) REFERENCES Produto(id),
            FOREIGN KEY (idEstoque) REFERENCES Estoque(id),
            FOREIGN KEY (idServico) REFERENCES Servico(id)
        )
    """)