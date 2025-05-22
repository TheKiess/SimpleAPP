import sqlite3 as lite
import datetime

con = lite.connect("dados.db")

# PESSOA

def inserirPessoa(pessoa):
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Pessoa (nome, contato, documento, tipo) VALUES (?, ?, ?, ?)", pessoa)

def listarPessoas():
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Pessoa")
        return cur.fetchall()

def deletarPessoa(idPessoa):
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM Pessoa WHERE id = ?", (idPessoa,))

def atualizarPessoa(idPessoa, nome, contato, documento, tipo):
    with con:
        cur = con.cursor()
        cur.execute("""
            UPDATE Pessoa 
            SET nome = ?, contato = ?, documento = ?, tipo = ?
            WHERE id = ?
        """, (nome, contato, documento, tipo, idPessoa))

# CATEGORIA

def inserirCategoria(nomeCategoria):
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Categoria (nome) VALUES (?)", (nomeCategoria,))

def listarCategorias():
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Categoria")
        return cur.fetchall()

def deletarCategoria(idCategoria):
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM Categoria WHERE id = ?", (idCategoria,))

# PRODUTO

def inserirProduto(nomeProduto):
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Produto (nome) VALUES (?)", (nomeProduto,))

def listarProdutos():
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Produto")
        return cur.fetchall()

def deletarProduto(idProduto):
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM Produto WHERE id = ?", (idProduto,))

# ESTOQUE

def inserirEstoque(estoque):
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Estoque (idProduto, tipo_produto, quantidade) VALUES (?, ?, ?)", estoque)

def listarEstoque():
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Estoque")
        return cur.fetchall()

def atualizarEstoque(idEstoque, quantidade):
    with con:
        cur = con.cursor()
        cur.execute("UPDATE Estoque SET quantidade = ? WHERE id = ?", (quantidade, idEstoque))

# TAREFA (SERVIÇO)

def inserirTarefa(tarefa):
    with con:
        cur = con.cursor()
        cur.execute("""
            INSERT INTO Tarefa (idPessoa, objetivo, valor, data_recebida, data_entregue, status, tempo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, tarefa)

def listarTarefas(status=None):
    with con:
        cur = con.cursor()
        if status:
            cur.execute("SELECT * FROM Tarefa WHERE status = ?", (status,))
        else:
            cur.execute("SELECT * FROM Tarefa")
        return cur.fetchall()

def atualizarStatusTarefa(idTarefa, novoStatus):
    with con:
        cur = con.cursor()
        cur.execute("UPDATE Tarefa SET status = ? WHERE id = ?", (novoStatus, idTarefa))

def deletarTarefa(idTarefa):
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM Tarefa WHERE id = ?", (idTarefa,))

# PRODUTOS USADOS EM TAREFAS

def inserirProdutoUsado(produtoUsado):
    with con:
        cur = con.cursor()
        cur.execute("""
            INSERT INTO ProdutoUsado (idProduto, idTarefa, quantidade, valor_unitario)
            VALUES (?, ?, ?, ?)
        """, produtoUsado)

def listarProdutosUsados():
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM ProdutoUsado")
        return cur.fetchall()

# VENDA

def inserirVenda(venda):
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Venda (idPessoa, valor, data) VALUES (?, ?, ?)", venda)

def listarVendas():
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Venda")
        return cur.fetchall()

def deletarVenda(idVenda):
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM Venda WHERE id = ?", (idVenda,))

# ITENS DA VENDA

def inserirItemVenda(item):
    with con:
        cur = con.cursor()
        cur.execute("""
            INSERT INTO ItemVenda (idVenda, idProduto, quantidade, valor_unitario)
            VALUES (?, ?, ?, ?)
        """, item)

def listarItensVenda():
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM ItemVenda")
        return cur.fetchall()

# RECEITAS (FINANCEIRO)

def inserirReceita(receita):
    with con:
        cur = con.cursor()
        cur.execute("""
            INSERT INTO Receitas (data, idPessoa, tipo, motivo, valor, categoria_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, receita)

def listarReceitas():
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Receitas")
        return cur.fetchall()

def deletarReceita(idReceita):
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM Receitas WHERE id = ?", (idReceita,))

def obterValores():
    with con:
        cur = con.cursor()
        cur.execute("""
            SELECT 
                Receitas.id, 
                Receitas.data, 
                Pessoa.nome, 
                Receitas.tipo, 
                Receitas.motivo, 
                Receitas.valor
            FROM Receitas
            JOIN Pessoa ON Receitas.idPessoa = Pessoa.id
        """)
        return cur.fetchall()

# INTERFACE COM CALENDÁRIO E TABELA

def tarefaJanelaPrincipal(tabela, calendario, con, co9):
    try:
        with con:
            cur = con.cursor()
            cur.execute("""
                SELECT Pessoa.nome, Tarefa.data_entregue, Tarefa.valor
                FROM Tarefa
                JOIN Pessoa ON Tarefa.idPessoa = Pessoa.id
                WHERE Tarefa.status = 'ativo'
            """)
            tarefas = cur.fetchall()

        for item in tabela.get_children():
            tabela.delete(item)

        for nome, data_str, valor in tarefas:
            if data_str:
                ano, mes, dia = map(int, data_str.split("-"))
                data_formatada = f"{dia:02d}/{mes:02d}/{ano}"
                data_obj = datetime.date(ano, mes, dia)

                tabela.insert("", "end", values=(nome, data_formatada, f"{valor:.2f} R$"))
                calendario.calevent_create(data_obj, f"{nome}", "entrega")

        calendario.tag_config("entrega", foreground="white", background=co9)

    except Exception as e:
        print(f"Erro ao carregar tarefas: {e}")
