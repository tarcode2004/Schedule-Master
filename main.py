from datetime import date
from datetime import datetime
from kivymd.app import MDApp
# Resize the window
from kivy.core.window import Window
import backend
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextFieldRect, MDTextFieldRound, MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.list import OneLineRightIconListItem, TwoLineAvatarIconListItem
from kivymd.uix.list import IconRightWidget
from kivymd.uix.pickers import MDTimePicker
from kivymd.uix.selectioncontrol import MDCheckbox
from functools import partial
from datetime import datetime
from backend import *
Window.size = (420, 720)

from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty, NumericProperty
class Command(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_size = 44


class Response(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_size = 44
    
class MainApp(MDApp):
    freq = 0
    user_idToken = ""
    local_id = ""
    task_day_list = []

    def newgoalobject(self, title, motiv, tasks, datex):
        task_list =[]
        strvar = ""
        #Ensure Date Format is correct
        try: 
            print(datex.text)    
            prevar = (datex.text.split('/')) 
            print(prevar)
            var = date(int(prevar[2]), int(prevar[0]), int(prevar[1]))
        except:
            print("Wrong Date Format")
            var = None
        #Create Tasks
        for i in (tasks.text.split(',')):
            strvar = strvar + i +", "
            new_task =  Task(i, None, title.text,var, [], Frequency(0), None)#d(name, description, goal, date, days, frequency, time):
            task_list.append(new_task)
        #Create Goal Object
        locals()[title.text]= Goal(title.text, motiv.text, var, task_list, strvar)
        #locals()[title.text].Tasks_str = tasks.text
        #Add Goal to Database Profile
        self.addcard(locals()[title.text])
        for i in task_list:
            self.addtaskcard(i)
       
    def addcard(self, goal):    
        base = TwoLineAvatarIconListItem()
        word = MDLabel()
        word.padding = 20, 20
        word.text = goal.Name
        word.font_size = "40dp"
        word.theme_text_color = "Custom"
        word.text_color = 0.6, 0.3, 0.9, 1
        ico = IconRightWidget()
        ico.icon = "progress-clock"
        base.md_bg_color = 1,1,1,1
        base.size = "100dp", "100dp"
        base.valign = 'center'
        base.on_release = partial(self.display_goal, goal)
        self.root.current = 'goals'
        base.add_widget(word)
        base.add_widget(ico)                 
        self.root.ids.goalpanel.add_widget(base)
        
    def printsht(self, item):
        print(item) 

    def newentry(self, target, title, text):
        locals()[title.text] = Journal_Entry(title, text, datetime.now())
        self.addjournalcard(locals()[title.text])
        #Append Journal to goals list

    def addjournalcard(self, journal_entry):
        if self.root.ids.children == []:
            base = TwoLineAvatarIconListItem()
            base.text = str()
            base.on_release = partial(self.display_entry, journal_entry.get_title, journal_entry.get_text())
            self.target.add_widget(base)
            self.root.current = 'journal'
    

    def display_entry(self, titlex, textx):
        popup = MDDialog(title = titlex, text = textx, auto_dismiss = True, overlay_color=(0.6, 0.3, 0.9, 1))
        popup.open()

    def display_task(self, task):
        popup = MDDialog(title = task.get_name(),text = "Description: "+str(task.get_description())+"\nGoal: "+str(task.get_goal())+"\nEnd Date: "+ str(task.get_date()),
        auto_dismiss = True, overlay_color=(0.6, 0.3, 0.9, 1))
        popup.open()
        
    def newtask(self, title, description, goal, frequency, timex):
        goal_ref = None
        #Check if goal enetred is valid
        for i in Goal_List:
            if goal == i.Name:
                goal_ref = i
                goal= goal_ref.Name
                datex = goal_ref.Date
        if goal_ref not in Goal_List:
            goal = None
            datex = ""

        #Check if time is valid
        try:
            pre_var = str(timex.text).split(':')
            print(pre_var)
            var = datetime.time(int(pre_var[0]),int(pre_var[1], 0 ))
        except:
            print("Invalid Time Format")
            pre_var = str(timex.text).split(':')
            print(pre_var)
            var = None
        locals()[title.text] = Task(title.text, description.text, goal, datex, self.task_day_list, Frequency(self.freq), timex)
        if goal_ref != None:
            goal_ref.add_task(locals()[title.text])
        self.addtaskcard(locals()[title.text])
        self.task_day_list = []
    
    def edit_task_call(self, task):
        self.root.ids.edit_Task_Title.text = task.get_name()
        self.root.ids.edit_task_goal = task.get_goal()
        self.root.current = "edit_task"
    #Edit existing Task Object
    def edit_task(self, task_ref, name, description, goal, frequency, timex):
        goal_ref = None
        task_ref = None
        #Check if goal enetred is valid
        for i in Goal_List:
            if goal == i.Name:
                goal_ref = i
                goal= goal_ref.Name
                datex = goal_ref.Date
                for i in (goal_ref.Tasks):
                    if task_ref == i.Name:
                        task_ref = i
                
        if goal_ref not in Goal_List:
            goal = None
            datex = ""

        #Check if time is valid
        try:
            pre_var = str(timex.text).split(':')
            print(pre_var)
            var = datetime.time(int(pre_var[0]),int(pre_var[1], 0 ))
        except:
            pre_var = timex.text.split(':')
            print(pre_var)
            print("Invalid Time Format")
            var = None
        task_ref.set_name(name.text)
        task_ref.set_description(description.text)
        task_ref.set_date(datex)
        task_ref.set_days(self.task_day_list)
        task_ref.set_frequency(Frequency(self.freq))
        task_ref.set_time(var) 
        self.task_day_list = []

    def addtaskcard(self, task):
        base = TwoLineAvatarIconListItem()
        base.text = task.Name
        ico = IconRightWidget()
        ico.icon = "cog"
        ico.on_release = partial(self.edit_task_call, task)
        base.on_release = partial(self.display_task, task)
        base.md_bg_color = 1,1,1,1
        base.size = "100dp", "100dp"
        base.valign = 'center'
        base.add_widget(ico)         
        self.root.ids.taskmdlist.add_widget(base)

    def addtxtfield(self, ref, txt):
        base = MDTextField()
        base.hint_text = txt
        base.hint_text_mode = 'persistent'
        base.mode = 'fill'

    def display_goal(self, goal):
        popup = MDDialog(title = goal.get_name(), 
                        text = "Motivation: "+str(goal.get_motivation())+"\nCompletion Date: "+str(goal.get_date())+ "\nTasks: "+str(goal.get_tasks_str()),
                        auto_dismiss = True, overlay_color=(0.6, 0.3, 0.9, 1))
        popup.open()   
   

   #Determine if task should repeated on a day
    def days_task(self, target, val):
        self.freq = val
        if self.root.ids.frequency_options.children == []and target == self.root.ids.frequency_options:
            print(self.root.ids.frequency_options.children)
            for i in ("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"):
                base = MDCard(orientation = 'vertical', md_bg_color = (0.9,0.9, 0.95, 1))
                text = MDLabel(text = i, theme_text_color= "Custom",
                                text_color= (0.6, 0.3, 0.9, 1) )
                check = MDCheckbox()
                check.on_press = partial(self.task_days, i, check.state)
                base.add_widget(text)
                base.add_widget(check)
                target.add_widget(base)
        elif self.root.ids.frequency_options.children == [] and target == self.root.ids.edit_frequency_options:
            for i in ("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"):
                base = MDCard(orientation = 'vertical', md_bg_color = (0.9,0.9, 0.95, 1))
                text = MDLabel(text = i, theme_text_color= "Custom",
                                text_color= (0.6, 0.3, 0.9, 1) )
                check = MDCheckbox()
                check.on_press = partial(self.task_days, i, check.state)
                base.add_widget(text)
                base.add_widget(check)
                target.add_widget(base)
    def task_days(self, item, val):
        print(val)
        if item not in self.task_day_list:
            if val == 'normal':
                self.task_day_list.append(item)
                print(self.task_day_list)
        elif item in self.task_day_list:
            self.task_day_list.remove(item)
            print(self.task_day_list)
            
    def display_user_tokens(self):
        Tarik = User(False, False, True, True)# Create User
        self.root.ids.the_label.text = "local_id: " + self.local_id + "\n user_idToken: " + self.user_idToken
        #Tarik.Get(MainApp.user_idToken)

    def sign_out(self):
        self.root.ids.firebase_login_screen.log_out()
        self.root.current = 'firebase_login_screen'              
        

MainApp().run()

