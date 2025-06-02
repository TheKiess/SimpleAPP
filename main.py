from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from PIL import Image, ImageTk
from collections import defaultdict
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import datetime
from services.view import *
from services.view import tarefaJanelaPrincipal, listarServicos
import json

################# CORES!!! ###############

co0 = "#2e2d2b"  # background preto
co1 = "#feffff"  # branca
co2 = "#4fa882"  # verde
co3 = "#38576b"  # valor
co4 = "#403d3d"  # cores das letras
co5 = "#FF8DA1"  # Rosa
co6 = "#038cfc"  # azul
co7 = "#15d100"  # verde
co8 = "#263238"  # Verde musgo escuro
co9 = "#FF0000" # Vermelho

################# TELA INICIAL APÓS LOGIN ###############

def janelaPrincipal():
    loginJanela.destroy()

    janela = Tk()
    janela.title("Mari Pontinhos de Amor")
    janela.geometry("900x650")
    janela.configure(background=co0)
    janela.resizable(width=FALSE, height=FALSE)

    style = ttk.Style(janela)
    style.theme_use("clam")

    # DIV CIMA
    divCima = Frame(janela, width=900, height=90, background=co6, relief="flat")
    divCima.grid(row=0, column=0, sticky="nsew")

    appImg = Image.open('Images/icone.jpg')
    appImg = appImg.resize((250, 70))
    appImg = ImageTk.PhotoImage(appImg)

    appLogo = Label(divCima, image=appImg, text="  Sistema de gestão", compound=LEFT,
                    background=co6, fg=co1, anchor=NW, font=("Verdana", 20), relief="raised")
    appLogo.image = appImg
    appLogo.place(x=10, y=5)

    topoBotoes = Frame(divCima, background=co6)
    topoBotoes.place(x=550, y=25)

    ttk.Button(topoBotoes, text="GESTÃO", command=janelaGestor).grid(row=0, column=0, padx=5)
    ttk.Button(topoBotoes, text="PESSOAS", command=janelaPessoas).grid(row=0, column=1, padx=5)
    ttk.Button(topoBotoes, text="VALORES", command=janelaValor).grid(row=0, column=2, padx=5)

    # DIV MEIO
    divMeio = Frame(janela, width=900, height=460, background=co8, relief="flat")
    divMeio.grid(row=1, column=0, padx=10, sticky="nsew")

    tituloAgenda = Label(divMeio, text="Calendário e agenda", font=("Verdana", 25, "bold"),
                         background=co8, foreground=co1)
    tituloAgenda.grid(row=0, column=0, columnspan=2, pady=(30, 10), sticky=N)

    frameCalendario = Frame(divMeio, background=co0, bd=2, relief="solid")
    frameCalendario.grid(row=1, column=0, padx=20, pady=30, sticky=N)
    frameCalendario.grid_propagate(False)

    hoje = datetime.date.today()
    calendario = Calendar(frameCalendario, selectmode='day', year=hoje.year, month=hoje.month, day=hoje.day,
                          background=co6, disabledbackground='white',
                          bordercolor=co0, headersbackground=co6,
                          normalbackground='white', foreground=co0, headersforeground=co0,
                          font=("Verdana", 14), headersfont=("Verdana", 12),
                          selectforeground="white", selectbackground=co8)
    calendario.pack(padx=10, pady=10, expand=True, fill="both")

    # TABELA
    frameTabela = Frame(divMeio, background=co8, bd=2, relief="solid")
    frameTabela.grid(row=1, column=1, padx=20, pady=30, sticky=N)
    colunas = ["nome", "entrega", "valor"]
    tabela = ttk.Treeview(frameTabela, columns=colunas, show="headings", height=12)

    tabela.heading("nome", text="Nome da Pessoa")
    tabela.heading("entrega", text="Data de Entrega")
    tabela.heading("valor", text="Valor")

    tabela.column("nome", width=150, anchor="center")
    tabela.column("entrega", width=100, anchor="center")
    tabela.column("valor", width=75, anchor="center")

    tabela.bind("<Button-1>", lambda e: "break" if tabela.identify_region(e.x, e.y) == "separator" else None)
    tabela.grid_propagate(False)
    tabela.pack()

    tarefaJanelaPrincipal(tabela, calendario, con, co9)

    # LEGENDA
    legendaFrame = Frame(divMeio, background=co8)
    legendaFrame.grid(row=2, column=0, pady=(0, 20), sticky=N)

    legendas = [
        ("black", "Dia atual"),
        (co9, "Data de entrega"),
        (co7, "Feriado"),
    ]

    for cor, texto in legendas:
        bloco = Frame(legendaFrame, width=20, height=10, bg=cor)
        bloco.pack(side=LEFT, padx=(10, 5), pady=34)

        label = Label(legendaFrame, text=texto, bg=co8, fg=co1, font=("Verdana", 10))
        label.pack(side=LEFT, padx=(0, 20))

    # DIV BAIXO
    divBaixo = Frame(janela, width=900, height=50, background=co6, relief="flat")
    divBaixo.grid(row=2, column=0, pady=0, padx=10, sticky="nsew")

    copyright_label = Label(divBaixo, text="© 2025 Frank Kiess - Todos os direitos reservados",
                            bg=co6, fg=co1, font=("Verdana", 10))
    copyright_label.pack(side=RIGHT, padx=10, pady=10)

    janela.mainloop()


