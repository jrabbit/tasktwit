import appscript

def add_task(task):
    appscript.app("Reminders").make(new=k.reminder, with_properties={k.name:task})