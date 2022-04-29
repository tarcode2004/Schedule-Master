from datetime import date
from datetime import datetime
from kivymd.app import MDApp
from kivy.core.window import Window
import backend
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextFieldRect, MDTextFieldRound, MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.list import OneLineRightIconListItem, TwoLineAvatarIconListItem
from kivymd.uix.list import IconRightWidget
from kivymd.uix.picker import MDTimePicker
from kivymd.uix.selectioncontrol import MDCheckbox
from functools import partial
from datetime import *
from backend import *
Window.size = (420, 810)
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty, NumericProperty




from asyncio import Task
from setuptools import Command
import azureservies
import backend

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
    User = User(local_id)# Create User

    def newgoalobject(self, title, motiv, tasks, datex):
        task_list = []
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
            new_task = backend.Task(i, None, title.text,var, [], Frequency(0), None)#d(name, description, goal, date, days, frequency, time):
            task_list.append(new_task)
        #Create Goal Object
        G = backend.Goal(title.text, motiv.text, var, task_list, strvar)
        locals()[title.text] = G
        self.User.GoalList.append(G)
        Dict_Goal = {}
        Dict_Goal["Goal"] = str(G.get_name())
        #Dict_Goal["Tasks"] = task_list
        Dict_Goal["Motivation"] = motiv.text
        Dict_Goal["Complete by"] = str(var)
        Dict_Goal["Task_Names"] = strvar
        Dict_Goal["Journal"] = []
        data = json.dumps(Dict_Goal)
        result = requests.patch("https://masterschedule-be192-default-rtdb.firebaseio.com/" + self.local_id + "/Goals"+ ".json", data=data)
        print(result)


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

    def newentry(self, task, status = None, note = None, excuse = None ):
        locals()[str(datetime.now)] = JournalEntry(task, status, note, excuse)
        self.addjournalcard(locals()[str((datetime.now))])

    def addjournalcard(self, journal_entry):
        if  journal_entry != None:
            base = TwoLineAvatarIconListItem()
            base.text = str()
            base.on_release = partial(self.display_entry, journal_entry)
            #self.root.add_widget(base)
            #self.root.current = 'journal'    

    def display_entry(self, journal_entry):
        popup = MDDialog(title = str(journal_entry.get_task())+": "+str(datetime.now()), text = journal_entry.get_note+"\n"+journal_entry.get_excuse(), auto_dismiss = True, overlay_color=(0.6, 0.3, 0.9, 1))
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
        locals()[title.text] = backend.Task(title.text, description.text, goal, datex, self.task_day_list, Frequency(self.freq), timex)
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
        print(goal)
        #Check if goal enetred is valid
        for i in self.User.Goal_List:
            print(i)
            if name in i.get_tasks_str():
                for j in i.get_tasks():
                    goal_ref = i
                    goal = goal_ref.Name
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
        print(task_ref)
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
<<<<<<< Updated upstream
   
    def call_bot(self, *args):
        #Task = self.User.GoalList[0].Tasks[0]
        self.TaskStatus(Task)
        journal = "self.User.GoalList[0].Journal[0]"
        self.addjournalcard(journal)
=======
>>>>>>> Stashed changes

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
        self.root.ids.the_label.text = "local_id: " + self.local_id + "\n user_idToken: " + self.user_idToken

    def sign_out(self):
        self.root.ids.firebase_login_screen.log_out()
        self.root.current = 'firebase_login_screen'              


    def JournalNote(*args):
        azureservies.TTS("What do you have to say about this task?")
        Note = azureservies.STT()
        return Note

    def YN(string):
        azureservies.TTS(string)
        result = azureservies.YN()
        return result

    def TaskStatus(self, *args):
        #Goal = Task.Goal
        TaskName = "do a task?"
        Prompt = "did you " + TaskName
        self.root.ids.chats.add_widget(Response( 
            text = Prompt,
            size_hint_x= .50,
            halign = "center",))
        azureservies.TTS(Prompt)
        JI = backend.JournalEntry
        TaskStatus = azureservies.TSU()
        

        if TaskStatus == "Task Completed":
            
            status =  "Task Completed"
            
            self.root.ids.chats.add_widget(Command( 
            text = status,
            size_hint_x= .50,
            halign = "center",))
            
            azureservies.TTS("Would you like to save a note with this task?")
            
            tts = "Would you like to save a note with this task?"
            
            self.root.ids.chats.add_widget(Response( 
            text = tts,
            size_hint_x= .50,
            halign = "center",))
            
            result = azureservies.YN()
            
            
            if result == "yes":
                Note = self.JournalNote()
                print(str(Note))    
                result = azureservies.YN()
                JI  = backend.JournalEntry(Task, TaskStatus, Note)#new journal entry
                
                #Goal.Journal.append(
                #   JI
                #)
            else:
                JI  = backend.JournalEntry(Task, TaskStatus)#new journal entry
                #Goal.Journal.append(
                # JI
                #)

        elif TaskStatus == "Working on Task":
            
            status =  "Working on Task"
            
            self.root.ids.chats.add_widget(Command( 
            text = status,
            size_hint_x= .50,
            halign = "center",))
            
            azureservies.TTS("When will you be finished?")
            
            
            tts = "When will you be finished?"
            
            self.root.ids.chats.add_widget(Response( 
            text = tts,
            size_hint_x= .50,
            halign = "center",))
            
            
            Note = azureservies.STT()
            JI = backend.JournalEntry(Task, TaskStatus, None)#new journal entry
            #Goal.Journal.append(
            #   JI
            #)
            #Undersatnd time
            #Reschedule task for that time

        elif TaskStatus == "Partially Completed":
            
            status =  "Partially Completed"
            
            self.root.ids.chats.add_widget(Command( 
            text = status,
            size_hint_x= .50,
            halign = "center",))
            
            
            Note = self.JournalNote()
            JI = backend.JournalEntry(Task, TaskStatus, Note)#new journal entry
            #Goal.Journal.append(
            #   JI
        # )
        elif TaskStatus == "Did not complete":
            
            status =  "Did not complete"
            
            self.root.ids.chats.add_widget(Command( 
            text = status,
            size_hint_x= .50,
            halign = "center",))
            
            
            azureservies.TTS("Why didn't you complete the task?")
            
            
            tts = "Why didn't you complete the task?"
            
            self.root.ids.chats.add_widget(Response( 
            text = tts,
            size_hint_x= .50,
            halign = "center",))
            
            
            Excuse = azureservies.NCU()
            Note = self.JournalNote()
           
            self.root.ids.chats.add_widget(Command( 
            text = Excuse,
            size_hint_x= .50,
            halign = "center",))
            
            JI = backend.JournalEntry(Task, TaskStatus, Note, Excuse)#new journal entry
            #Goal.Journal.append(
                #JI
        # )
        elif TaskStatus == "None": 
            Note = self.JournalNote()
            self.root.ids.chats.add_widget(Command( 
            text = Note,
            size_hint_x= .50,
            halign = "center",))
            JI = backend.JournalEntry(Task, TaskStatus, Note)#new journal entry
        # Goal.Journal.append(
            #    JI
            #)

MainApp().run()

