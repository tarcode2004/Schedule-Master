from backend import *

Tarik = User(False, False, True, True)

Tarik.Bio = "Computer Science Student"
Tarik.ContactList.append({'Christian':56543})
Tarik.AddGoal("Improve Cardiovascular Health", [Tarik.GoalList[1]])
print(Tarik.GoalList[2].UpperGoals[0].Name)
#Tarik.PrintGoals()