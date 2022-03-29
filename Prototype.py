from turtle import onclick, textinput
from types import ClassMethodDescriptorType
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.properties import StringProperty, BooleanProperty
Window.size = (900, 720)
class Login(Screen):
    bool = False
    msg = StringProperty("")
    Username = ""
    def Quit(self):
        exit()
    def Confirm(self, un, pw):
        if un in ["Christian", "Tarik", "Jhoan", "Cara"] and pw == "password":
            self.msg = "yeah boi"
            self.bool = True
            self.Username = un
            Menu.Username = un[0]
        else:
            self.msg = "Invalid Credentials" 
    def ActionII(self):
        pass
    def AddTask(self):
        pass
        
class Menu(Screen):
    TaskProg = 50
    Task = "Cardio"
    NTask = "Clean Room"
    Username = "Group 1"
    
    
class Tasks(Screen):
    pass
class Social(Screen):
    pass
class Mile_Stone(Screen):
    pass
class Control(ScreenManager):
    pass
    
kv = Builder.load_file('proto.kv')
class ProtoApp(App):
    def build(self):
        return(kv)

if __name__ == '__main__':
    ProtoApp().run()