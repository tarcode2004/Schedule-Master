from datetime import date
from gc import callbacks
from re import MULTILINE
import backend
from xmlrpc.client import DateTime
from kivymd.app import MDApp
# Resize the window
from kivy.core.window import Window
from backend import *
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextFieldRect, MDTextFieldRound, MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.list import OneLineRightIconListItem, TwoLineAvatarIconListItem
from kivymd.uix.list import IconRightWidget
from kivymd.uix.picker import MDDatePicker
from functools import partial
from datetime import datetime

Window.size = (420, 780)
class MainApp(MDApp):
    user_idToken = ""
    local_id = ""
    goal_cards = 0
    dateholder = ""


    def addcard(self, panel, title, motiv, datex, tasklist, taskwidget):        
        list = (datex.text.split('/')) 
        var = date(int(list[2]), int(list[0]), int(list[1]))
        #Card Widget
        base = TwoLineAvatarIconListItem()
        word = MDLabel()
        word.padding = 20, 20
        word.text = title.text
        word.text_size = "40dp"
        word.theme_text_color = 'Custom'
        word.text_color = 0.6, 0.3, 0.9, 1
        ico = IconRightWidget()
        ico.icon = "progress-clock"
        base.md_bg_color = 1,1,1,1
        base.size = "100dp", "100dp"
        base.valign = 'center'
        base.on_release = partial(self.display_goal, title, motiv, var.strftime('%B %d, %Y'), tasklist)
        self.root.current = 'goals'
        base.add_widget(word)
        base.add_widget(ico)                 
        self.root.ids.goalpanel.add_widget(base)
        for i in (tasklist.text.split(',')):
            self.newtask(i, taskwidget)

    def printsht(self):
        print("fuiyoh")
    
    def addentry(self, target, title, text):
        base = TwoLineAvatarIconListItem()
        base.text = str(title.text)
        base.on_release = partial(self.display_entry, title, text)
        target.add_widget(base)
        self.root.current = 'journal'

    def display_entry(self, titlex, textx):
            popup = MDDialog(title = titlex.text, text = textx.text, auto_dismiss = True, overlay_color=(0.6, 0.3, 0.9, 1), buttons = [MDFlatButton(text="Close"), MDFlatButton(text = "Delete")])
            popup.open()

    def newtask(self, title, taskwidget):
        base = TwoLineAvatarIconListItem()
        base.text = title
        ico = IconRightWidget()
        ico.icon = "cog"
        ico.on_release = partial(self.printsht)
        base.on_release = partial(self.printsht)
        base.md_bg_color = 1,1,1,1
        base.size = "100dp", "100dp"
        base.valign = 'center'
        base.add_widget(ico)         
        #self.root.ids.taskmdlist.add_widget(base)
        taskwidget.add_widget(base)

    def addtxtfield(self, ref, txt):
        base = MDTextField()
        base.hint_text = txt
        base.hint_text_mode = 'persistent'
        base.mode = 'fill'

    def display_goal(self, titlex, motiv, datex, tasklist):
        popup = MDDialog(title = str(titlex.text), 
                        text = "Motivation: "+str(motiv.text)+"\nCompletion Date: "+str(datex)+ "\nTasks: "+str(tasklist.text),
                        auto_dismiss = True, overlay_color=(0.6, 0.3, 0.9, 1), 
                        buttons = [MDFlatButton(text = "Delete"), MDFlatButton(text="Close"), MDFlatButton(text= "Complete")])
        popup.open()   

    def goal_cal(self):
        picker = MDDatePicker()
        picker.open()

    def display_user_tokens(self):
        Tarik = User(self.local_id)# Create User
        Tarik.AddGoal("Get Buff", None)
        Tarik.AddTask("Go to the Gym", "Get Buff")
        Tarik.Push()
        self.root.ids.the_label.text = "local_id: " + self.local_id + "\n user_idToken: " + self.user_idToken
        #Tarik.Get(MainApp.user_idToken)

    def sign_out(self):
        self.root.ids.firebase_login_screen.log_out()
        self.root.current = 'firebase_login_screen'              
        

MainApp().run()

