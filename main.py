from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

################# cores ###############
co0 = "#2e2d2b"  # background preto
co1 = "#feffff"  # branca
co2 = "#4fa882"  # verde
co3 = "#38576b"  # valor
co4 = "#403d3d"  # cores das letras
co5 = "#e06636"  # um Azul positivo
co6 = "#038cfc"  # azul
co7 = "#3fbfb9"  # verde
co8 = "#263238"  # + verde
co9 = "#e9edf5"  # + verde

#ESSA JANELA SERÁ APÓS USADA NO LOGIN
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
    divCima = Frame(janela, width=1040, height=80, background=co6, relief="flat")
    divCima.grid(row=0, column=0)
    appImg = Image.open('Images/icone.jpg')
    appImg = appImg.resize((250, 70))
    appImg = ImageTk.PhotoImage(appImg)
    appLogo = Label(divCima, image=appImg, text="Sistema de gestão", compound=LEFT, background=co6, fg=co1, anchor=NW, relief="raised", font=("Verdana 20"))
    appLogo.image = appImg  # manter referência
    appLogo.place(x=2, y=2)

    # DIV MEIO
    divMeio = Frame(janela, width=1040, height=320, background=co8, pady=20, relief="raised")
    divMeio.grid(row=1, column=0, pady=1, padx=10, sticky=NSEW)

    topoBotoes = Frame(divMeio, background=co8)
    topoBotoes.grid(row=0, column=0, columnspan=3)

    ttk.Button(topoBotoes, text="GESTÃO").grid(row=0, column=0, padx=10)
    ttk.Button(topoBotoes, text="PESSOAS").grid(row=0, column=1, padx=10)
    ttk.Button(topoBotoes, text="VALORES").grid(row=0, column=2, padx=10)

    # DIV BAIXO
    divBaixo = Frame(janela, width=1040, height=300, background=co8, pady=20, relief="flat")
    divBaixo.grid(row=2, column=0, pady=0, padx=10, sticky=NSEW)

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