def janelaPessoas():

    def formatarCelular(event):
        widget = event.widget
        texto = widget.get()
        numeros = ''.join(filter(str.isdigit, texto))[:11]
        formatado = ""
        if len(numeros) >= 1:
            formatado = f"({numeros[:2]}"
        if len(numeros) >= 3:
            formatado += f") {numeros[2]}"
        if len(numeros) >= 4:
            formatado += f" {numeros[3:7]}"
        if len(numeros) >= 8:
            formatado += f"-{numeros[7:11]}"
        widget.delete(0, "end")
        widget.insert(0, formatado)

    def carregarPessoas():
        tabela.delete(*tabela.get_children())
        for pessoa in listarPessoas():
            tabela.insert("", "end", values=pessoa)

    def cadastrar():
        def loginAdmin():
            def salvarLogin():
                login = entryLogin.get()
                senha = entrySenha.get()
                if login and senha:
                    entry_login_admin["login"] = login
                    entry_login_admin["senha"] = senha
                    janelaLogin.destroy()
                else:
                    mensagemAdmin.config(text="Preencha login e senha!")

            janelaLogin = Toplevel(janelaCadastro)
            janelaLogin.title("Login do Administrador")
            janelaLogin.geometry("300x180")
            janelaLogin.configure(bg=co0)
            janelaLogin.resizable(False, False)

            Label(janelaLogin, text="Login", bg=co0, fg=co1).pack(pady=(15, 0))
            entryLogin = Entry(janelaLogin)
            entryLogin.pack()

            Label(janelaLogin, text="Senha", bg=co0, fg=co1).pack(pady=(10, 0))
            entrySenha = Entry(janelaLogin, show="*")
            entrySenha.pack()

            mensagemAdmin = Label(janelaLogin, text="", bg=co0, fg="red")
            mensagemAdmin.pack(pady=(5, 0))

            Button(janelaLogin, text="Salvar", command=salvarLogin).pack(pady=10)

        def salvar():
            nome = entryNome.get()
            celular = entryCelular.get()
            documento = entryDocumento.get()
            tipo = tipoVar.get()

            if nome and celular and documento and tipo:
                inserirPessoa((nome, celular, documento, tipo))
                carregarPessoas()
                janelaCadastro.destroy()
            else:
                mensagem.config(text="Preencha todos os campos corretamente!")

        def on_tipo_selected(event):
            if tipoVar.get() == "administrador":
                loginAdmin()

        entry_login_admin = {"login": "", "senha": ""}

        janelaCadastro = Toplevel(janelaPessoas)
        janelaCadastro.title("Cadastrar Pessoa")
        janelaCadastro.geometry("280x320")
        janelaCadastro.configure(bg=co0)
        janelaCadastro.resizable(False, False)

        Label(janelaCadastro, text="Nome", bg=co0, fg=co1).pack(pady=(15, 0))
        entryNome = Entry(janelaCadastro)
        entryNome.pack()

        Label(janelaCadastro, text="Celular", bg=co0, fg=co1).pack(pady=(10, 0))
        entryCelular = Entry(janelaCadastro)
        entryCelular.pack()
        entryCelular.bind("<KeyRelease>", formatarCelular)

        Label(janelaCadastro, text="Documento", bg=co0, fg=co1).pack(pady=(10, 0))
        entryDocumento = Entry(janelaCadastro)
        entryDocumento.pack()

        Label(janelaCadastro, text="Tipo", bg=co0, fg=co1).pack(pady=(10, 0))
        tipoVar = StringVar()
        comboTipo = ttk.Combobox(janelaCadastro, textvariable=tipoVar, state="readonly")
        comboTipo["values"] = ["comprador", "vendedor", "ambos", "administrador"]
        comboTipo.pack()
        comboTipo.bind("<<ComboboxSelected>>", on_tipo_selected)

        mensagem = Label(janelaCadastro, text="", bg=co0, fg="red")
        mensagem.pack()

        Button(janelaCadastro, text="Salvar", command=salvar).pack(pady=10)

    def editar():
        item = tabela.selection()
        if item:
            valores = tabela.item(item, "values")

            def salvar_edicao():
                novoNome = entryNome.get()
                novoCelular = entryCelular.get()
                novoDocumento = entryDocumento.get()
                novoTipo = tipoVar.get()
                if novoNome and novoCelular and novoDocumento and novoTipo:
                    atualizarPessoa(valores[0], novoNome, novoCelular, novoDocumento, novoTipo)
                    carregarPessoas()
                    janelaEditar.destroy()

            janelaEditar = Toplevel(janelaPessoas)
            janelaEditar.title("Editar Pessoa")
            janelaEditar.geometry("280x320")
            janelaEditar.configure(bg=co0)
            janelaEditar.resizable(False, False)

            Label(janelaEditar, text="Nome", bg=co0, fg=co1).pack(pady=(10, 0))
            entryNome = Entry(janelaEditar)
            entryNome.insert(0, valores[1])
            entryNome.pack()

            Label(janelaEditar, text="Celular", bg=co0, fg=co1).pack(pady=(10, 0))
            entryCelular = Entry(janelaEditar)
            entryCelular.insert(0, valores[2])
            entryCelular.pack()
            entryCelular.bind("<KeyRelease>", formatarCelular)

            Label(janelaEditar, text="Documento", bg=co0, fg=co1).pack(pady=(10, 0))
            entryDocumento = Entry(janelaEditar)
            entryDocumento.insert(0, valores[3])
            entryDocumento.pack()

            Label(janelaEditar, text="Tipo", bg=co0, fg=co1).pack(pady=(10, 0))
            tipoVar = StringVar()
            comboboxTipo = ttk.Combobox(janelaEditar, textvariable=tipoVar, state="readonly")
            comboboxTipo["values"] = ["comprador", "vendedor", "ambos", "administrador"]
            comboboxTipo.set(valores[4])
            comboboxTipo.pack()

            Button(janelaEditar, text="Salvar", command=salvar_edicao).pack(pady=20)

    def excluir():
        item = tabela.selection()
        if item:
            valores = tabela.item(item, "values")
            deletarPessoa(valores[0])
            tabela.delete(item)

    # ----- JANELA PRINCIPAL -----
    janelaPessoas = Toplevel()
    janelaPessoas.title("Cadastro de Pessoas")
    janelaPessoas.geometry("900x650")
    janelaPessoas.configure(background=co0)
    janelaPessoas.resizable(False, False)
    janelaPessoas.grid_rowconfigure(1, weight=1)
    janelaPessoas.grid_columnconfigure(0, weight=1)

    # DIV CIMA
    divCima = Frame(janelaPessoas, width=900, height=90, background=co6, relief="flat")
    divCima.grid(row=0, column=0, sticky="nsew")
    appImg = Image.open('Images/icone.jpg').resize((250, 70))
    appImg = ImageTk.PhotoImage(appImg)
    appLogo = Label(divCima, image=appImg, text="  Cadastros pessoais", compound=LEFT,
                    background=co6, fg=co1, anchor=NW, font=("Verdana", 20), relief="raised")
    appLogo.image = appImg
    appLogo.place(x=10, y=5)

    # DIV MEIO
    divMeio = Frame(janelaPessoas, width=900, height=460, background=co8, relief="flat")
    divMeio.grid(row=1, column=0, padx=10, sticky="nsew")
    divMeio.grid_propagate(False)
    divMeio.grid_rowconfigure(1, weight=1)
    divMeio.grid_columnconfigure(0, weight=1)

    titulo = Label(divMeio, text="Cadastro de Pessoas", font=("Verdana", 20, "bold"),
                   background=co8, foreground=co1)
    titulo.grid(row=0, column=0, pady=(10, 0), sticky="n")

    frameTabela = Frame(divMeio, background=co8, bd=2, relief="solid")
    frameTabela.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

    colunas = ["id", "nome", "contato", "documento", "tipo"]
    tabela = ttk.Treeview(frameTabela, columns=colunas, show="headings")
    tabela.grid(row=0, column=0, sticky="nsew")
    for col in colunas:
        tabela.heading(col, text=col.upper())
        tabela.column(col, anchor="center", width=100)

    frameTabela.grid_rowconfigure(0, weight=1)
    frameTabela.grid_columnconfigure(0, weight=1)

    # BOTÕES
    frameBotoes = Frame(divMeio, background=co8)
    frameBotoes.grid(row=2, column=0, pady=10)
    ttk.Button(frameBotoes, text="Cadastrar", command=cadastrar).pack(side=LEFT, padx=10)
    ttk.Button(frameBotoes, text="Editar", command=editar).pack(side=LEFT, padx=10)
    ttk.Button(frameBotoes, text="Excluir", command=excluir).pack(side=LEFT, padx=10)

    # RODAPÉ
    divBaixo = Frame(janelaPessoas, width=900, height=40, background=co6, relief="flat")
    divBaixo.grid(row=2, column=0, padx=10, sticky="ew")

    Label(divBaixo, text="© 2025 Frank Kiess - Todos os direitos reservados",
          bg=co6, fg=co1, font=("Verdana", 10)).pack(side=RIGHT, padx=10, pady=10)

    carregarPessoas()


