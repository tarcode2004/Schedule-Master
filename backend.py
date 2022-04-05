import uuid

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
        ID = uuid.uuid4()
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
            print(self.GoalList[x].Name, " : ", end="")
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
    