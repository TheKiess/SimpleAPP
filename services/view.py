import sqlite3 as lite

con = lite.connect("dados.db")

def inserirPessoa(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Pessoa (nome, contato, tipo) VALUES (?, ?, ?)"
        cur.execute(query, i)

inserirPessoa(["Marilei", "54996054694", "comprador"])


def inserirCategoria(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Categoria (nome) VALUES (?)"
        cur.execute(query, i)

inserirCategoria(["Alimentacao"])


def inserirReceitas(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Receitas (categoria_id, adicionado_em, valor) VALUES (?, ?, ?)"
        cur.execute(query, i)

inserirReceitas([1, "2025-05-16", 16.0])


def inserirGastos(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Gastos (categoria_id, retirado_em, valor) VALUES (?, ?, ?)"
        cur.execute(query, i)

inserirGastos([1, "2025-05-16", 20.0])

def deletarReceitas(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Receitas WHERE id=?"
        cur.execute(query, i)

def deletarGastos(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Gastos WHERE id=?"
        cur.execute(query, i)

def verCategoria():
    listaItens = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Categoria")
        linha = cur.fetchall()
        for l in linha:
            listaItens.append(l)
        
        return listaItens
    
print(verCategoria())