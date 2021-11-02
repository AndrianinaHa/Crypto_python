from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.config import Config
from kivymd.uix.fitimage import FitImage
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.properties import ObjectProperty
from kivy.factory import Factory
from kivymd.uix.card import MDCard
from kivymd.uix.list import IRightBodyTouch, ThreeLineAvatarIconListItem, IconLeftWidget, ImageLeftWidget
from kivy.properties import StringProperty
import mysql.connector
from cryptography.fernet import Fernet
import io
from kivy.core.image import Image as CoreImage
from kivymd.uix.imagelist import SmartTile
from PIL import Image


class Login(Screen):
    pass


class Register(Screen):
    pass


class OptionApp(Screen):
    pass


class Livre(Screen):
    pass


class Profile(Screen):
    def confirmer(self):
        data_base = mysql.connector.connect(host="localhost", user="root", passwd="I001#?fff0066",
                                            database="users")
        c = data_base.cursor()
        nom = self.ids.user_name.text
        prenom = self.ids.user_prenom.text
        email = self.ids.mail.text
        pseudo = self.ids.email.text
        c.execute("INSERT INTO `personne` (`user_nom`,`user_prenom`, `user_email`) "
                  "VALUES (%s,%s,%s) "
                  " WHERE (SELECT * from personne where personne.user_pseudo = %s)", (nom, prenom, email, pseudo))
        data_base.commit()
        data_base.close()

    def on_pre_enter(self):
        data_base = mysql.connector.connect(host="localhost", user="root", passwd="I001#?fff0066",
                                            database="users")
        c = data_base.cursor()
        part = self.ids.email.text
        c.execute("select user_pseudo,user_nom,user_prenom,user_email,key_enc from personne")
        results = c.fetchall()
        for result in results:
            key = result[4].encode()
            print("hwy", len(key))
            fernet = Fernet(key)
            decuser = fernet.decrypt(result[0].encode()).decode()
            if result[1] != "":
                decnom = fernet.decrypt(result[1].encode()).decode()
            if result[2] != "":
                decprenom = fernet.decrypt(result[2].encode()).decode()
            decmail = fernet.decrypt(result[3].encode()).decode()
            if decuser == part:
                validation = True
                break
            else:
                validation = False
        if validation:
            self.ids.user_name.hint_text = f'{decnom}'
            self.ids.user_prenom.hint_text = f'{decprenom}'
            self.ids.mail.hint_text = f'{decmail}'
        else:
            if self.ids.user_name.hint_text == "":
                self.ids.user_name.hint_text = 'Nom'
            elif self.ids.user_prenom.hint_text == "":
                self.ids.user_prenom.hint_text = 'Prenom'

        data_base.commit()
        data_base.close()


class ListItem(ThreeLineAvatarIconListItem):
    """Custom list item."""
    icon = StringProperty("android")


class MainApp(Screen):

    def search_regular(self):
        self.ids.scroll.clear_widgets()
        data_base = mysql.connector.connect(host="localhost", user="root", passwd="I001#?fff0066",
                                            database="users")
        c = data_base.cursor()
        query = self.ids["cherche"].text
        c.execute("select book_nom,book_genre,user_pseudo from book,personne where book.book_nom = %s and personne.id "
                  "= book_author", (query,))
        result = c.fetchall()
        for liste in result:
            texte = f"Titre :\n{liste[0]}"
            stext = f"Genre :\n{liste[1]}"
            ttext = f"Auteur :\n{liste[2]}"
            icons = IconLeftWidget(icon="android")
            items = ListItem(text=texte, secondary_text=stext, tertiary_text=ttext)
            items.add_widget(icons)
            self.ids.scroll.add_widget(items)
        data_base.commit()
        data_base.close()

    def on_pre_enter(self):
        data_base = mysql.connector.connect(host="localhost", user="root", passwd="I001#?fff0066",
                                            database="users")
        c = data_base.cursor()
        c.execute("select book_nom,book_genre,user_pseudo,book_image from book,personne where personne.id = book_author")
        result = c.fetchall()
        for liste in result:
            with open(f"{liste[0]}.png", 'wb') as file:
                file.write(liste[3])
            icons = ImageLeftWidget(source=f"{liste[0]}.png", radius=[100])
            items = ListItem(text=f"Titre : {liste[0]}", secondary_text=f"Genre : {liste[1]}")
            items.add_widget(icons)
            self.ids.scroll.add_widget(items)
        data_base.commit()
        data_base.close()

    data = {
        'Options': 'language-python',
        'Profile': 'language-php',
    }