def janelaValor():
    janelaValores = Toplevel()
    janelaValores.title("Controle de Valores")
    janelaValores.geometry("1100x650")
    janelaValores.configure(background=co0)
    janelaValores.resizable(width=FALSE, height=FALSE)
    janelaValores.grid_rowconfigure(1, weight=1)
    janelaValores.grid_columnconfigure(0, weight=3)
    janelaValores.grid_columnconfigure(1, weight=1)

    # DIV CIMA
    divCima = Frame(janelaValores, width=1000, height=90, background=co6, relief="flat")
    divCima.grid(row=0, column=0, columnspan=2, sticky="nsew")

    appImg = Image.open('Images/icone.jpg').resize((250, 70))
    appImgTk = ImageTk.PhotoImage(appImg)
    appLogo = Label(divCima, image=appImgTk, text="  Controle de Valores", compound=LEFT,
                    background=co6, fg=co1, anchor=NW, font=("Verdana", 20), relief="raised")
    appLogo.image = appImgTk
    appLogo.place(x=10, y=5)

    # DIV MEIO
    divMeio = Frame(janelaValores, background=co8, bd=2, relief="solid", width=600, height=460)
    divMeio.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    divMeio.grid_propagate(False)

    colunas = ["id", "data", "nome", "tipo", "motivo", "valor"]
    tabela = ttk.Treeview(divMeio, columns=colunas, show="headings")

    for col in colunas:
        tabela.heading(col, text=col.upper())

    largura_colunas = [25, 70, 130, 80, 150, 80]
    for col, largura in zip(colunas, largura_colunas):
        tabela.column(col, width=largura, anchor="center")

    tabela.pack(fill="both", expand=True)

    try:
        dadosValores = obterValores()
    except Exception as e:
        print("Erro ao obter dados:", e)
        dadosValores = []

    for dado in dadosValores:
        cor = "green" if dado[3] == "Entrada" else "red"
        tabela.insert("", "end", values=dado, tags=(cor,))

    tabela.tag_configure("green", background="#d0ffd0")
    tabela.tag_configure("red", background="#ffd0d0")

    # DIV GRAFICO
    frameGrafico = Frame(janelaValores, background=co8, bd=2, relief="solid", width=380, height=460)
    frameGrafico.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
    frameGrafico.grid_propagate(False)

    entradasMensais = defaultdict(float)
    saidasMensais = defaultdict(float)

    for dado in dadosValores:
        try:
            data = datetime.datetime.strptime(dado[1], "%d-%m-%Y")
        except ValueError:
            try:
                data = datetime.datetime.strptime(dado[1], "%Y-%m-%d")
            except:
                continue

        mes = data.strftime("%b")
        valor = float(dado[5]) if isinstance(dado[5], (int, float)) else float(dado[5].replace(",", "."))
        if dado[3] == "Entrada":
            entradasMensais[mes] += valor
        else:
            saidasMensais[mes] += valor

    todosMeses = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    mesesPresentes = sorted(set(list(entradasMensais.keys()) + list(saidasMensais.keys())),
                        key=lambda m: todosMeses.index(m))

    entradas = [entradasMensais[mes] for mes in mesesPresentes]
    saidas = [saidasMensais[mes] for mes in mesesPresentes]
    lucros = [entradasMensais[mes] - saidasMensais[mes] for mes in mesesPresentes]

    fig, ax = plt.subplots(figsize=(5, 3))
    x = range(len(mesesPresentes))
    ax.bar([i - 0.25 for i in x], saidas, width=0.25, label='Saídas', color='red')
    ax.bar(x, entradas, width=0.25, label='Entradas', color='green')
    ax.bar([i + 0.25 for i in x], lucros, width=0.25, label='Lucro', color='gold')

    ax.set_xticks(x)
    ax.set_xticklabels(mesesPresentes)
    ax.set_title("Resumo Financeiro Mensal")
    ax.set_ylabel("R$")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=frameGrafico)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # DIV BAIXO
    divBaixo = Frame(janelaValores, width=1000, height=40, background=co6, relief="flat")
    divBaixo.grid(row=2, column=0, columnspan=2, sticky="ew")
    Label(divBaixo, text="© 2025 Frank Kiess - Todos os direitos reservados",
          bg=co6, fg=co1, font=("Verdana", 10)).pack(side=RIGHT, padx=10, pady=10)


