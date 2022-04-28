import uuid
import json
import requests
import datetime
import time
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

class Goal:
    ID = ""
    Name = ""
    Motivation = ""
    UpperGoals = []
    SubGoals = [] 
    EndDate = ""
    Tasks = [] # Tasks related to Goal
    Journal = [] # Journal tracking progress toward goal
    MentorList = [] # Mentors who have access to this goal
    PeerList = [] # Peers who share this list

    def addSubGoal(self, id):
        self.SubGoals.append(id)
    
    def PrintID(self):
        print(self.ID)

    def __init__(self, name, UG):
        self.ID = uuid.uuid4()
        self.Name = name
        self.UpperGoals = UG # Have list of Upper Goals
        try:
            for G in UG:
                G.addSubGoal(self.ID)# Add itself as a subgoal to Upper Goals
        except:
            pass


class Task: 
    ID = ""
    Name = ""
    Description = ""
    Dates = []
    Frequency = Frequency(0) # Never, Days, Weeks, Months, Years repeat option
    Num = 0 # Number of days, weeks, months, or years to repeate
    Alert = Alert(1)# Indicated type of Alert
    Vertification = Verification(0)
    Goal

    def __init__(self, name, G):
        self.ID = uuid.uuid4()
        self.Name = name
        self.Goal = G # Have list of Upper Goals
        self.Goal.Tasks.append(self)


class JournalEntry:
    date = time
    Task
    Status = ""
    Note = ""
    Excuse = ""

    def __init__(self, *args):
        # if args are more than 1
        # sum of args
        if len(args) == 2:
            self.Task = args[0] # Task
            self.Status = args[1] # Status
  
        # if arg is an integer
        # square the arg
        elif len(args) == 3:
            self.Task = args[0]
            self.Status = args[1] # Status
            self.Note = args[2] # Note
  
        # if arg is string
        # Print with hello
        elif len(args) == 4:
            self.Task = args[0]
            self.Status = args[1] # Status
            self.Note = args[2] # Note
            self.Excuse = args[3] # Excuse
    

class User:
    #Basics
    UID = ""
    Username = ""
    ProfilePic_ID = 1
    Bio = ""
    GoalList = [Goal]
    ContactList = []

    def PrintGoals(self):
        for x in range(len(self.GoalList)):
            if self.GoalList[x].UpperGoals == None :
                print(self.GoalList[x].Name, " : ", end="")
                self.GoalList[x].PrintID()
            else:
                print("\t", self.GoalList[x].Name, " : ", end="")
                self.GoalList[x].PrintID()

    def FindGoal(self, string):
        for G in self.GoalList:
            if G.Name == string:
                return G

    def FindTask(self, goal, string):
        for T in goal.Tasks:
            if T.Name == string:
                return T
    
    def AddGoal(self, Name, UG):
        G = Goal(Name, UG)
        self.GoalList.append(G)
        return G

    def AddTask(self, Name, Goal):
        goal = self.FindGoal(Goal)
        goal.Tasks.append(Task(Name, goal))
        return self.FindTask(goal, Name)

    def Get(self, UserID):
        print(UserID)
        result = requests.get("https://masterschedule-be192-default-rtdb.firebaseio.com/"+UserID+".json")
        data = json.loads(result.content.decode())
        print(result.ok)
        print("DATA IS", data)
        #Assign to Data Structures

    def Push(self):
        user = '{"Bio": "", "Contact List": {"Christian": "", "Luis": ""}, "Goal List": {}, "Profile Pic": "", "UID": "", "name": "Bruh Metin"}'
        print(self.UID)
        result = requests.patch("https://masterschedule-be192-default-rtdb.firebaseio.com/" + self.UID + ".json", data=user)
        print("Status",result)

    def __init__(self,ID):
        self.UID = ID
        
    def getContacts(self, local_id):
        result = requests.get("https://masterschedule-be192-default-rtdb.firebaseio.com/Connections.json")
        data = json.loads(result.content.decode())
        print(result.ok)
        print(data['Christian and Luis']['IID'])
        #print("DATA IS", data) 
