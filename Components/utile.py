import tkinter as tk
from tkinter import *
import mysql.connector as sql

#--------- fomction deplacement -----


def centre_fenetre(window,a,b):
    x_Left = int(window.winfo_screenwidth()/2 -a/2)
    y_Top = int(window.winfo_screenheight()/2 -b/2)
    window.geometry("{}x{}+{}+{}".format(a,b,x_Left, y_Top))

def title_bar(main,largeur,couleur):
    #-------title bar ---------
    def deplacement(e):
        main.geometry(f'+{e.x_root}+{e.y_root}')
    def quitter(e):
        main.quit()
    bar_titre=tk.Frame(main, bg="black",width=30)
    bar_titre.pack(expand=1,fill=X)
    bar_titre.place(x=0,y=0,width=largeur)
    bar_titre.bind("<B1-Motion>",deplacement)
    #------- close button ------
    quit_label=tk.Label(bar_titre,text="X",bg=couleur,fg="White",font=("Helvetica, 13"))
    quit_label.pack(side=RIGHT)
    quit_label.bind("<Button-1>",quitter)
    
    #------ connexion base de donnees
