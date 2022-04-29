import backend
import bot
import requests
import json


def PostJournal( Name, Status, Note, Excuse):
        Journal = {}
        Journal['Name'] = Name
        Journal['Status'] = Status
        Journal['Note'] = Note
        Journal['Excuse'] = Excuse
        data = json.dumps(Journal)
        print(data)
        result = requests.patch("https://masterschedule-be192-default-rtdb.firebaseio.com/" + "TrKnJb5kpwWBep4lk2ywdsAkep63" + "/Journal" ".json", data=data)
        print(result)

def GetJournal():
        result = requests.get("https://masterschedule-be192-default-rtdb.firebaseio.com/" + "TrKnJb5kpwWBep4lk2ywdsAkep63" + "/Journal" ".json")
        data = json.loads(result.content.decode())
        print(data)

Health = backend.Goal("Get Health", "Live Longer", "none", "ABS", "ABC")
Run = backend.Task('Go on a run', "Yes", Health, "None", "none", "none", "none")
Run.Goal = Health
Run.Name = 'Go on a run'

bot.TaskStatus(Run)

print("Task Name:", Health.Journal[0].Task.Name)
print("Status:", Health.Journal[0].Status)
print("Note:", Health.Journal[0].Note)
print("Excuse:", Health.Journal[0].Excuse)

PostJournal(Health.Journal[0].Task.Name,Health.Journal[0].Status,Health.Journal[0].Note,Health.Journal[0].Excuse)
GetJournal()


