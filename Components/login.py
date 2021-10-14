import tkinter as tk
from tkinter import *
from tkinter.font import names
from tkinter.messagebox import showinfo
from PIL import ImageTk
from PIL import Image, ImageFilter
from ttkbootstrap import Style
from tkinter import ttk
from register import Login
from utile import *
from main import main_soft
    
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
    db = sql.connect(host = "localhost", user = "root", passwd = "I001#?fff0066",database = "user")

    cur = db.cursor()
    user = txt_user.get()
    passwd = txt_psswd.get()
    if(user == "" or passwd == ""):
            showinfo("Oops!","Your information can't be empty!")
            
    cur.execute("select nom,mdp from personne where nom = '%s' and mdp = '%s'" % (user, passwd))
    result = cur.fetchall()
    if result:
        showinfo("Success","You're logged in!")
        main_soft(main)
    else:
        showinfo("Failed","You've entered wrong credentials!")
            
    cur.close()

    db.close()

def register_form():
    global txt_user
    global txt_psswd
    global main
    splash.destroy()
    #------ initialisation -------
    style=Style(theme='solar')
    main=style.master
    main.overrideredirect(True)
    
    
    #------ window  ----------
    centre_fenetre(main,600,600)
    main.resizable(False,False)
    #------- Image Fond --------------
    main.bg=ImageTk.PhotoImage(file="Components/images/1506.png")
    main.bg_image=Label(main,image=main.bg).place(x=0,y=0,relwidth=1,relheight=1)
    
    #--------- title bar ------
    title_bar(main,600,"black")
    #---- entree ---
    txt_user=ttk.Entry(main,font=("Helvetica Neue",12),width=28,textvariable=StringVar())
    txt_user.place(relx=0.32,rely=0.413)
    txt_psswd=ttk.Entry(main,font=("Helvetica Neue",12),width=28,textvariable=StringVar(),show="*")
    txt_psswd.place(relx=0.32,rely=0.524)
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
    forgot_btn=ttk.Button(main,command=lambda:Login(main),text="Mot de passe oublié?",style='success.TButton',width=18).place(relx=0.51,rely=0.64)



splash.after(3000,register_form)
mainloop()