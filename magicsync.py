import os
import sys
import anydbm
import platform
import hashlib
import time
import json

import TheHitList
import producteev

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

def get_settings():
    db = anydbm.open(os.path.join(directory(), 'settings'), 'c')
    return db

def is_new(task):
    taskdb = get_db()
    if hashlib.sha1(task).hexdigest() in taskdb.keys():
        return False
    else:
        return True

def add_thl(task):
    # local thl usage
    thl = TheHitList.Application()
    thl_task = TheHitList.Task()
    thl_task.title = task
    thl.inbox().add_task(thl_task)

def add_producteev(task):
    settings = get_settings()
    if 'prod-user-token' in settings:
        token = settings['prod-user-token']
        producteev.add_task(token, task)
    else:
        if 'prod-user' not in settings:
            user = raw_input("Need producteev username:")
            settings['prod-user'] = user
        token = producteev.auth(settings['prod-user'])
        settings['prod-user-token'] = token
        producteev.add_task(token, task)

def add(task, source, dests):
    apps = {'thl': add_thl, 'prod': add_producteev}
    taskdb = get_db()
    taskdb[hashlib.sha1(task).hexdigest()] = json.dumps({'text':task,
     'date': time.ctime(), 'source': source, 'dest': dests })
    for x in dests:
        apps[x](task)
