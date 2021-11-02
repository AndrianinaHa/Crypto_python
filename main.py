from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.factory import Factory


KV='''
    MDScreen:

    MDCard:
        size_hint: None, None
        size: "180dp", "180dp"
        pos_hint: {"center_x": .5, "center_y": .8}
        radius: [100]
        FitImage:
            size_hint_y: 1
            source: "../assets/images/1.jpg"
            radius: [100]
            
    MDRoundFlatButton:
        text: "Se deconnecter"
        size_hint: .15,.06
        text_color: 0, 1, 0, 1
        pos_hint: {"center_x": .8, "center_y": .2}
        
    MDRoundFlatButton:
        text: "Preferences"
        size_hint: .15,.06
        text_color: 0, 1, 0, 1
        pos_hint: {"center_x": .8, "center_y": .3}
        
    MDBoxLayout:
        id: email
        orientation: "vertical"
        pos_hint: {"center_x": .505, "center_y": .55}
        
        MDLabel:
            text: "Haarena Andrianina"
            halign: "center"
            
        
    MDLabel:
        text: "Informations utilisateur"
        halign: "center"
        pos_hint: {"center_x": .2, "center_y": .5}
    MDLabel:
        text: "Nom"
        halign: "center"
        pos_hint: {"center_x": .1, "center_y": .4}
    MDLabel:
        text: "Prenom"
        halign: "center"
        pos_hint: {"center_x": .1, "center_y": .3}
    MDLabel:
        text: "E-mail"
        halign: "center"
        pos_hint: {"center_x": .1, "center_y": .2}
        
    '''


class Layout(Widget):
    pass


class ContentNavigationDrawer(MDBoxLayout):
    pass


class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "My Material Application"
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.root = Builder.load_file('assets/kv/main.kv')

    def rail_open(self):
        if self.root.ids.rail.rail_state == "open":
            self.root.ids.rail.rail_state = "close"
        else:
            self.root.ids.rail.rail_state = "open"


if __name__ == "__main__":
    MainApp().run()
