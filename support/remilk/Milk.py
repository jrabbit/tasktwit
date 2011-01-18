#!/usr/bin/env python
# Milk.py - A wrapper for the pyrtm interface for the Remember The Milk API

__version__ = "0.1"
__author__  = "Glenn Hope"
__email__   = "hopega@email.wofford.edu"

# Modified by Jrabbit 2011. 
# Glenn Hope licensed this GPLv3 according to google code.

#Imports
import time
import calendar
import pprint
from rtm import createRTM, API

class Milk:
    def __init__(self, apiKey, secret, token=None):
        self.rtm = createRTM(apiKey, secret, token)
        #do any other loading from the config here, assign to self.

#Lists
    def getListID(self, listname):
        for lst in self.rtm.lists.getList().lists.list:
            if lst.name == listname:
                return lst.id

    def getTasks(self, list_id):
        return self.rtm.tasks.getList(list_id=list_id).tasks.list.taskseries

#Tasks
    def addTask(self, taskname, list_id, smartadd=True):
        self.rtm.tasks.add(timeline=self.rtm.timelines.create().timeline,
                        name=taskname,
                        list_id = list_id,
                        parse=smartadd)

    def completeTask(self, taskname, list_id):
        self.rtm.tasks.complete(timeline=self.rtm.timelines.create().timeline,
                        list_id = list_id,
                        taskseries_id=taskname,
                        task_id=True)

    def printAllTaskInfo(self, list_id):
        tasklist = dottedDictToList(self.getTasks(list_id))
        for task in tasklist:
            pprint.pprint(task)
            print "-" * 80

    def getFormattedTaskInfo(self, list_id):
        taskinfo = []
        tasklist = self.getTasks(list_id)
        #attributes to be printed, move these to milkConfig.py
        #TODO: add fix for task being a list (taskname var which is either 'task' or 'task[i]'?)
        
        defaultAttr = ['task.priority', 'name', 'task.due', 'task.postponed']
                            
        for taskseries in tasklist:
            if type(taskseries.task) not in (list, tuple):
                if not taskseries.task.completed:
                    taskinfo += [[eval("taskseries." + attr) for attr in defaultAttr]]
        return sorted(taskinfo)

        #what was this going to do? sort by date?
        return sorted(taskinfo, lambda s, t: self.pr(s, t))

    def pr(s, t):
        print s
        print t


#    def printCSVTaskInfo(self, list_id):
#        #TODO: add cmdline option to specify output format
#        #for outputting as csv
#        defaultStyle = '"%s","%s","%s","%s"'
#        taskinfo = self.getFormattedTaskInfo(list_id)
#        for task in taskinfo:
#            task[dateIndex] = testTimeFormat(task[dateIndex])

    def printFormattedTaskInfo(self, list_id):
        taskinfo = self.getFormattedTaskInfo(list_id)

        #consider having a lookup table for these against api methods
        defaultNames = ['Pr', 'Name', 'Due', 'Postponed']

        maxLength = 40
        defaultStyle = "| %2s | %-" + str(maxLength) + "s | %-24s | %9s |"

        #make this a list if needed
        nameIndex = 1
        dateIndex = 2

        titlestring = defaultStyle % tuple(defaultNames)
        dashes = "-" * len(titlestring)
        print dashes
        print titlestring
        print dashes

        #format each task and print it
        for task in taskinfo:
            splStr = splitString(task[nameIndex], maxLength)
            task[nameIndex] = splStr[0]
            task[dateIndex] = testTimeFormat(task[dateIndex])
            print defaultStyle % tuple(task)
            for string in splStr[1:]:
                print defaultStyle % ("", string, "", "")
            print dashes

#API
    def returnAPIMethods(self):
        types = API.items()
        types.sort()
        output = []
        for type, methods in types:
            cleanedMethods = []
            for method in methods.keys():
                cleanedMethods.append(method)
            output.append([type, cleanedMethods])
        return output

    def printAPIMethods(self):
        pprint.pprint(self.returnAPIMethods())

#Util functions
def dottedDictToList(item):
    output = []
    if str(type(item)) == "<class 'rtm.dottedDict'>":
        children = item.__dict__.items()
        return [dottedDictToList(i) for i in children]
    elif type(item) in (list, tuple):
        return [dottedDictToList(i) for i in item]
    else:
        return item

def testTimeFormat(str):
    try:
        time.strptime(str, '%Y-%m-%dT%H:%M:%SZ')
        str = formatTime(localToUTC(str))
    except ValueError:
        pass
    return str

def splitString(stri, maxlen):
    lst = []
    index = 0
    while index < len(stri) - 1:
        endex = index + maxlen
        slice = stri[index:endex]
        splitStr = slice.rsplit(" ", 1)
        if len(slice) < maxlen:
            currstr = slice
        elif splitStr[0] == "":
            currstr = splitStr[1]
        else:
            currstr = splitStr[0]
        lst.append(currstr)
        index += len(currstr)
    return lst

def localToUTC(timestr):
    timeobj = time.strptime(timestr, '%Y-%m-%dT%H:%M:%SZ')
    convtime = time.localtime(calendar.timegm(timeobj))
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', convtime)

def formatTime(timestr):
    timeobj = time.strptime(timestr, '%Y-%m-%dT%H:%M:%SZ')
    return time.strftime('%c', timeobj)