class Navigation(ScreenManager):
    pass


class Sign(MDApp):
    dialog = None

    def build(self):
        data_base = mysql.connector.connect(host="localhost", user="root", passwd="I001#?fff0066")
        c = data_base.cursor()
        # Creer une bd si elle n'existe pas
        c.execute("CREATE DATABASE IF NOT EXISTS users")
        # Creer table si elle n'existe pas
        c.execute("CREATE TABLE IF NOT EXISTS `users`.`personne` ( `id` INT UNSIGNED NOT NULL AUTO_INCREMENT , "
                  "`user_pseudo` VARCHAR( "
                  "255) NOT NULL , `user_nom` VARCHAR(255) NOT NULL, `user_prenom` VARCHAR(255) NOT NULL , "
                  "`user_email` VARCHAR(255) NOT NULL,`key_enc` VARCHAR(255) NOT NULL , `user_mdp` VARCHAR(255) "
                  "NOT NULL , PRIMARY KEY (`id`)) ;")
        # Verifie si elle existe
        c.execute("CREATE TABLE IF NOT EXISTS `users`.`book` ( `id_book` INT NOT NULL AUTO_INCREMENT , `book_nom` "
                  "VARCHAR(255) NOT NULL , `book_genre` VARCHAR(255) NOT NULL , `book_author` INT UNSIGNED NOT NULL , "
                  "`book_star` INT NOT NULL ,`book_image` LONGBLOB NOT NULL, "
                  "PRIMARY KEY (`id_book`), CONSTRAINT `fk_author` FOREIGN KEY (`book_author`) REFERENCES "
                  "`users`.`personne`( `id`) ON DELETE CASCADE ON UPDATE CASCADE);")
        data_base.commit()
        data_base.close()
        self.screen = Builder.load_file('../assets/kv/sign.kv')
        return self.screen

    def connecter(self):
        data_base = mysql.connector.connect(host="localhost", user="root", passwd="I001#?fff0066",
                                            database="users")
        c = data_base.cursor()
        user = self.screen.get_screen('login').ids.user_name.text
        mdp = self.screen.get_screen('login').ids.user_pass.text
        if user == "" or mdp == "":
            if not self.dialog:
                self.dialog = MDDialog(
                    title="Oops !",
                    text="Veuillez compléter ces champs",
                    buttons=[MDFlatButton(text='Close', on_release=self.close_dialog)]
                )
            self.dialog.open()
        else:
            # Creer une bd si elle n'existe pas
            c.execute("""SELECT 
                        id,key_enc,user_pseudo,user_mdp
                        from personne """)
            # Verifie si elle existe
            results = c.fetchall()
            validation = True
            for result in results:
                key = result[1].encode()
                fernet = Fernet(key)
                decuser = fernet.decrypt(result[2].encode()).decode()
                decmdp = fernet.decrypt(result[3].encode()).decode()
                if decuser == user and decmdp == mdp:
                    validation = True
                    break
                else:
                    validation = False
            if validation:
                if not self.dialog:
                    self.dialog = MDDialog(
                        title="Succès",
                        text="Bienvenue !"
                    )
                self.dialog.open()
                self.screen.switch_to(MainApp(name="principale"), transition=FadeTransition(), duration=.7)
                self.screen.get_screen('profile').ids.email.text = user
            else:
                if not self.dialog:
                    self.dialog = MDDialog(
                        title="Oops",
                        text="Le nom d'utilisateur ou le mot de passe est incorrecte ",
                        radius=[20, 7, 20, 7]
                    )
                self.dialog.open()
        data_base.commit()
        data_base.close()

    def enregistrer(self):
        data_base = mysql.connector.connect(host="localhost", user="root", passwd="I001#?fff0066",
                                            database="users")
        # variable pour obtenir les entrees utilisateurs
        user = self.screen.get_screen('register').ids.user_pseudo.text
        mail = self.screen.get_screen('register').ids.user_mail.text
        mdp = self.screen.get_screen('register').ids.user_crouch.text
        mdp1 = self.screen.get_screen('register').ids.user_crouch1.text
        # curseur base de donnees
        c = data_base.cursor()
        if user == "" or mail == "" or mdp == "" or mdp1 == "":
            if not self.dialog:
                self.dialog = MDDialog(
                    title="Oops",
                    text="Veuillez compléter ces champs",
                    radius=[20, 7, 20, 7],
                    buttons=[MDFlatButton(text='Close', on_release=self.dialog.dismiss())]
                )
            self.dialog.open()
        if mdp1 != mdp:
            if not self.dialog:
                self.dialog = MDDialog(
                    title="Oops",
                    text="Veuillez bien confirmer votre mot passe",
                    radius=[20, 7, 20, 7]
                )
            self.dialog.open()
        if not mdp.isalnum():
            if not self.dialog:
                self.dialog = MDDialog(
                    title="Oops",
                    text="Le mot de passe doit contenir des lettres et des chiffres",
                    radius=[20, 7, 20, 7]
                )
            self.dialog.open()
        if user == mdp or user == mdp1:
            if not self.dialog:
                self.dialog = MDDialog(
                    title="Oops",
                    text="Le mot de passe doit être différent du nom d'utilisateur",
                    radius=[20, 7, 20, 7]
                )
            self.dialog.open()
        if len(mail) < 15:
            if not self.dialog:
                self.dialog = MDDialog(
                    title="Oops",
                    text="Adresse e-mail incorrecte",
                    radius=[20, 7, 20, 7]
                )
            self.dialog.open()
        if mdp.capitalize() != mdp:
            if not self.dialog:
                self.dialog = MDDialog(
                    title="Oops",
                    text="Le mot de passe doit commencer avec une lettre en majuscule",
                    radius=[20, 7, 20, 7]
                )
            self.dialog.open()
        if len(mdp) < 8:
            if not self.dialog:
                self.dialog = MDDialog(
                    title="Oops",
                    text="Le mot de passe doit avoir au moins 8 caractères",
                    radius=[20, 7, 20, 7]
                )
            self.dialog.open()
        if len(user) < 4:
            if not self.dialog:
                self.dialog = MDDialog(
                    title="Oops",
                    text="Le nom doit avoir au moins 4 caractères",
                    radius=[20, 7, 20, 7]
                )
            self.dialog.open()
        else:
            # Creer une bd si elle n'existe pas
            key = Fernet.generate_key()
            fernet = Fernet(key)
            userenc = fernet.encrypt(user.encode())
            mailenc = fernet.encrypt(mail.encode())
            mdpenc = fernet.encrypt(mdp.encode())
            c.execute("INSERT INTO `personne` (`id`, `user_pseudo`,`user_nom`,`user_prenom`, `user_email`,`key_enc`,"
                      "`user_mdp`) VALUES (NULL,%s,'','',%s,%s,%s)", (userenc, mailenc, key, mdpenc,))
            # Verifie si elle existe
            if not self.dialog:
                self.dialog = MDDialog(
                    title="Succès",
                    text="Bienvenue",
                    radius=[20, 7, 20, 7]
                )
            self.dialog.open()
            self.screen.switch_to(MainApp(name="principale"), transition=FadeTransition(), duration=.7)
        data_base.commit()
        data_base.close()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def callback(self, instance):
        if instance.icon == 'language-python':
            self.screen.switch_to(OptionApp(name="options"), duration=.7)
        elif instance.icon == 'language-php':
            self.screen.switch_to(Profile(name="profile"), duration=.7)

    def lire(self):
        self.screen.switch_to(Livre(name="lire"), transition=FadeTransition(), duration=.7)
        #self.screen.get_screen('lire').ids.livret.text =


if __name__ == "__main__":
    Sign().run()
