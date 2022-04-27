from kivymd.app import MDApp
# Resize the window
from kivy.core.window import Window
import azureservies
import bot
import backend

Window.size = (350, 600)
class MainApp(MDApp):
    user_idToken = ""
    local_id = ""
    

    def display_user_tokens(self):
        Tarik = backend.User(self.user_idToken)# Create User
        self.root.ids.the_label.text = "local_id: " + self.local_id + "\n user_idToken: " + self.user_idToken
        Goal = Tarik.AddGoal("Get Buff", None)
        Task = Tarik.AddTask("Go to the gym","Get Buff")
        bot.TaskStatus(Task)
        Tarik.FindTask(Tarik.FindGoal("Get Buff"), "Go to the gym")
        


    def sign_out(self):
        self.root.ids.firebase_login_screen.log_out()
        self.root.current = 'firebase_login_screen'              
        

MainApp().run()