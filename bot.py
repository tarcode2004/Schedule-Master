from asyncio import Task
import azureservies
import backend

def JournalNote():
    azureservies.TTS("What do you have to say about this task?")
    Note = azureservies.STT()
    return Note

def YN(string):
    azureservies.TTS(string)
    result = azureservies.YN()
    return result

def TaskStatus(Task):
    Goal = Task.Goal
    TaskName = Task.Name
    Prompt = "did you " + TaskName
    azureservies.TTS(Prompt)
    JI = backend.JournalEntry
    TaskStatus = azureservies.TSU()

    if TaskStatus == "Task Completed":
        result = YN("Would you like to save a note with this task?")
        if result == "yes":
            Note = JournalNote()
            JI  = backend.JournalEntry(Task, TaskStatus, Note)#new journal entry
            Goal.Journal.append(
                JI
            )
        else:
            JI  = backend.JournalEntry(Task, TaskStatus)#new journal entry
            Goal.Journal.append(
                JI
            )

    elif TaskStatus == "Working on Task":
        azureservies.TTS("When will you be finished?")
        Note = azureservies.STT()
        JI = backend.JournalEntry(Task, TaskStatus, None)#new journal entry
        Goal.Journal.append(
            JI
        )
        #Undersatnd time
        #Reschedule task for that time

    elif TaskStatus == "Partially Completed":
        Note = JournalNote()
        JI = backend.JournalEntry(Task, TaskStatus, Note)#new journal entry
        Goal.Journal.append(
            JI
        )
    elif TaskStatus == "Did not complete":
        azureservies.TTS("Why didn't you complete the task?")
        Excuse = azureservies.NCU()
        Note = JournalNote()
        JI = backend.JournalEntry(Task, TaskStatus, Note, Excuse)#new journal entry
        Goal.Journal.append(
            JI
        )
    elif TaskStatus == "None": 
        Note = JournalNote()
        JI = backend.JournalEntry(Task, TaskStatus, Note)#new journal entry
        Goal.Journal.append(
            JI
        )