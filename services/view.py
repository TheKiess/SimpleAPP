import sqlite3
import sqlite3 as lite
import datetime
import json

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
        cur.execute("""
            SELECT 
                e.id, 
                p.nome, 
                e.tipo_produto, 
                e.quantidade 
            FROM Estoque e
            JOIN Produto p ON e.idProduto = p.id
        """)
        return cur.fetchall()

def atualizarEstoque(idEstoque, quantidade):
    with con:
        cur = con.cursor()
        cur.execute("UPDATE Estoque SET quantidade = ? WHERE id = ?", (quantidade, idEstoque))


################ MOVIMENTAÇÃO DE ESTOQUE ################

def listarMovimentacoesPorEstoque(idEstoque):
    with con:
        cur = con.cursor()
        cur.execute("""
            SELECT 
                me.quantidade_movimentada,
                me.data_movimentacao,
                p.nome,
                e.tipo_produto
            FROM MovimentacaoEstoque me
            JOIN Estoque e ON me.idEstoque = e.id
            JOIN Produto p ON e.idProduto = p.id
            WHERE me.idEstoque = ?
            ORDER BY me.data_movimentacao DESC
        """, (idEstoque,))
        return cur.fetchall()
    
def listarMovimentacoesPorEstoque(idEstoque):
    with con:
        cur = con.cursor()
        cur.execute("""
            SELECT 
                m.id,
                m.quantidade_movimentada,
                m.data_movimentacao,
                p.nome,
                e.tipo_produto
            FROM MovimentacaoEstoque m
            JOIN Estoque e ON m.idEstoque = e.id
            JOIN Produto p ON e.idProduto = p.id
            WHERE m.idEstoque = ?
            ORDER BY m.data_movimentacao DESC
        """, (idEstoque,))
        return cur.fetchall()
    
def buscarEstoquePorProduto(idProduto):
    with con:
        cur = con.cursor()
        cur.execute("SELECT id, quantidade FROM Estoque WHERE idProduto = ?", (idProduto,))
        return cur.fetchone()

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


################ TABELA HISTORICO PAGAMENTO  ################

def registrarPagamentoParcial(id_servico, valor_parcial):

    if valor_parcial <= 0:
        return {"status": "erro", "mensagem": "O valor parcial deve ser maior que zero."}

    try:
        conexao = sqlite3.connect('dados.db')
        cursor = conexao.cursor()

        # Busca o valor atual do serviço
        cursor.execute("SELECT valor_final FROM Servico WHERE id = ?", (id_servico,))
        resultado = cursor.fetchone()

        if resultado is None:
            return {"status": "erro", "mensagem": "Serviço não encontrado."}

        valor_atual = resultado[0]
        novo_valor = valor_atual - valor_parcial

        if novo_valor < 0:
            return {
                "status": "erro",
                "mensagem": f"Pagamento excede o valor restante (R$ {valor_atual:.2f})."
            }

        cursor.execute("UPDATE Servico SET valor_final = ? WHERE id = ?", (novo_valor, id_servico))

        data_pagamento = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        
        cursor.execute("""
            INSERT INTO HistoricoPagamento (idServico, valor_pago, data_pagamento)
            VALUES (?, ?, ?)
        """, (id_servico, valor_parcial, data_pagamento))

        conexao.commit()
        return {
            "status": "sucesso",
            "mensagem": f"Pagamento de R$ {valor_parcial:.2f} registrado com sucesso! Valor restante: R$ {novo_valor:.2f}"
        }

    except sqlite3.Error as e:
        conexao.rollback()
        return {"status": "erro", "mensagem": f"Erro no banco de dados: {str(e)}"}

    finally:
        conexao.close()

################ TABELA MOVIMENTAÇÃO COMPRA  ################

def salvarCompraNoBanco(venda):
    with con:
        cur = con.cursor()

        # Isso vai colocar a venda dentro do BD
        produtos_json = json.dumps(venda["produtos"])
        cur.execute("""
            INSERT INTO Venda (valor, produtos, data, idPessoa)
            VALUES (?, ?, ?, ?)
        """, (venda["valor"], produtos_json, venda["data"], venda["idPessoa"]))
        idVenda = cur.lastrowid

        # Cada produto que vir ele terá inserido será colocado e atualizado
        for prod in venda["produtos"]:
            idProduto = prod["id"]
            quantidade = prod["quantidade"]

            cur.execute("""
                INSERT INTO MovimentacaoCompra (idProduto, idEstoque, idVenda, quantidade, tipo_movimentacao, data)
                VALUES (?, NULL, ?, ?, 'entrada', ?)
            """, (idProduto, idVenda, quantidade, venda["data"]))

            estoque = buscarEstoquePorProduto(idProduto)
            if estoque:
                idEstoque, qtdAtual = estoque
                novaQtd = qtdAtual + quantidade
                atualizarEstoque(idEstoque, novaQtd)
            else:
                cur.execute("""
                    INSERT INTO Estoque (idProduto, quantidade)
                    VALUES (?, ?)
                """, (idProduto, quantidade))

def atualizarValorFinal(id_servico, valor_antigo, valor_novo):
    try:
        diferenca = valor_antigo - valor_novo

        conn = sqlite3.connect("dados.db")
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Servico
            SET valor_final = valor_final + ?
            WHERE id = ?
        """, (diferenca, id_servico))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Erro ao ajustar valor_final: {e}")
        return False

################ TABELA MOVIMENTAÇÃO SERVIÇO  ################

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
            f"Compra: {produtos}",
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