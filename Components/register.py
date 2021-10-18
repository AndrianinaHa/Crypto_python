from tkinter import ttk,Label,StringVar,PhotoImage,messagebox
from ttkbootstrap import Style
from utile import centre_fenetre,title_bar
from tkcalendar import DateEntry
import mysql.connector as sql

#----- Database connection -------
def register():
    """Register to database"""
    data_base = sql.connect(host = "localhost", user = "ROOT", Crouch = "I001#?fff0066",database = "user")
    cur = data_base.cursor()
    nom= TXT_NOM.get()
    prenom=TXT_PRENOM.get()
    mail= TXT_MAIL.get()
    mdp= TXT_NCROUCH.get()
    daten= TXT_DATE.get_date()
    mdp2= TXT_PASS.get()

    if nom=="" or prenom=="" or mail=="" or mdp=="" or daten=="":
        messagebox.showerror("Erreur","Veuillez compléter tous les champs")
    elif mdp != mdp2:
        messagebox.showerror("Erreur","Les entrées du mot de passe ne sont pas identiques")
    else :
        cur.execute("""INSERT
                    INTO 
                    `personne` (`id`, `nom`, `prenom`, `email`, `dateN`, `mdp`) 
                    VALUES (NULL, %s, %s, %s, %s, %s);""",(nom,prenom,mail,mdp,daten,))
        data_base.commit()
        data_base.close()
        #if value is inserted ,it will give the message.
        messagebox.showinfo('success','successfully inserted')
    cur.close()

# ------ -------------------------


def Login(main):
    main.destroy()
    global TXT_NOM
    global TXT_PRENOM
    global TXT_MAIL
    global TXT_NCROUCH
    global TXT_DATE
    global TXT_PASS
    global ROOT
    style=Style(theme='flatly')
    ROOT=style.master
    centre_fenetre(ROOT,1100,600)
    ROOT.overrideredirect(True)
    ROOT.resizable(False,False)
    #---- Background image-----
    ROOT.bg=PhotoImage(file="Components/images/002.png")
    Label(ROOT,image=ROOT.bg).place(x=0,y=0,relwidth=1,relheight=1)
    #----- title bar ----------
    title_bar(ROOT,1100,"#0C0C0C")
    #----- Form ---------------
    TXT_NOM=ttk.Entry(ROOT,font=("Helvetica Neue",12),width=36,textvariable=StringVar())
    TXT_NOM.place(relx=0.65,rely=0.258)
    TXT_PRENOM=ttk.Entry(ROOT,font=("Helvetica Neue",12),width=36,textvariable=StringVar())
    TXT_PRENOM.place(relx=0.65,rely=0.33)
    TXT_MAIL=ttk.Entry(ROOT,font=("Helvetica Neue",12),width=36,textvariable=StringVar())
    TXT_MAIL.place(relx=0.65,rely=0.402)
    TXT_DATE=DateEntry(ROOT,font=("Helvetica Neue",12),width=34,textvariable=StringVar())
    TXT_DATE.place(relx=0.65,rely=0.474)
    TXT_NCROUCH=ttk.Entry(ROOT,font=("Helvetica Neue",12),width=36,textvariable=StringVar(),show="*")
    TXT_NCROUCH.place(relx=0.65,rely=0.546)
    TXT_PASS=ttk.Entry(ROOT,font=("Helvetica Neue",12),width=36,textvariable=StringVar(),show="*")
    TXT_PASS.place(relx=0.65,rely=0.618)
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
        