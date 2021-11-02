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
from kivymd.uix.list import IRightBodyTouch, ThreeLineAvatarIconListItem, IconLeftWidget
from kivy.properties import StringProperty
import mysql.connector
from cryptography.fernet import Fernet


class ListItem(ThreeLineAvatarIconListItem):
    """Custom list item."""
    icon = StringProperty("android")


class OptionApp(Screen):
    pass


class Profile(Screen):
    def confirmer(self):
        data_base = mysql.connector.connect(host="localhost", user="root", passwd="I001#?fff0066",
                                            database="users")
        c = data_base.cursor()
        nom = self.ids.user_name.text
        prenom = self.ids.user_prenom.text
        email = self.ids.mail.text
        id_personne = 1
        c.execute("INSERT INTO `personne` (`user_nom`,`user_prenom`, `user_email`) "
                  "VALUES (%s,%s,%s) "
                  " WHERE (SELECT * from personne where personne.id = %s)", (nom, prenom, email, id_personne))

    def on_pre_enter(self):
        data_base = mysql.connector.connect(host="localhost", user="root", passwd="I001#?fff0066",
                                            database="users")
        c = data_base.cursor()
        c.execute("select user_nom,user_prenom,user_email from personne where personne.id = 1")
        results = c.fetchone()
        if self.ids.user_name.hint_text == "":
            self.ids.user_name.hint_text = 'Nom'
        else:
            self.ids.user_name.hint_text = f'{results[0]}'
        if self.ids.user_prenom.hint_text == "":
            self.ids.user_prenom.hint_text = 'Prenom'
        else:
            self.ids.user_prenom.hint_text = f'{results[1]}'
        self.ids.email.text = f'{results[2]}'

        self.ids.mail.hint_text = f'{results[2]}'


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
        c.execute("select book_nom,book_genre,user_pseudo from book,personne where personne.id = book_author")
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

    data = {
        'Options': 'language-python',
        'Profile': 'language-php',
    }


class Navigation(ScreenManager):
    pass


class TestApp(MDApp):
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        self.screen = Builder.load_file('test.kv')

    def build(self):
        return self.screen

    def callback(self, instance):
        if instance.icon == 'language-python':
            self.screen.switch_to(OptionApp(name="options"), duration=.7)
        elif instance.icon == 'language-php':
            self.screen.switch_to(Profile(name="profile"), duration=.7)


if __name__ == "__main__":
    TestApp().run()
