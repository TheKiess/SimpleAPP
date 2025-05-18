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
co7 = "#3fbfb9"  # verde
co8 = "#263238"  # + verde
co9 = "#e9edf5"  # + verde



################# TELA INICIAL APÓS LOGIN ###############

def abrir_janela_principal():
    loginJanela.destroy()

    janela = Tk()
    janela.title("Mari Pontinhos de Amor")
    janela.geometry("900x650")
    janela.configure(background=co0)
    janela.resizable(width=FALSE, height=FALSE)

    style = ttk.Style(janela)
    style.theme_use("clam")

    # DIV CIMA
    divCima = Frame(janela, width=900, height=80, background=co6, relief="flat")
    divCima.grid(row=0, column=0, sticky="nsew")

    appImg = Image.open('Images/icone.jpg')
    appImg = appImg.resize((250, 70))
    appImg = ImageTk.PhotoImage(appImg)

    appLogo = Label(divCima, image=appImg, text="  Sistema de gestão", compound=LEFT,
                    background=co6, fg=co1, anchor=NW, font=("Verdana", 20))
    appLogo.image = appImg
    appLogo.place(x=10, y=5)

    topoBotoes = Frame(divCima, background=co6)
    topoBotoes.place(x=550, y=25)

    ttk.Button(topoBotoes, text="GESTÃO").grid(row=0, column=0, padx=5)
    ttk.Button(topoBotoes, text="PESSOAS").grid(row=0, column=1, padx=5)
    ttk.Button(topoBotoes, text="VALORES").grid(row=0, column=2, padx=5)

    # DIV MEIO
    divMeio = Frame(janela, width=900, height=460, background=co8, relief="flat")
    divMeio.grid(row=1, column=0, padx=10, sticky="nsew")

    frameCalendario = Frame(divMeio, background=co0, bd=2, relief="solid")
    frameCalendario.grid(row=0, column=0, padx=20, pady=30, sticky=N)
    frameCalendario.grid_propagate(False)

    hoje = datetime.date.today()
    calendario = Calendar(frameCalendario, selectmode='day', year=hoje.year, month=hoje.month, day=hoje.day,
                          background=co6, disabledbackground='white',
                          bordercolor=co0, headersbackground=co6,
                          normalbackground='white', foreground=co0, headersforeground=co0,
                          font=("Verdana", 14), headersfont=("Verdana", 12),
                          selectforeground="white", selectbackground=co5)
    calendario.pack(padx=10, pady=10, expand=True, fill="both")

    #TABELA
    frameTabela = Frame(divMeio, background=co8)
    frameTabela.grid(row=0, column=1, padx=20, pady=30, sticky=N)
    colunas = ["nome", "entrega","valor"]
    tabela = ttk.Treeview(frameTabela, columns=colunas, show="headings", height=12)

    tabela.heading("nome", text="Nome da Pessoa")
    tabela.heading("entrega", text="Data de Entrega")
    tabela.heading("valor", text="Valor")

    tabela.column("nome", width=150)
    tabela.column("entrega", width=100)
    tabela.column("valor", width=75)

    tabela.grid_propagate(False)

    # Ficou estranho, mas dá para entender...
    dadosExemplo = [
        ["Maria da Costura", "20/05/2025", 80.00],
        ["Joana Linha", "22/05/2025", 65.50],
        ["Ana Agulha", "25/05/2025", 77.00]
    ]
    for dado in dadosExemplo:
        tabela.insert("", "end", values=dado)
        nome, data_str, valor = dado
        dia, mes, ano = map(int, data_str.split("/"))
        data = datetime.date(ano, mes, dia)
        calendario.calevent_create(data, f"{nome}", "entrega")
    calendario.tag_config("entrega", foreground="red")
    tabela.pack()

    # DIV BAIXO
    divBaixo = Frame(janela, width=900, height=50, background=co6, relief="flat")
    divBaixo.grid(row=2, column=0, pady=0, padx=10, sticky="nsew")

    copyright_label = Label(divBaixo, text="© 2025 Frank Kiess - Todos os direitos reservados",
                            bg=co6, fg=co1, font=("Verdana", 10))
    copyright_label.pack(side=RIGHT, padx=10, pady=10)

    janela.mainloop()




################# SISTEMA DE LOGIN DO APLICATIVO ###############
def verificar_login():
    usuario = entradaUsuario.get()
    senha = entradaSenha.get()

    # Simples verificação (substituir com validação real)
    if usuario == "admin" and senha == "admin":
        abrir_janela_principal()
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

ttk.Button(loginJanela, text="Entrar", command=verificar_login).pack(pady=10)

loginJanela.mainloop()