def janelaGestor():

    def formatar_data(event):
        entrada = event.widget
        texto = entrada.get()
        numeros = ''.join(filter(str.isdigit, texto))[:8]

        novo_texto = ""
        if len(numeros) >= 2:
            novo_texto += numeros[:2] + "-"
        else:
            novo_texto += numeros
        if len(numeros) >= 4:
            novo_texto += numeros[2:4] + "-"
        elif len(numeros) > 2:
            novo_texto += numeros[2:]
        if len(numeros) > 4:
            novo_texto += numeros[4:]

        entrada.delete(0, 'end')
        entrada.insert(0, novo_texto)

        if len(novo_texto) == 10:
            try:
                dia, mes, ano = map(int, novo_texto.split("-"))
                datetime.date(ano, mes, dia)
                entrada.config(bg="white")
            except ValueError:
                entrada.config(bg="#ffcccc")
        else:
            entrada.config(bg="white")

    def janelaAdicionarServico():
        janela = Toplevel()
        janela.title("Adicionar Serviço")
        janela.geometry("400x350")
        janela.configure(background=co0)
        janela.resizable(False, False)

        Label(janela, text="Cadastrar Novo Serviço", bg=co0, fg=co1, font=("Verdana", 14)).pack(pady=10)

        Label(janela, text="Descrição do Serviço:", bg=co0, anchor=W).pack(fill=X, padx=20)
        entrada_objetivo = Entry(janela, font=("Verdana", 10))
        entrada_objetivo.pack(padx=20, fill=X)

        Label(janela, text="Valor Cobrado (R$):", bg=co0, anchor=W).pack(fill=X, padx=20, pady=(10, 0))
        entrada_valor = Entry(janela, font=("Verdana", 10))
        entrada_valor.pack(padx=20, fill=X)

        Label(janela, text="Data de Entrega (opcional):", bg=co0, anchor=W).pack(fill=X, padx=20, pady=(10, 0))
        entrada_data_fim = Entry(janela, font=("Verdana", 10))
        entrada_data_fim.pack(padx=20, fill=X)
        entrada_data_fim.bind("<KeyRelease>", formatar_data)

        Label(janela, text="Pessoa vinculada:", bg=co0, anchor=W).pack(fill=X, padx=20, pady=(10, 0))
        pessoas = [p for p in listarPessoas() if p[4] in ("comprador", "ambos")]
        nomes = [p[1] for p in pessoas]
        pessoa_var = StringVar()
        combo_pessoa = ttk.Combobox(janela, textvariable=pessoa_var, values=nomes, font=("Verdana", 10), state="readonly")
        combo_pessoa.pack(padx=20, fill=X)

        def salvar_servico():
            objetivo = entrada_objetivo.get()
            valor = entrada_valor.get()
            nome_pessoa = pessoa_var.get()
            data_inicio = datetime.datetime.now().strftime("%d-%m-%Y")
            data_fim = entrada_data_fim.get().strip() or None

            if not (objetivo and valor and nome_pessoa):
                messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios!")
                return

            if data_fim:
                try:
                    dia, mes, ano = map(int, data_fim.split("-"))
                    datetime.date(ano, mes, dia)
                except ValueError:
                    messagebox.showerror("Erro", "Data de entrega inválida!")
                    return

            try:
                idPessoa = [p[0] for p in pessoas if p[1] == nome_pessoa][0]
                servico = ("ativo", objetivo, data_inicio, data_fim, None, float(valor), idPessoa)
                inserirServico(servico)
                messagebox.showinfo("Sucesso", "Serviço adicionado com sucesso!")
                janela.destroy()
                carregar_dados()
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao salvar: {e}")

        Button(janela, text="Salvar Serviço", bg="#4CAF50", fg="white", font=("Verdana", 10),
            command=salvar_servico).pack(pady=20)

        
    def janelaAdicionarProduto():
        janela = Toplevel()
        janela.title("Adicionar Produto")
        janela.geometry("300x200")
        janela.configure(background=co0)
        janela.resizable(False, False)

        Label(janela, text="Nome do Produto:", bg=co0, anchor=W).pack(fill=X, padx=20, pady=(20, 5))
        entrada_nome = Entry(janela, font=("Verdana", 10))
        entrada_nome.pack(padx=20, fill=X)

        def salvar_produto():
            nome = entrada_nome.get()
            if not nome:
                messagebox.showwarning("Aviso", "Digite o nome do produto.")
                return

            try:
                inserirProduto(nome)
                messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
                janela.destroy()
                carregar_dados()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar produto: {e}")

        Button(janela, text="Salvar Produto", bg="#4CAF50", fg="white", font=("Verdana", 10),
               command=salvar_produto).pack(pady=20)


    def janelaAdicionarEstoque():
        janela = Toplevel()
        janela.title("Adicionar Estoque")
        janela.geometry("350x250")
        janela.configure(background=co0)
        janela.resizable(False, False)

        Label(janela, text="Material/Cor:", bg=co0, anchor=W).pack(fill=X, padx=20, pady=(20, 0))
        entrada_tipo = Entry(janela, font=("Verdana", 10))
        entrada_tipo.pack(padx=20, fill=X)

        Label(janela, text="Quantidade:", bg=co0, anchor=W).pack(fill=X, padx=20, pady=(10, 0))
        entrada_quantidade = Entry(janela, font=("Verdana", 10))
        entrada_quantidade.pack(padx=20, fill=X)

        Label(janela, text="Produto:", bg=co0, anchor=W).pack(fill=X, padx=20, pady=(10, 0))
        produtos = listarProdutos()
        nomes = [p[1] for p in produtos]
        produto_var = StringVar()
        comboProduto = ttk.Combobox(janela, textvariable=produto_var, values=nomes, font=("Verdana", 10), state="readonly")
        comboProduto.pack(padx=20, fill=X)

        def salvar_estoque():
            tipo = entrada_tipo.get()
            qtd = entrada_quantidade.get()
            nome_produto = produto_var.get()

            if not (tipo and qtd and nome_produto):
                messagebox.showwarning("Aviso", "Preencha todos os campos!")
                return

            try:
                idProduto = [p[0] for p in produtos if p[1] == nome_produto][0]
                inserirEstoque(idProduto, tipo, int(qtd))
                messagebox.showinfo("Sucesso", "Estoque adicionado com sucesso!")
                janela.destroy()
                carregar_dados()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar estoque: {e}")

        Button(janela, text="Salvar Estoque", bg="#4CAF50", fg="white", font=("Verdana", 10),
               command=salvar_estoque).pack(pady=20)



    def janelaAdicionarCompra():
        janela = Toplevel()
        janela.title("Adicionar Compra")
        janela.geometry("400x550")
        janela.configure(background=co0)
        janela.resizable(False, False)

        Label(janela, text="Cadastrar Nova Compra", bg=co0, fg=co1, font=("Verdana", 14)).pack(pady=10)

        Label(janela, text="Valor Total (R$):", bg=co0, anchor=W).pack(fill=X, padx=20)
        entrada_valor = Entry(janela, font=("Verdana", 10))
        entrada_valor.pack(padx=20, fill=X)

        frame_produto = Frame(janela, bg=co0)
        frame_produto.pack(padx=20, pady=10, fill=X)

        Label(frame_produto, text="Produto:", bg=co0).grid(row=0, column=0, sticky=W)
        produtos = listarProdutos()
        nomes_produtos = [p[1] for p in produtos]
        produtoVar = StringVar()
        comboProduto = ttk.Combobox(frame_produto, textvariable=produtoVar, values=nomes_produtos, font=("Verdana", 10), state="readonly", width=15)
        comboProduto.grid(row=1, column=0, padx=(0, 5))

        Label(frame_produto, text="Quantidade:", bg=co0).grid(row=0, column=1, sticky=W)
        entrada_quantidade = Entry(frame_produto, font=("Verdana", 10), width=5)
        entrada_quantidade.grid(row=1, column=1, padx=(0, 5))

        def adicionarProduto():
            nome = produtoVar.get()
            qtd = entrada_quantidade.get()
            if not (nome and qtd.isdigit() and int(qtd) > 0):
                messagebox.showwarning("Aviso", "Selecione um produto e insira uma quantidade válida!")
                return
            lista_produtos.insert(END, f"{nome} - {qtd}")
            produtos_adicionados.append({
                "id": [p[0] for p in produtos if p[1] == nome][0],
                "nome": nome,
                "quantidade": int(qtd)
            })
            entrada_quantidade.delete(0, END)
            produtoVar.set("")

        Button(frame_produto, text="Adicionar", bg="#4CAF50", fg="white", font=("Verdana", 9),
            command=adicionarProduto).grid(row=1, column=2, padx=(5, 0))

        Label(janela, text="Produtos Adicionados:", bg=co0, anchor=W).pack(fill=X, padx=20)
        lista_produtos = Listbox(janela, font=("Verdana", 10), height=6)
        lista_produtos.pack(padx=20, fill=X)

        Button(janela, text="Remover Produto Selecionado", bg="#d9534f", fg="white", font=("Verdana", 10),
            command=lambda: removerProduto()).pack(pady=5)

        def removerProduto():
            idx = lista_produtos.curselection()
            if idx:
                lista_produtos.delete(idx)
                del produtos_adicionados[idx[0]]

        Label(janela, text="Data (DD-MM-AAAA):", bg=co0, anchor=W).pack(fill=X, padx=20, pady=(10, 0))
        entrada_data = Entry(janela, font=("Verdana", 10))
        entrada_data.pack(padx=20, fill=X)
        entrada_data.bind("<KeyRelease>", formatar_data)

        Label(janela, text="Pessoa que venderá:", bg=co0, anchor=W).pack(fill=X, padx=20, pady=(10, 0))
        pessoas = [p for p in listarPessoas() if p[4] in ("vendedor", "ambos")]
        nomes_pessoas = [p[1] for p in pessoas]
        pessoaVar = StringVar()
        comboPessoa = ttk.Combobox(janela, textvariable=pessoaVar, values=nomes_pessoas, font=("Verdana", 10), state="readonly")
        comboPessoa.pack(padx=20, fill=X)

        produtos_adicionados = []

        def salvarCompra():
            valor = entrada_valor.get()
            data = entrada_data.get()
            nome_pessoa = pessoaVar.get()

            if not (valor and data and nome_pessoa and produtos_adicionados):
                messagebox.showwarning("Aviso", "Preencha todos os campos e adicione pelo menos um produto!")
                return

            try:
                idPessoa = [p[0] for p in pessoas if p[1] == nome_pessoa][0]
                venda = {
                    "valor": float(valor),
                    "produtos": produtos_adicionados,
                    "data": data,
                    "idPessoa": idPessoa
                }
                salvarCompraNoBanco(venda)
                messagebox.showinfo("Sucesso", "Compra registrada com sucesso!")
                janela.destroy()
                carregar_dados()
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

        Button(janela, text="Salvar Compra", bg="#4CAF50", fg="white", font=("Verdana", 10),
            command=salvarCompra).pack(pady=20)
    
    def abrirDetalhesServico(event, tabela):
        def carregar_historico():
            tree_hist.delete(*tree_hist.get_children())
            conn = sqlite3.connect('dados.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id, valor_pago, data_pagamento FROM HistoricoPagamento WHERE idServico = ?", (idServico,))
            historico = cursor.fetchall()
            conn.close()
            for id_pag, valor_pg, data_pg in historico:
                tree_hist.insert("", "end", iid=id_pag, values=(f"R$ {valor_pg:.2f}", data_pg))

        item_selecionado = tabela.selection()
        if not item_selecionado:
            return

        valores = tabela.item(item_selecionado)["values"]
        idServico, nome, objetivo, valor, inicio, fim = valores

        janela = Toplevel()
        janela.title("Detalhes do Serviço")
        janela.geometry("550x500")
        janela.configure(background=co0)

        frame_topo = Frame(janela, bg=co0)
        frame_topo.pack(pady=10)

        frame_esquerda = Frame(frame_topo, bg=co0)
        frame_esquerda.pack(side="left", padx=20)
        Label(frame_esquerda, text=f"ID: {idServico}", font=("Verdana", 10), fg=co1, bg=co0).pack(pady=2)
        Label(frame_esquerda, text=f"Descrição: {objetivo}", font=("Verdana", 10), fg=co1, bg=co0).pack(pady=2)
        Label(frame_esquerda, text=f"Início: {inicio}", font=("Verdana", 10), fg=co1, bg=co0).pack(pady=2)

        frame_direita = Frame(frame_topo, bg=co0)
        frame_direita.pack(side="left", padx=20)
        Label(frame_direita, text=f"Nome: {nome}", font=("Verdana", 10), fg=co1, bg=co0).pack(pady=2)
        label_valor = Label(frame_direita, text=f"Valor atual: R$ {float(valor):.2f}", fg=co7, font=("Verdana", 10), bg=co0)
        label_valor.pack(pady=2)
        Label(frame_direita, text=f"Fim: {fim}", font=("Verdana", 10), fg=co1, bg=co0).pack(pady=2)

        Label(janela, text="Histórico de Pagamentos:", font=("Verdana", 10, "bold"), bg=co0).pack(pady=5)
        tree_hist = ttk.Treeview(janela, columns=("valor", "data"), show="headings")
        tree_hist.heading("valor", text="Valor Pago")
        tree_hist.heading("data", text="Data")
        tree_hist.column("valor", anchor="center", width=100)
        tree_hist.column("data", anchor="center", width=200)
        tree_hist.pack(pady=5, fill="x", padx=10)

        carregar_historico()

        frame_botoes = Frame(janela, bg=co0)
        frame_botoes.pack(pady=10)

        Label(frame_botoes, text="Valor parcial: R$", font=("Verdana", 10), bg=co0).pack(side="left")
        entry_valor = Entry(frame_botoes, width=10)
        entry_valor.pack(side="left", padx=5)

        def registrarPagamentoUI():
            try:
                valor_parcial = float(entry_valor.get())
                if valor_parcial <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erro", "Insira um valor válido e maior que zero.")
                return

            resultado = registrarPagamentoParcial(idServico, valor_parcial)
            if resultado["status"] == "sucesso":
                messagebox.showinfo("Sucesso", resultado["mensagem"])
                carregar_historico()

                conn = sqlite3.connect("dados.db")
                cursor = conn.cursor()
                cursor.execute("SELECT valor_final FROM Servico WHERE id = ?", (idServico,))
                novo_valor = cursor.fetchone()[0]
                conn.close()
                label_valor.config(text=f"Valor atual: R$ {novo_valor:.2f}")
                entry_valor.delete(0, END)
            else:
                messagebox.showerror("Erro", resultado["mensagem"])

        def editarPagamento():
            item = tree_hist.selection()
            if not item:
                messagebox.showwarning("Aviso", "Selecione um pagamento para editar.")
                return

            id_pagamento = int(item[0])
            valor_atual, _ = tree_hist.item(item, "values")

            janela_editar = Toplevel(janela)
            janela_editar.title("Editar Pagamento")
            janela_editar.geometry("300x180")
            janela_editar.configure(bg=co0)

            Label(janela_editar, text="Valor:", font=("Verdana", 10), bg=co0).pack(pady=5)
            entry_novo_valor = Entry(janela_editar)
            entry_novo_valor.insert(0, valor_atual.replace("R$ ", "").replace(",", "."))
            entry_novo_valor.pack()

            def salvarEdicao():
                try:
                    novo_valor = float(entry_novo_valor.get())
                except ValueError:
                    messagebox.showerror("Erro", "Insira um valor numérico válido.")
                    return

                valor_antigo = float(valor_atual.replace("R$ ", "").replace(",", "."))
                data_atual = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

                conn = sqlite3.connect("dados.db")
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE HistoricoPagamento
                    SET valor_pago = ?, data_pagamento = ?
                    WHERE id = ?
                """, (novo_valor, data_atual, id_pagamento))
                conn.commit()
                conn.close()

                sucesso = atualizarValorFinal(idServico, valor_antigo, novo_valor)
                if sucesso:
                    novo_total = float(label_valor.cget("text").split("R$ ")[1].replace(",", ".")) + (valor_antigo - novo_valor)
                    label_valor.config(text=f"Valor atual: R$ {novo_total:.2f}")
                    carregar_historico()
                    messagebox.showinfo("Sucesso", "Pagamento editado com sucesso.")
                    janela_editar.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao ajustar o valor total do serviço.")

            Button(janela_editar, text="Salvar", command=salvarEdicao, bg="#4CAF50", fg="white").pack(pady=10)

        def finalizarServicoUI():
            confirmar = messagebox.askyesno("Confirmar", "Deseja realmente finalizar este serviço?")
            if confirmar:
                resultado = finalizarServico(idServico)
                if resultado["status"] == "sucesso":
                    messagebox.showinfo("Sucesso", resultado["mensagem"])
                    janela.destroy()
                else:
                    messagebox.showerror("Erro", resultado["mensagem"])

        Button(frame_botoes, text="Registrar Pagamento", command=registrarPagamentoUI, bg="#4CAF50", fg="white").pack(side="left", padx=5)
        Button(frame_botoes, text="Editar Selecionado", command=editarPagamento).pack(side="left", padx=5)
        Button(frame_botoes, text="Finalizar Serviço", bg="red", fg="white", command=finalizarServicoUI).pack(side="left", padx=5)


    def abrirDetalhesCompra(event, tabela):
        item_selecionado = tabela.selection()
        if not item_selecionado:
            return

        valores = tabela.item(item_selecionado)["values"]
        id_venda, valor_total, produtos, data, id_pessoa, nome_pessoa, tipo_pessoa = valores

        janela = Toplevel()
        janela.title("Detalhes da Compra")
        janela.geometry("500x300")
        janela.configure(background=co0)

        Label(janela, text=f"ID: {id_venda}", font=("Verdana", 10)).pack(pady=5)
        Label(janela, text=f"Valor Total: R$ {float(valor_total):.2f}", font=("Verdana", 10)).pack(pady=5)
        Label(janela, text=f"Produtos: {produtos}", font=("Verdana", 10), wraplength=450, justify="left").pack(pady=5)
        Label(janela, text=f"Data: {data}", font=("Verdana", 10)).pack(pady=5)
        Label(janela, text=f"Pessoa: {nome_pessoa} ({tipo_pessoa})", font=("Verdana", 10)).pack(pady=5)



    def abrirDetalhesEstoque(event, tabela):
        item_selecionado = tabela.selection()
        if not item_selecionado:
            return

        valores = tabela.item(item_selecionado)["values"]
        id_estoque, nome_produto, tipo, quantidade = valores

        janela = Toplevel()
        janela.title("Detalhes do Estoque")
        janela.geometry("600x400")
        janela.configure(background=co0)

        frame_topo = Frame(janela, bg=co0)
        frame_topo.pack(pady=10)

        frame_esquerda = Frame(frame_topo, bg=co0)
        frame_esquerda.pack(side="left", padx=20)

        Label(frame_esquerda, text=f"ID: {id_estoque}", font=("Verdana", 10), fg=co1, bg=co0).pack(pady=2)
        Label(frame_esquerda, text=f"Produto: {nome_produto}", font=("Verdana", 10), fg=co1, bg=co0).pack(pady=2)

        frame_direita = Frame(frame_topo, bg=co0)
        frame_direita.pack(side="left", padx=20)

        Label(frame_direita, text=f"Tipo: {tipo}", font=("Verdana", 10), fg=co1, bg=co0).pack(pady=2)
        label_quantidade = Label(frame_direita, text=f"Quantidade Atual: {quantidade}", font=("Verdana", 10), fg=co7, bg=co0)
        label_quantidade.pack(pady=2)

        Label(janela, text="Histórico de Movimentações:", font=("Verdana", 10, "bold"), bg=co0).pack(pady=5)

        tabela_mov = ttk.Treeview(janela, columns=("produto", "tipo", "quantidade", "data"), show="headings")
        tabela_mov.heading("produto", text="Produto")
        tabela_mov.heading("tipo", text="Tipo")
        tabela_mov.heading("quantidade", text="Quantidade")
        tabela_mov.heading("data", text="Data")

        tabela_mov.column("produto", width=150, anchor="center")
        tabela_mov.column("tipo", width=100, anchor="center")
        tabela_mov.column("quantidade", width=100, anchor="center")
        tabela_mov.column("data", width=150, anchor="center")

        tabela_mov.pack(padx=10, pady=5, fill="both", expand=True)

        movimentacoes = listarMovimentacoesPorEstoque(id_estoque)
        for quantidade_mov, data_mov, nome_prod, tipo_prod in movimentacoes:
            tabela_mov.insert("", "end", values=(nome_prod, tipo_prod, quantidade_mov, data_mov))


    janelaGestao = Toplevel()
    janelaGestao.title("Gestor de Serviços")
    janelaGestao.geometry("1000x700")
    janelaGestao.configure(background=co0)
    janelaGestao.resizable(False, False)

    # DIV CIMA
    divCima = Frame(janelaGestao, width=1000, height=90, background=co6)
    divCima.pack(side=TOP, fill=X)
    appImg = Image.open('Images/icone.jpg').resize((250, 70))
    appImg = ImageTk.PhotoImage(appImg)
    appLogo = Label(divCima, image=appImg, text="   Sistema de gestão", compound=LEFT,
                    background=co6, fg=co1, anchor=NW, font=("Verdana", 20), relief="raised")
    appLogo.image = appImg
    appLogo.place(x=10, y=5)

    notebook = ttk.Notebook(janelaGestao)
    notebook.pack(fill=BOTH, expand=True)

    # FRAMES PARA ABAS
    frameAtivos = Frame(notebook, bg=co8)
    frameFinalizados = Frame(notebook, bg=co8)
    frameProdutos = Frame(notebook, bg=co8)
    frameEstoque = Frame(notebook, bg=co8)
    frameCompras = Frame(notebook, bg=co8)

    notebook.add(frameAtivos, text="Serviços Ativos")
    notebook.add(frameFinalizados, text="Serviços Finalizados")
    notebook.add(frameProdutos, text="Produtos")
    notebook.add(frameEstoque, text="Estoque")
    notebook.add(frameCompras, text="Compras")

    # Tabelas
    colunaServico = ["id", "nome", "objetivo", "valor", "data_inicio", "data_fim"]
    tabelaAtivos = ttk.Treeview(frameAtivos, columns=colunaServico, show="headings")
    tabelaAtivos.pack(fill=BOTH, expand=True, padx=10, pady=10)
    tabelaAtivos.bind("<Double-1>", lambda event: abrirDetalhesServico(event, tabelaAtivos))

    for col in colunaServico:
        tabelaAtivos.heading(col, text=col.upper())
    largura_colunas_ativos = [25, 160, 160, 75, 40, 40]
    for col, largura in zip(colunaServico, largura_colunas_ativos):
        tabelaAtivos.column(col, width=largura, anchor="center")

    Button(frameAtivos, text="Adicionar Serviço", font=("Verdana", 10),
           bg="#4CAF50", fg="white", padx=10, command=janelaAdicionarServico).pack(pady=10)



    tabelaFinalizados = ttk.Treeview(frameFinalizados, columns=colunaServico, show="headings")
    tabelaFinalizados.pack(fill=BOTH, expand=True, padx=10, pady=10)

    for col in colunaServico:
        tabelaFinalizados.heading(col, text=col.upper())
    largura_colunas_finalizados = [25, 160, 160, 75, 40, 40]
    for col, largura in zip(colunaServico, largura_colunas_finalizados):
        tabelaFinalizados.column(col, width=largura, anchor="center")

    tabelaProdutos = ttk.Treeview(frameProdutos, columns=["id", "nome"], show="headings")
    tabelaProdutos.pack(fill=BOTH, expand=True, padx=10, pady=(10, 5))

    colunaProdutos = ["id", "nome"]
    for col in colunaProdutos:
        tabelaProdutos.heading(col, text=col.upper())
    largura_colunas_produtos = [25, 320]
    for col, largura in zip(colunaProdutos, largura_colunas_produtos):
        tabelaProdutos.column(col, width=largura, anchor="center")

    Button(frameProdutos, text="Adicionar Produto", font=("Verdana", 10),
           bg="#4CAF50", fg="white", padx=10, command=janelaAdicionarProduto).pack(pady=10)

    tabelaEstoque = ttk.Treeview(frameEstoque, columns=["id", "produto", "material/cor", "quantidade"], show="headings")
    tabelaEstoque.pack(fill=BOTH, expand=True, padx=10, pady=10)
    tabelaEstoque.bind("<Double-1>", lambda event: abrirDetalhesEstoque(event, tabelaEstoque))

    colunaEstoque = ["id", "produto", "material/cor", "quantidade"]
    for col in colunaEstoque:
        tabelaEstoque.heading(col, text=col.upper())

    largura_colunas_estoque = [25, 150, 45, 25]
    for col, largura in zip(colunaEstoque, largura_colunas_estoque):
        tabelaEstoque.column(col, width=largura, anchor="center")

    Button(frameEstoque, text="Adicionar Estoque", font=("Verdana", 10),
           bg="#4CAF50", fg="white", padx=10, command=janelaAdicionarEstoque).pack(pady=10)

    tabelaCompras = ttk.Treeview(frameCompras, columns=["id", "valor", "produtos", "data", "idPessoa", "nome", "tipo"], show="headings")
    tabelaCompras.pack(fill=BOTH, expand=True, padx=10, pady=(10, 5))
    tabelaCompras.bind("<Double-1>", lambda event: abrirDetalhesCompra(event, tabelaCompras))

    colunasCompras = ["id", "valor", "produtos", "data", "idPessoa", "nome", "tipo"]
    for col in colunasCompras:
        tabelaCompras.heading(col, text=col.upper())
    
    largura_colunas_compras = [25, 75, 120, 60, 25, 80, 30]
    for col, largura in zip(colunasCompras, largura_colunas_compras):
        tabelaCompras.column(col, width=largura, anchor="center")

    Button(frameCompras, text="Adicionar Compra", font=("Verdana", 10),
           bg="#4CAF50", fg="white", padx=10, command=janelaAdicionarCompra).pack(pady=10)

    # DIV BAIXO
    divBaixo = Frame(janelaGestao, height=40, background=co6)
    divBaixo.pack(side=BOTTOM, fill=X)
    Label(divBaixo, text="© 2025 Frank Kiess - Todos os direitos reservados",
          bg=co6, fg=co1, font=("Verdana", 10)).pack(side=RIGHT, padx=10, pady=10)

    # Função para carregar dados nas abas
    def carregar_dados():
        pessoas = {p[0]: (p[1], p[4]) for p in listarPessoas()}
        
        for tabela, status in [(tabelaAtivos, "ativo"), (tabelaFinalizados, "finalizado")]:
            for row in tabela.get_children():
                tabela.delete(row)
            for servico in listarServicos(status):
                id_, idPessoa, objetivo, valor, data_inicio, data_fim, _ = servico
                nome, _ = pessoas.get(idPessoa, (f"ID {idPessoa}", ""))
                tabela.insert("", "end", values=(id_, nome, objetivo, valor, data_inicio, data_fim))

        for row in tabelaProdutos.get_children():
            tabelaProdutos.delete(row)
        for produto in listarProdutos():
            tabelaProdutos.insert("", "end", values=produto)

        for row in tabelaEstoque.get_children():
            tabelaEstoque.delete(row)
        for item in listarEstoque():
            tabelaEstoque.insert("", "end", values=item)

        for row in tabelaCompras.get_children():
            tabelaCompras.delete(row)
        for venda in listarVendas():
            id_venda, valor, produtos_json, data, id_pessoa, *resto = venda
            try:
                produtos_lista = json.loads(produtos_json)
                nomes_produtos = ", ".join([f"{p['quantidade']} {p['nome']}" for p in produtos_lista])
            except Exception as e:
                print(f"Erro ao processar JSON de produtos: {e}")
                nomes_produtos = "Erro ao ler produtos"
            
            nome_pessoa, tipo_pessoa = pessoas.get(id_pessoa, (f"ID {id_pessoa}", ""))
            tabelaCompras.insert("", "end", values=(
                id_venda, valor, nomes_produtos, data, id_pessoa, nome_pessoa, tipo_pessoa
            ))


    carregar_dados()
    janelaGestao.mainloop()
    
################# SISTEMA DE LOGIN DO APLICATIVO ###############

def verificarLogin():
    usuario = entradaUsuario.get()
    senha = entradaSenha.get()

    # Simples verificação (substituir com validação real)
    if usuario == "" and senha == "":
        janelaPrincipal()
    else:
        aviso["text"] = "Usuário ou senha inválidos"


################# TELA UTILIZADA NO LOGIN

loginJanela = Tk()
loginJanela.title("Login")
loginJanela.geometry("300x200")
loginJanela.eval('tk::PlaceWindow %s center' % loginJanela.winfo_pathname(loginJanela.winfo_id()))
loginJanela.resizable(FALSE, FALSE)

# Fundo com imagem
img = Image.open("images/floral.jpg")
img = img.resize((300, 200))
backgroundImage = ImageTk.PhotoImage(img)
background_label = Label(loginJanela, image=backgroundImage)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

frame = Frame(loginJanela, bg="#ffffff", bd=0)
frame.place(relx=0.5, rely=0.5, anchor="center")

Label(frame, text="Usuário:", font=("Verdana", 10, "bold"), bg= "#ffffff", fg= "#000000").grid(row=0, column=0, sticky="w", padx=10, pady=(10, 2))
entradaUsuario = Entry(frame, bg='grey')
entradaUsuario.grid(row=1, column=0, padx=10)

Label(frame, text="Senha:", font=("Verdana", 10, "bold"), bg= "#ffffff", fg= "#000000").grid(row=2, column=0, sticky="w", padx=10, pady=(10, 2))
entradaSenha = Entry(frame, show="*", bg='grey')
entradaSenha.grid(row=3, column=0, padx=10)

aviso = Label(frame, text="", fg="red", bg="#ffffff", font=("Verdana", 8))
aviso.grid(row=4, column=0, pady=(5, 0))

ttk.Style().configure("TButton", font=("Verdana", 9))
ttk.Button(frame, text="Entrar", command=verificarLogin).grid(row=5, column=0, pady=10)

loginJanela.mainloop()