import uuid
import requests
import datetime
from enum import Enum

class ContactStatus(Enum):
    Request_Sent = 0
    Request_Recieved = 1
    Established = 2

class Contact:
    ID = ""
    Status = ContactStatus()

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
    Dates = [datetime.datetime(2022, 4, 5)]
    Frequency = Frequency(0) # Never, Days, Weeks, Months, Years repeat option
    Num = 0 # Number of days, weeks, months, or years to repeate
    Alert = Alert(1)# Indicated type of Alert
    Vertification = Verification(0)
    SubTasks = []

    def __init__(self, name, G):
        self.ID = uuid.uuid4()
        self.Name = name
        self.Goal = G # Have list of Upper Goals
        self.Goal.Tasks.append(self)


class Goal:
    ID = ""
    Name = ""
    Motivation = ""
    UpperGoals = []
    SubGoals = [] 
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
            Good = Goal("Be Good", None)
            self.GoalList.append(Good)
        if B:
            Relationships = Goal("Maintain Relationships", None)
            self.GoalList.append(Relationships)
        if C:
            Job = Goal("Provide Value to Society", None)
            self.GoalList.append(Job)
        if D:
            Health = Goal("Be Healthy", None)
            self.GoalList.append(Health)
        
