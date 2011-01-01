import os
import sys
import anydbm
import platform
import hashlib
import time
import json

# a bit of repeat code from hitman

def directory():
    """Construct tasktwit_dir from os name"""
    home = os.path.expanduser('~')
    if platform.system() == 'Linux':
        hitman_dir = os.path.join(home, '.tasktwit')
    elif platform.system() == 'Darwin':
        hitman_dir = os.path.join(home, 'Library', 'Application Support',
         'tasktwit')
    elif platform.system() == 'Windows':
        hitman_dir = os.path.join(os.environ['appdata'], 'tasktwit')
    else:
        hitman_dir = os.path.join(home, '.tasktwit')
    if not os.path.isdir(tasktwit_dir):
        os.mkdir(tasktwit_dir)
    return tasktwit_dir

def get_db():
    """Get database of synced tasks.
    db[sha1] = jsonobj"""
    db = anydbm.open(os.path.join(directory(), 'sync'), 'c')
    return db

def is_new(task):
    taskdb = get_db()
    if hashlib.sha1(task).hexdigest() in taskdb.keys():
        return False
    else:
        return True

def add(task, source, dests):
    taskdb = get_db()
    taskdb[hashlib.sha1(task).hexdigest()] = json.dumps({'text':task,
     'date': time.ctime(), 'source': source, 'dest': dests })
    