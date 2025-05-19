from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
from PIL import Image, ImageTk
import datetime

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

    ttk.Button(topoBotoes, text="GESTÃO").grid(row=0, column=0, padx=5)
    ttk.Button(topoBotoes, text="PESSOAS", command=janelaPessoas).grid(row=0, column=1, padx=5)
    ttk.Button(topoBotoes, text="VALORES").grid(row=0, column=2, padx=5)

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

    #TABELA
    frameTabela = Frame(divMeio, background=co8, bd=2, relief="solid")
    frameTabela.grid(row=1, column=1, padx=20, pady=30, sticky=N)
    colunas = ["nome", "entrega","valor"]
    tabela = ttk.Treeview(frameTabela, columns=colunas, show="headings", height=12)

    tabela.heading("nome", text="Nome da Pessoa")
    tabela.heading("entrega", text="Data de Entrega")
    tabela.heading("valor", text="Valor")

    tabela.column("nome", width=150, anchor="center")
    tabela.column("entrega", width=100, anchor="center")
    tabela.column("valor", width=75, anchor="center")

    tabela.bind("<Button-1>", lambda e: "break" if tabela.identify_region(e.x, e.y) == "separator" else None)
    tabela.grid_propagate(False)


    # Ficou estranho, mas dá para entender...
    dadosExemplo = [
        ["Maria da Costura", "20/05/2025", "80.00 R$"],
        ["Joana Linha", "22/05/2025", "65.50 R$"],
        ["Ana Agulha", "25/05/2025", "77.00 R$"]
    ]
    for dado in dadosExemplo:
        tabela.insert("", "end", values=dado)
        nome, data_str, valor = dado
        dia, mes, ano = map(int, data_str.split("/"))
        data = datetime.date(ano, mes, dia)
        calendario.calevent_create(data, f"{nome}", "entrega")
    calendario.tag_config("entrega", foreground="white", background=co9)
    tabela.pack()

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
    def cadastrar():
        # TEMPORÁRIO
        entry_login_admin = {"login": "", "senha": ""}

        def abrir_login_admin():
            def salvar_login():
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

            Button(janelaLogin, text="Salvar", command=salvar_login).pack(pady=10)

        def salvar():
            nome = entry_nome.get()
            celular = entry_celular.get()
            tipo = tipoVar.get()

            if nome and celular and tipo:
                if tipo == "Administrador":
                    if not entry_login_admin.get("login") or not entry_login_admin.get("senha"):
                        mensagem.config(text="Preencha login e senha!")
                        return
                novoId = len(tabela.get_children()) + 1
                tabela.insert("", "end", values=[novoId, nome, celular, tipo])
                janelaCadastro.destroy()
            else:
                mensagem.config(text="Preencha todos os campos!")

        def on_tipo_selected(event):
            if tipoVar.get() == "Administrador":
                abrir_login_admin()

        # Tela principal
        janelaCadastro = Toplevel(janelaPessoas)
        janelaCadastro.title("Cadastrar Pessoa")
        janelaCadastro.geometry("300x300")
        janelaCadastro.configure(bg=co0)
        janelaCadastro.resizable(width=FALSE, height=FALSE)

        Label(janelaCadastro, text="Nome", bg=co0, fg=co1).pack(pady=(15, 0))
        entry_nome = Entry(janelaCadastro)
        entry_nome.pack()

        Label(janelaCadastro, text="Celular", bg=co0, fg=co1).pack(pady=(10, 0))
        entry_celular = Entry(janelaCadastro)
        entry_celular.pack()

        Label(janelaCadastro, text="Tipo", bg=co0, fg=co1).pack(pady=(10, 0))
        tipoVar = StringVar()
        combo_tipo = ttk.Combobox(janelaCadastro, textvariable=tipoVar, state="readonly")
        combo_tipo["values"] = ["Comprador", "Vendedor", "Ambos", "Administrador"]
        combo_tipo.pack()
        combo_tipo.bind("<<ComboboxSelected>>", on_tipo_selected)

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
                tabela.item(item, values=(valores[0], novoNome, novoCelular, novoTipo))
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
    
            Label(janelaEditar, text="Tipo", bg=co0, fg=co1).pack(pady=(10, 0))
            tipoVar = StringVar()
            comboboxTipo = ttk.Combobox(janelaEditar, textvariable=tipoVar, state="readonly")
            comboboxTipo["values"] = ["Comprador", "Vendedor", "Ambos"]
            comboboxTipo.set(valores[3])
            comboboxTipo.pack()
    
            Button(janelaEditar, text="Salvar", command=salvar_edicao).pack(pady=20)

    def excluir():
        item = tabela.selection()
        if item:
            tabela.delete(item)

    janelaPessoas = Toplevel()
    janelaPessoas.title("Cadastro de Pessoas")
    janelaPessoas.geometry("900x650")
    janelaPessoas.configure(background=co0)
    janelaPessoas.resizable(width=FALSE, height=FALSE)

    # DIV CIMA
    divCima = Frame(janelaPessoas, width=900, height=90, background=co6, relief="flat")
    divCima.grid(row=0, column=0, sticky="nsew")
    appImg = Image.open('Images/icone.jpg')
    appImg = appImg.resize((250, 70))
    appImg = ImageTk.PhotoImage(appImg)
    appLogo = Label(divCima, image=appImg, text="  Cadastros pessoais", compound=LEFT,
                    background=co6, fg=co1, anchor=NW, font=("Verdana", 20), relief="raised")
    appLogo.image = appImg
    appLogo.place(x=10, y=5)

    # DIV MEIO
    divMeio = Frame(janelaPessoas, width=900, height=460, background=co8, relief="flat")
    divMeio.grid(row=1, column=0, padx=10, sticky="nsew")

    titulo = Label(divMeio, text="Cadastro de Pessoas", font=("Verdana", 20, "bold"),
                   background=co8, foreground=co1)
    titulo.pack(pady=(10, 10))

    frameTabela = Frame(divMeio, background=co8, bd=2, relief="solid")
    frameTabela.pack(fill="x", padx=20)

    colunas = ["id", "nome", "celular", "tipo"]
    tabela = ttk.Treeview(frameTabela, columns=colunas, show="headings", height=12)

    for col in colunas:
        tabela.heading(col, text=col.capitalize())

    tabela.column("id", width=50, anchor="center")
    tabela.column("nome", width=300, anchor="center")
    tabela.column("celular", width=200, anchor="center")
    tabela.column("tipo", width=200, anchor="center")

    tabela.pack(fill="x")

    # TESTE ANTES
    dadosPessoas = [
        [1, "Maria Costura", "(47) 99999-0001", "Comprador"],
        [2, "João Linha", "(47) 98888-0002", "Vendedor"],
        [3, "Ana Agulha", "(47) 97777-0003", "Comprador"]
    ]

    for dado in dadosPessoas:
        tabela.insert("", "end", values=dado)

    frameBotoes = Frame(divMeio, background=co8)
    frameBotoes.pack(pady=10)
    ttk.Button(frameBotoes, text="Cadastrar", command=cadastrar).pack(side=LEFT, padx=10)
    ttk.Button(frameBotoes, text="Editar", command=editar).pack(side=LEFT, padx=10)
    ttk.Button(frameBotoes, text="Excluir", command=excluir).pack(side=LEFT, padx=10)

    # Rodapé
    divBaixo = Frame(janelaPessoas, width=900, height=40, background=co6, relief="flat")
    divBaixo.grid(row=2, column=0, padx=10, sticky="ew")

    copyright_label = Label(divBaixo, text="© 2025 Frank Kiess - Todos os direitos reservados",
                            bg=co6, fg=co1, font=("Verdana", 10))
    copyright_label.pack(side=RIGHT, padx=10, pady=10)



################# SISTEMA DE LOGIN DO APLICATIVO ###############
def verificarLogin():
    usuario = entradaUsuario.get()
    senha = entradaSenha.get()

    # Simples verificação (substituir com validação real)
    if usuario == "admin" and senha == "admin":
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