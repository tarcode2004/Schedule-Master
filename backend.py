import uuid
import json
import requests
import datetime
from enum import Enum

class ContactStatus(Enum):
    Request_Sent = 0
    Request_Recieved = 1
    Established = 2

class Contact:
    ID = ""
    Status = ContactStatus(0)

class Connection:
    InstantiatorID = ""
    Instantiator = True
    RecipientID = ""
    Recipient = False

class Frequency(Enum):
    Never = 0
    Day = 1
    Week = 2
    Month = 3
    Year = 4

class Alert(Enum):
    No = 0
    Notification = 1
    Alarm = 2

class Verification(Enum):
    No = 0 # don't ask for verification
    Gym = 1 # detect gym using camera
    Book = 2 # detect book using camera
    Ball = 3 # detect ball using camera

class Task: 
    ID = ""
    Name = ""
    Description = ""
    Date = ""
    Frequency = Frequency(0) # Never, Days, Weeks, Months
    Days=[]
    Time = ""
    Goal_Name = ""
    Alert = Alert(1)# Indicated type of Alert
    Vertification = Verification(0)
    SubTasks = []
class Journal_Entry():
    Title= ""
    Content=""
    RecordTime =""
    def __init__ (self, Title, Content, RecordTime):
        self.Title = Title
        self.Content = Content
        self.RecordTime = RecordTime
    def get_title(self):
        return (self.Title)
    def get_text(self):
        return(self.Content)
    def get_time(self):
        return(self.RecordTime)
    def set_title(self, val):
        self.Title = val
    def add_text(self, val):
        self.Content += val
    def set_time(self, val):
        self.Content = val

    def __init__(self, name, description, goal, date, days, frequency, time):
        self.ID = uuid.uuid4()
        self.Name = name
        self.Goal_Name = goal # Have list of Upper Goals
        self.Description = description
        self.Date = date
        self.days = days
        self.Frequency = frequency
        self.Time = str(time)
    def get_name(self):
        return self.Name
    def get_description(self):
        return self.Description
    def get_goal(self):
        return self.Goal_Name
    def get_date(self):
        return(self.Date)
    def get_days(self):
        return(self.Days)
    def get_frequency(self):
        return(self.Frequency)
    def get_times(self):
        return(self.Time)
    
    #Mutators
    def set_name(self, val):
        self.Name = val
    def set_description(self, val):
        self.Description = val
    def set_goal(self, val):
        self.Goal_Name = val
    def set_date(self, val):
        self.Date = val
    def set_days(self, val):
        self.Days = val
    def set_frequency(self, val):
        self.Frequency = val
    def set_times(self, val):
        self.Time = val
    

class Goal:
    ID = ""
    Name = ""
    Motivation = ""
    Tasks = [] # Tasks related to Goal
    Journal = [] # Journal tracking progress toward goal
    MentorList = [] # Mentors who have access to this goal
    PeerList = [] # Peers who share this list
    Date = ""
    Tasks_str= ""    
    def PrintID(self):
        print(self.ID)

    def __init__(self, name, motiv, deadline, tasks, tasks_str):
        self.ID = uuid.uuid4()
        self.Name = name
        self.Motivation = motiv
        self.Date = str(deadline)
        self.Tasks.append(tasks)
        self.Tasks_str = tasks_str
    def add_task(self, task):
        self.Tasks.append(task)
    def get_tasks_str(self):
        self.Tasks_str
    def get_tasks(self):
        return(self.Tasks)
    def get_motivation(self):
        return(self.Motivation)
    def get_date(self):
        return(self.Date)
    def get_name(self):
        return(self.Name)
    def add_task(self, task):
        self.Tasks.append(task)
        



class User:
    #Basics
    UID = ""
    Username = ""
    ProfilePic_ID = 1
    Bio = ""
    GoalList = []
    ContactList = []

    def PrintGoals(self):
        for x in range(len(self.GoalList)):
            if self.GoalList[x].UpperGoals == None :
                print(self.GoalList[x].Name, " : ", end="")
                self.GoalList[x].PrintID()
            else:
                print("\t", self.GoalList[x].Name, " : ", end="")
                self.GoalList[x].PrintID()

    def AddGoal(self, Name, UG):
        self.GoalList.append(Goal(Name, UG))

    def __init__(self, A, B, C, D):
        UID = uuid.uuid4()
        """
        Pass 4 boolean variables to set top level motivations / goals
        first for being a better person
        second for maintaining relationships
        third for a job or providing value to society
        fourth for health
        """
        if A:
            Good = Goal("Be Good", None, None, None, None)
            self.GoalList.append(Good)
        if B:
            Relationships = Goal("Maintain Relationships", None, None, None, None)
            self.GoalList.append(Relationships)
        if C:
            Job = Goal("Provide Value to Society", None, None, None, None)
            self.GoalList.append(Job)
        if D:
            Health = Goal("Be Healthy", None, None, None, None)
            self.GoalList.append(Health)
        
    def getContacts(self, local_id):
        result = requests.get("https://masterschedule-be192-default-rtdb.firebaseio.com/Connections.json")
        data = json.loads(result.content.decode())
        print(result.ok)
        #print(data['Christian and Luis']['IID'])
        #print("DATA IS", data) 



#Varaibles For Database
Goal_List = []