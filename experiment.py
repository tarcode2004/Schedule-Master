from backend import *

Tarik = User()# Create User

Tarik.AddGoal("Improve Cardiovascular Health", [Tarik.GoalList[0]]) # Add Sub Goal

Tarik.GoalList[1].Tasks.append(Task("Go on a run", Tarik.GoalList[1]))
print(Tarik.GoalList[1].Tasks[0].Name)


Tarik.Bio = "Computer Science Student"
Tarik.ContactList.append({'Christian':56543})
Tarik.PrintGoals()