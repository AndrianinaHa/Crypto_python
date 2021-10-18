import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import ttk,Tk,Label,StringVar,mainloop
from PIL import ImageTk
from ttkbootstrap import Style
from register import Login
from utile import centre_fenetre,title_bar
from main import main_soft
import mysql.connector as sql

splash=Tk()
#-------- Center window -------
centre_fenetre(splash,64,64)
#--------- window info --------
splash.title("Loading")
splash.overrideredirect(True)
splash.resizable(False,False)
#------- Chargement -----------
splash.image = tk.PhotoImage(file="Components/images/001.png")
loader = tk.Label(splash, bg='white')
loader.config(image=splash.image)
splash.wm_attributes("-topmost", True)
splash.wm_attributes("-disabled", True)
splash.wm_attributes("-transparentcolor", "white")
loader.pack()

def login():
    """Login side client"""
    data_base = sql.connect(host = "localhost", user = "root", passwd = "I001#?fff0066",database = "user")
    cur = data_base.cursor()
    user = TXT_USER.get()
    Crouch = TXT_CROUCH.get()
    if(user == "" or Crouch == ""):
        showinfo("Oops!","Your information can't be empty!")
    else :
        cur.execute("""select
                    nom,mdp 
                    from 
                    personne 
                    where 
                    nom = %s and mdp = %s """,(user,Crouch,))
    result = cur.fetchall()
    if result is None:
        return False
    if result:
        showinfo("Success","You're logged in!")
        main_soft(MAIN)
    else:
        showinfo("Failed","You've entered wrong credentials!")
            
    cur.close()

    data_base.close()

def register_form():
    """Register form"""
    global TXT_USER
    global TXT_CROUCH
    global MAIN
    splash.destroy()
    #------ initialisation -------
    style=Style(theme='solar')
    MAIN=style.master
    MAIN.overrideredirect(True)
    #------ window  ----------
    centre_fenetre(MAIN,600,600)
    MAIN.resizable(False,False)
    #------- Image Fond --------------
    MAIN.bg=ImageTk.PhotoImage(file="Components/images/1506.png")
    Label(MAIN,image=MAIN.bg).place(x=0,y=0,relwidth=1,relheight=1)
    #--------- title bar ------
    title_bar(MAIN,600,"black")
    #---- entree ---
    TXT_USER=ttk.Entry(MAIN,font=("Helvetica Neue",12),width=28,textvariable=StringVar())
    TXT_USER.place(relx=0.32,rely=0.413)
    TXT_CROUCH=ttk.Entry(MAIN,font=("Helvetica Neue",12),width=28,textvariable=StringVar(),show="*")
    TXT_CROUCH.place(relx=0.32,rely=0.524)
    #------- button --------
    button_1 = ttk.Button(
        command=lambda:login(),
        style="secondary.Outline.TButton",
        text="Confirmer",
        width=18
    )
    button_1.place(
        relx=0.24,
        rely=0.64
    )
    ttk.Button(MAIN,command=lambda:Login(MAIN),text="Mot de passe oublié?",style='success.TButton',width=18).place(relx=0.51,rely=0.64)



splash.after(3000,register_form)
mainloop()
