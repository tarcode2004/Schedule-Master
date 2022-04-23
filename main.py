from kivymd.app import MDApp
# Resize the window
from kivy.core.window import Window
import azureservies
from backend import *

Window.size = (350, 600)
class MainApp(MDApp):
    user_idToken = ""
    local_id = ""
    

    def display_user_tokens(self):
        Tarik = User(False, False, True, True)# Create User
        self.root.ids.the_label.text = "local_id: " + self.local_id + "\n user_idToken: " + self.user_idToken
        Tarik.getContacts(self.local_id)
        azureservies.default()

    def sign_out(self):
        self.root.ids.firebase_login_screen.log_out()
        self.root.current = 'firebase_login_screen'              
        

MainApp().run()