import sqlite3 as lite
import datetime

con = lite.connect("dados.db")

################ TABELA PESSOA ################

def inserirPessoa(pessoa):
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Pessoa (nome, contato, documento, tipo) VALUES (?, ?, ?, ?)", pessoa)

def listarPessoas():
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Pessoa")
        return cur.fetchall()

def atualizarPessoa(idPessoa, nome, contato, documento, tipo):
    with con:
        cur = con.cursor()
        cur.execute("""
            UPDATE Pessoa SET nome = ?, contato = ?, documento = ?, tipo = ? WHERE id = ?
        """, (nome, contato, documento, tipo, idPessoa))

def deletarPessoa(idPessoa):
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM Pessoa WHERE id = ?", (idPessoa,))

################ TABELA PRODUTO ################
def inserirProduto(nome):
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Produto (nome) VALUES (?)", (nome,))

def listarProdutos():
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Produto")
        return cur.fetchall()

def deletarProduto(idProduto):
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM Produto WHERE id = ?", (idProduto,))

################ TABELA ESTOQUE ################

def inserirEstoque(idProduto, tipo_produto, quantidade):
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Estoque (idProduto, tipo_produto, quantidade) VALUES (?, ?, ?)", 
                    (idProduto, tipo_produto, quantidade))

def listarEstoque():
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Estoque")
        return cur.fetchall()

def atualizarEstoque(idEstoque, quantidade):
    with con:
        cur = con.cursor()
        cur.execute("UPDATE Estoque SET quantidade = ? WHERE id = ?", (quantidade, idEstoque))

################ TABELA SERVICO ################

def inserirServico(servico):
    with con:
        cur = con.cursor()
        cur.execute("""
            INSERT INTO Servico (status, objetivo, data_inicio, data_fim, tempo, valor_final, idPessoa)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, servico)

def listarServicos(status=None):
    with con:
        cur = con.cursor()
        if status:
            cur.execute("""
                SELECT 
                    s.id,
                    s.idPessoa,
                    s.objetivo,
                    s.valor_final,
                    s.data_inicio,
                    s.data_fim,
                    s.tempo
                FROM Servico s
                WHERE s.status = ?
            """, (status,))
        else:
            cur.execute("""
                SELECT 
                    s.id,
                    s.idPessoa,
                    s.objetivo,
                    s.valor_final,
                    s.data_inicio,
                    s.data_fim,
                    s.tempo
                FROM Servico s
            """)
        return cur.fetchall()
    
def listarServicosComPessoa(status=None):
    with con:
        cur = con.cursor()
        if status:
            cur.execute("""
                SELECT 
                    s.id,
                    s.idPessoa,
                    s.objetivo,
                    s.valor_final,
                    s.data_inicio,
                    s.data_fim,
                    s.tempo,
                    p.nome,
                    p.tipo
                FROM Servico s
                JOIN Pessoa p ON s.idPessoa = p.id
                WHERE s.status = ?
            """, (status,))
        else:
            cur.execute("""
                SELECT 
                    s.id,
                    s.idPessoa,
                    s.objetivo,
                    s.valor_final,
                    s.data_inicio,
                    s.data_fim,
                    s.tempo,
                    p.nome,
                    p.tipo
                FROM Servico s
                JOIN Pessoa p ON s.idPessoa = p.id
            """)
        return cur.fetchall()
    
def atualizarServico(idServico, status, objetivo, data_inicio, data_fim, tempo, valor_final):
    with con:
        cur = con.cursor()
        cur.execute("""
            UPDATE Servico SET status = ?, objetivo = ?, data_inicio = ?, data_fim = ?, tempo = ?, valor_final = ? 
            WHERE id = ?
        """, (status, objetivo, data_inicio, data_fim, tempo, valor_final, idServico))

def deletarServico(idServico):
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM Servico WHERE id = ?", (idServico,))

################ TABELA UTILIZA ################

def vincularProdutoAoServico(idProduto, idServico, produtos_usados, quantidade):
    with con:
        cur = con.cursor()
        cur.execute("""
            INSERT INTO Utiliza (idProduto, idServico, produtos_usados, quantidade)
            VALUES (?, ?, ?, ?)
        """, (idProduto, idServico, produtos_usados, quantidade))

def listarProdutosPorServico():
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Utiliza")
        return cur.fetchall()

################ TABELA VENDA ################

def inserirVenda(venda):
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Venda (valor, produtos, data, idPessoa) VALUES (?, ?, ?, ?)", venda)

def listarVendas():
    with con:
        cur = con.cursor()
        cur.execute("""
            SELECT 
                v.id,
                v.valor,
                v.produtos,
                v.data,
                v.idPessoa,
                p.nome,
                p.tipo
            FROM Venda v
            JOIN Pessoa p ON v.idPessoa = p.id
        """)
        return cur.fetchall()

def deletarVenda(idVenda):
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM Venda WHERE id = ?", (idVenda,))

################ COMANDO  ################

def obterValores():
    dados = []

    for servico in listarServicosComPessoa():
        id_, idPessoa, objetivo, valor, data_inicio, data_fim, tempo, nomePessoa, tipoPessoa = servico
        dados.append((
            id_,
            data_inicio,
            nomePessoa,
            "Entrada",
            f"Serviço: {objetivo}",
            valor
        ))

    for venda in listarVendas():
        idVenda, valor, produtos, data, idPessoa, nome, tipo = venda
        dados.append((
            idVenda,
            data,
            nome,
            "Saída",
            f"Venda: {produtos}",
            valor
        ))

    return dados

def tarefaJanelaPrincipal(tabela, calendario, conexao, cor_evento):
    try:
        cur = conexao.cursor()
        cur.execute("""
            SELECT 
                s.data_fim,
                s.valor_final,
                p.nome
            FROM Servico s
            JOIN Pessoa p ON s.idPessoa = p.id
            WHERE s.data_fim IS NOT NULL
        """)
        resultados = cur.fetchall()
    except Exception as e:
        print("Erro ao carregar tarefas:", e)
        return

    for data_fim, valor, nome in resultados:
        try:
            if isinstance(data_fim, str):
                try:
                    data = datetime.datetime.strptime(data_fim, "%Y-%m-%d").date()
                except:
                    data = datetime.datetime.strptime(data_fim, "%d-%m-%Y").date()
            else:
                data = data_fim

            calendario.calevent_create(data, "Entrega", "entrega")
            calendario.tag_config("entrega", background=cor_evento, foreground="white")

            data_str = data.strftime("%d/%m/%Y")
            valor_str = f"R$ {float(valor):.2f}" if valor else "R$ 0,00"
            tabela.insert("", "end", values=(nome, data_str, valor_str))
        except Exception as e:
            print(f"Erro ao processar tarefa: {e}")