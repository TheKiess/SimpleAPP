from tkinter import *
from tkinter import Tk, ttk
from PIL import Image, ImageTk

################# cores ###############
co0 = "#2e2d2b"  # Preta
co1 = "#feffff"  # branca
co2 = "#4fa882"  # verde
co3 = "#38576b"  # valor
co4 = "#403d3d"   # letra
co5 = "#e06636"   # - profit
co6 = "#038cfc"   # azul
co7 = "#3fbfb9"   # verde
co8 = "#263238"   # + verde
co9 = "#e9edf5"   # + verde

colors = ['#5588bb', '#66bbbb','#99bb55', '#ee9944', '#444466', '#bb5555']

janela = Tk()
janela.title("Mari Pontinhos de Amor")
janela.geometry("900x650")
janela.configure(background="#2e2d2b")
janela.resizable(width=FALSE, height=FALSE)

style= ttk.Style(janela)
style.theme_use("clam")

# Frames (div) de telas
divCima = Frame(janela, width=1040, height=80, background=co6, relief="flat")
divCima.grid(row=0, column=0)

appImg = Image.open('Images/icone.jpg')
appImg = appImg.resize((250, 70))
appImg = ImageTk.PhotoImage(appImg)

appLogo = Label(divCima, image=appImg, text="Sistema de gestão", compound=LEFT, background=co6, fg=co1, anchor=NW, relief="raised", font=("Verdana 20"))
appLogo.place(x=2, y=2)

divMeio = Frame(janela, width=1040, height=320, background=co8, pady=20, relief="raised")
divMeio.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

divBaixo = Frame(janela, width=1040, height=300, background=co8, pady=20, relief="flat")
divBaixo.grid(row=2, column=0, pady=0, padx=10, sticky=NSEW)

janela.mainloop()