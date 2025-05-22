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
            janelaLogin.resizable(width=FALSE, height=FALSE)

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
            tipo = tipoVar.get()
            if nome and celular and tipo:
                inserirPessoa((nome, celular, tipo))
                carregarPessoas()
                janelaCadastro.destroy()
            else:
                mensagem.config(text="Preencha todos os campos corretamente!")

        def on_tipo_selected(event):
            if tipoVar.get() == "Administrador":
                loginAdmin()

        entry_login_admin = {"login": "", "senha": ""}

        janelaCadastro = Toplevel(janelaPessoas)
        janelaCadastro.title("Cadastrar Pessoa")
        janelaCadastro.geometry("300x240")
        janelaCadastro.configure(bg=co0)
        janelaCadastro.resizable(width=FALSE, height=FALSE)

        Label(janelaCadastro, text="Nome", bg=co0, fg=co1).pack(pady=(15, 0))
        entryNome = Entry(janelaCadastro)
        entryNome.pack()

        Label(janelaCadastro, text="Celular", bg=co0, fg=co1).pack(pady=(10, 0))
        entryCelular = Entry(janelaCadastro)
        entryCelular.pack()
        entryCelular.bind("<KeyRelease>", formatarCelular)

        Label(janelaCadastro, text="Tipo", bg=co0, fg=co1).pack(pady=(10, 0))
        tipoVar = StringVar()
        comboTipo = ttk.Combobox(janelaCadastro, textvariable=tipoVar, state="readonly")
        comboTipo["values"] = ["Comprador", "Vendedor", "Comprador e Vendedor", "Administrador"]
        comboTipo.pack()
        comboTipo.bind("<<ComboboxSelected>>", on_tipo_selected)

        mensagem = Label(janelaCadastro, text="", bg=co0, fg="red")
        mensagem.pack()

        Button(janelaCadastro, text="Salvar", command=salvar).pack(pady=20)

    def editar():
        item = tabela.selection()
        if item:
            valores = tabela.item(item, "values")
            def salvar_edicao():
                novoNome = entryNome.get()
                novoCelular = entryCelular.get()
                novoTipo = tipoVar.get()
                if novoNome and novoCelular and novoTipo:
                    atualizarPessoa(valores[0], novoNome, novoCelular, novoTipo)
                    carregarPessoas()
                    janelaEditar.destroy()

            janelaEditar = Toplevel(janelaPessoas)
            janelaEditar.title("Editar Pessoa")
            janelaEditar.geometry("300x250")
            janelaEditar.configure(bg=co0)
            janelaEditar.resizable(width=FALSE, height=FALSE)

            Label(janelaEditar, text="Nome", bg=co0, fg=co1).pack(pady=(10, 0))
            entryNome = Entry(janelaEditar)
            entryNome.insert(0, valores[1])
            entryNome.pack()

            Label(janelaEditar, text="Celular", bg=co0, fg=co1).pack(pady=(10, 0))
            entryCelular = Entry(janelaEditar)
            entryCelular.insert(0, valores[2])
            entryCelular.pack()
            entryCelular.bind("<KeyRelease>", formatarCelular)

            Label(janelaEditar, text="Tipo", bg=co0, fg=co1).pack(pady=(10, 0))
            tipoVar = StringVar()
            comboboxTipo = ttk.Combobox(janelaEditar, textvariable=tipoVar, state="readonly")
            comboboxTipo["values"] = ["Comprador", "Vendedor", "Comprador e Vendedor", "Administrador"]
            comboboxTipo.set(valores[3])
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
    janelaPessoas.resizable(width=FALSE, height=FALSE)
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

    colunas = ["id", "nome", "celular", "tipo"]
    tabela = ttk.Treeview(frameTabela, columns=colunas, show="headings")
    for col in colunas:
        tabela.heading(col, text=col.capitalize())

    tabela.column("id", width=50, anchor="center")
    tabela.column("nome", width=300, anchor="center")
    tabela.column("celular", width=200, anchor="center")
    tabela.column("tipo", width=200, anchor="center")
    tabela.pack(fill="both", expand=True)

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

    # 🔄 INTEGRA COM BANCO
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
                data = datetime.datetime.strptime(dado[1], "%Y-%m-%d")  # Fallback
            except:
                continue

        mes = data.strftime("%b")
        valor = float(dado[5]) if isinstance(dado[5], (int, float)) else float(dado[5].replace(",", "."))
        if dado[3] == "Entrada":
            entradasMensais[mes] += valor
        else:
            saidasMensais[mes] += valor

    todosMeses = ["Jan", "Fev", "Mar", "Abr", "Maio", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    mesesPresentes = [m for m in todosMeses if m in entradasMensais or m in saidasMensais]

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

    janelaGestao = Toplevel()
    janelaGestao.title("Gestor de Tarefas")
    janelaGestao.geometry("900x650")
    janelaGestao.configure(background=co0)
    janelaGestao.resizable(False, False)

    # DIV CIMA
    divCima = Frame(janelaGestao, width=900, height=90, background=co6)
    divCima.pack(side=TOP, fill=X)
    appImg = Image.open('Images/icone.jpg')
    appImg = appImg.resize((250, 70))
    appImg = ImageTk.PhotoImage(appImg)
    appLogo = Label(divCima, image=appImg, text="   Sistema de gestão", compound=LEFT,
                    background=co6, fg=co1, anchor=NW, font=("Verdana", 20), relief="raised")
    appLogo.image = appImg
    appLogo.place(x=10, y=5)

    # DIV MEIO
    notebook = ttk.Notebook(janelaGestao)
    notebook.pack(fill=BOTH, expand=True)

    frameAdicionar = Frame(notebook, bg=co8)
    frameAtivos = Frame(notebook, bg=co8)
    frameFinalizados = Frame(notebook, bg=co8)

    # Função para carregar tarefas nas tabelas
    def carregar_tarefas():
        for tabela, status in [(tabelaAtivos, "ativo"), (tabelaFinalizados, "finalizado")]:
            for row in tabela.get_children():
                tabela.delete(row)
            tarefas = listarTarefas(status)
            for tarefa in tarefas:
                id_, idPessoa, objetivo, valor, data_recebida, data_entregue, _ = tarefa
                nome = f"ID {idPessoa}"  # Pode-se substituir por nome real, se necessário
                tabela.insert("", "end", values=(id_, nome, objetivo, valor, data_recebida, data_entregue))

    # PRIMEIRA ABA - ADICIONAR TAREFA
    notebook.add(frameAdicionar, text="Adicionar Tarefa")
    Label(frameAdicionar, text="Nova Tarefa", font=("Verdana", 14, "bold"), bg=co8).pack(pady=10)

    form_frame = Frame(frameAdicionar, bg=co8)
    form_frame.pack(pady=10)

    labels = ["ID Pessoa", "Objetivo", "Valor", "Data Recebida", "Data Entrega"]
    entries = {}

    for i, label in enumerate(labels):
        lbl = Label(form_frame, text=label + ":", font=("Verdana", 10), bg=co8)
        lbl.grid(row=i, column=0, sticky="e", pady=5, padx=5)
        ent = Entry(form_frame, width=30)
        ent.grid(row=i, column=1, pady=5, padx=5)
        entries[label] = ent

    def adicionarTarefa():
        try:
            idPessoa = int(entries["ID Pessoa"].get().strip())
            objetivo = entries["Objetivo"].get().strip()
            valor = float(entries["Valor"].get().strip())
            data_recebida = entries["Data Recebida"].get().strip()
            data_entregue = entries["Data Entrega"].get().strip()
        except ValueError:
            messagebox.showerror("Erro", "Certifique-se de preencher ID e Valor corretamente.")
            return

        if not all([idPessoa, objetivo, valor, data_recebida, data_entregue]):
            messagebox.showwarning("Campos vazios", "Por favor, preencha todos os campos.")
            return

        tarefa = (idPessoa, objetivo, valor, data_recebida, data_entregue, "ativo")
        resposta = messagebox.askyesno("Confirmar Adição", f"Deseja adicionar a tarefa:\n\n{tarefa}")
        if resposta:
            inserirReceita(tarefa)
            messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")
            for entrada in entries.values():
                entrada.delete(0, END)
            carregar_tarefas()

    btn_frame = Frame(frameAdicionar, bg=co8)
    btn_frame.pack(pady=10)

    Button(btn_frame, text="Adicionar Tarefa", command=adicionarTarefa,
           font=("Verdana", 10), bg="#4CAF50", fg="white", padx=10).pack()

    # SEGUNDA ABA - SERVIÇOS ATIVOS
    notebook.add(frameAtivos, text="Serviços Ativos")

    colunas = ["id", "nome", "objetivo", "valor", "data_recebida", "data_entregue"]
    tabelaAtivos = ttk.Treeview(frameAtivos, columns=colunas, show="headings")
    tabelaAtivos.pack(fill=BOTH, expand=True, padx=10, pady=10)

    for col in colunas:
        tabelaAtivos.heading(col, text=col.upper())
        tabelaAtivos.column(col, anchor="center", width=120 if col != "id" else 40)

    # TERCEIRA ABA - SERVIÇOS FINALIZADOS
    notebook.add(frameFinalizados, text="Serviços Finalizados")

    tabelaFinalizados = ttk.Treeview(frameFinalizados, columns=colunas, show="headings")
    tabelaFinalizados.pack(fill=BOTH, expand=True, padx=10, pady=10)

    for col in colunas:
        tabelaFinalizados.heading(col, text=col.upper())
        tabelaFinalizados.column(col, anchor="center", width=120 if col != "id" else 40)

    # DIV BAIXO
    divBaixo = Frame(janelaGestao, height=40, background=co6)
    divBaixo.pack(side=BOTTOM, fill=X)
    Label(divBaixo, text="© 2025 Frank Kiess - Todos os direitos reservados",
          bg=co6, fg=co1, font=("Verdana", 10)).pack(side=RIGHT, padx=10, pady=10)

    carregar_tarefas()
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

#TELA UTILIZADA NO LOGIN
loginJanela = Tk()
loginJanela.title("Login")
loginJanela.geometry("300x180")
loginJanela.eval('tk::PlaceWindow %s center' % loginJanela.winfo_pathname(loginJanela.winfo_id()))
loginJanela.configure(bg=co0)
loginJanela.resizable(FALSE, FALSE)

Label(loginJanela, text="Usuário:", bg=co0, fg=co1).pack(pady=5)
entradaUsuario = Entry(loginJanela)
entradaUsuario.pack()

Label(loginJanela, text="Senha:", bg=co0, fg=co1).pack(pady=5)
entradaSenha = Entry(loginJanela, show="*")
entradaSenha.pack()

aviso = Label(loginJanela, text="", bg=co0, fg="red")
aviso.pack()

ttk.Button(loginJanela, text="Entrar", command=verificarLogin).pack(pady=10)

loginJanela.mainloop()