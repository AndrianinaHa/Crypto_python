from logging import currentframe
from tkinter import *
from tkinter.font import Font
from PIL import ImageTk
from ttkbootstrap import Style
from tkinter import ttk
from utile import *
from tkcalendar import DateEntry
import mysql.connector as sql
from tkinter import messagebox

#----- Database connection -------
    
def register():
    db = sql.connect(host = "localhost", user = "root", passwd = "I001#?fff0066",database = "user")

    cur = db.cursor()
    nom= txt_nom.get()
    prenom=txt_prenom.get()
    mail= txt_mail.get()
    mdp= txt_npsswd.get()
    dateN= txt_date.get_date()
    mpd2= txt_cnpsswd.get()

    if nom=="" or prenom=="" or mail=="" or mdp=="" or dateN=="":
        messagebox.showerror("Error","All field are mandatory")
    else :
        cur.execute("INSERT INTO `personne` (`id`, `nom`, `prenom`, `email`, `dateN`, `mdp`) VALUES (NULL, '%s', '%s', '%s', '%s', '%s');" % (nom, prenom,mail,dateN,mdp))
        db.commit()
        db.close()
        messagebox.showinfo('success','successfully inserted') #if value is inserted ,it will give the message.

    cur.close()

# ------ -------------------------


def Login(main):
    main.destroy()
    global txt_nom
    global txt_prenom
    global txt_mail
    global txt_npsswd
    global txt_date
    global txt_cnpsswd
    global root
    style=Style(theme='flatly')
    root=style.master
    centre_fenetre(root,1100,600)
    root.overrideredirect(True)
    root.resizable(False,False)
        
        #--------- fomction deplacement -----
    def deplacement(e):
        root.geometry(f'+{e.x_root}+{e.y_root}')
    def quitter(e):
            root.quit()
    #---- Background image-----
    root.bg=PhotoImage(file="Components/images/002.png")
    bg_image=Label(root,image=root.bg).place(x=0,y=0,relwidth=1,relheight=1)
    #----- title bar ----------
    title_bar(root,1100,"#0C0C0C")
    #----- Form ---------------
    txt_nom=ttk.Entry(root,font=("Helvetica Neue",12),width=36,textvariable=StringVar())
    txt_nom.place(relx=0.65,rely=0.258)
    txt_prenom=ttk.Entry(root,font=("Helvetica Neue",12),width=36,textvariable=StringVar())
    txt_prenom.place(relx=0.65,rely=0.33)
    txt_mail=ttk.Entry(root,font=("Helvetica Neue",12),width=36,textvariable=StringVar())
    txt_mail.place(relx=0.65,rely=0.402)
    txt_date=DateEntry(root,font=("Helvetica Neue",12),width=34,textvariable=StringVar())
    txt_date.place(relx=0.65,rely=0.474)
    txt_npsswd=ttk.Entry(root,font=("Helvetica Neue",12),width=36,textvariable=StringVar(),show="*")
    txt_npsswd.place(relx=0.65,rely=0.546)
    txt_cnpsswd=ttk.Entry(root,font=("Helvetica Neue",12),width=36,textvariable=StringVar(),show="*")
    txt_cnpsswd.place(relx=0.65,rely=0.618)
    #------ Form Button ----------
    button_2 = ttk.Button(
    command=lambda:register(),
    style="secondary.Outline.TButton",
    text="Confirmer",
    width=18
    )
    style.configure('secondary.Outline.TButton',font=(None,14))
    button_2.place(
        relx=0.6,
        rely=0.83
    )
        