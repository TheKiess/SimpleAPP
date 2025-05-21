import sqlite3 as lite

con = lite.connect("dados.db")


# PESSOA

def inserirPessoa(pessoa):
    """Insere uma nova pessoa."""
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Pessoa (nome, contato, tipo) VALUES (?, ?, ?)", pessoa)

def listarPessoas():
    """Retorna todas as pessoas."""
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Pessoa")
        return cur.fetchall()

def deletarPessoa(idPessoa):
    """Remove pessoa pelo ID."""
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM Pessoa WHERE id = ?", (idPessoa,))

def atualizarPessoa(idPessoa, nome, contato, tipo):
    """Atualiza os dados de uma pessoa."""
    with con:
        cur = con.cursor()
        cur.execute("""
            UPDATE Pessoa 
            SET nome = ?, contato = ?, tipo = ?
            WHERE id = ?
        """, (nome, contato, tipo, idPessoa))

def obterValores():
    """Retorna receitas formatadas para exibição na tabela de valores."""
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

# CATEGORIA

def inserirCategoria(nomeCategoria):
    """Insere uma nova categoria."""
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Categoria (nome) VALUES (?)", (nomeCategoria,))

def listarCategorias():
    """Retorna todas as categorias."""
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Categoria")
        return cur.fetchall()

def deletarCategoria(idCategoria):
    """Remove categoria pelo ID."""
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM Categoria WHERE id = ?", (idCategoria,))


# RECEITAS

def inserir_receita(receita):
    """Insere uma nova receita."""
    with con:
        cur = con.cursor()
        cur.execute("""
            INSERT INTO Receitas (data, idPessoa, tipo, motivo, valor, categoria_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, receita)

def listarReceitas():
    """Retorna todas as receitas."""
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Receitas")
        return cur.fetchall()

def deletarReceita(idReceita):
    """Remove receita pelo ID."""
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM Receitas WHERE id = ?", (idReceita,))

# TAREFAS

def inserir_tarefa(tarefa):
    """Insere nova tarefa."""
    with con:
        cur = con.cursor()
        cur.execute("""
            INSERT INTO Tarefa (idPessoa, objetivo, valor, data_recebida, data_entregue, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, tarefa)

def listarTarefas(status=None):
    """Retorna tarefas com ou sem filtro por status ('ativo' ou 'finalizado')."""
    with con:
        cur = con.cursor()
        if status:
            cur.execute("SELECT * FROM Tarefa WHERE status = ?", (status,))
        else:
            cur.execute("SELECT * FROM Tarefa")
        return cur.fetchall()

def atualizar_status_tarefa(idTarefa, novoStatus):
    with con:
        cur = con.cursor()
        cur.execute("UPDATE Tarefa SET status = ? WHERE id = ?", (novoStatus, idTarefa))

def deletar_tarefa(idTarefa):
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM Tarefa WHERE id = ?", (idTarefa,))