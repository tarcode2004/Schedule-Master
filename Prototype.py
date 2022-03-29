from turtle import onclick, textinput
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
Window.size = (900, 720)
class A(Screen):
    def Quit(self):
        exit()
    def ActionI(self):
        pass
    def ActionII(self):
        pass
    def AddTask(self):
        pass
        
class B(Screen):
    pass
class C(Screen):
    pass
class Control(ScreenManager):
    pass
kv = Builder.load_file('proto.kv')
class ProtoApp(App):
    def build(self):
        return(kv)

if __name__ == '__main__':
    ProtoApp().run()