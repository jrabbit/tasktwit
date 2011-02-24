import os
import sys
import anydbm
import hashlib
import time
import json

import support.thl
import support.producteev
import support.directory


def get_db():
    """Get database of synced tasks.
    db[sha1] = jsonobj"""
    db = anydbm.open(os.path.join(support.directory.directory(), 'sync'), 'c')
    return db

def get_settings():
    db = anydbm.open(os.path.join(support.directory.directory(),
    'settings'), 'c')
    return db

def is_new(task):
    taskdb = get_db()
    if hashlib.sha1(task).hexdigest() in taskdb.keys():
        return False
    else:
        return True

def add_producteev(task):
    settings = get_settings()
    if 'prod-user-token' in settings:
        token = settings['prod-user-token']
        support.producteev.add_task(task, token)
    else:
        if 'prod-user' not in settings:
            user = raw_input("Need producteev username:")
            settings['prod-user'] = user
        token = support.producteev.auth(settings['prod-user'])
        settings['prod-user-token'] = token
        support.producteev.add_task(task, token)
#get prod support.producteev.get_tasks(get_settings()['prod-user-token'])
def add(task, source, dests):
    apps = {'thl': support.thl.add_task, 'prod': add_producteev}
    taskdb = get_db()
    taskdb[hashlib.sha1(task).hexdigest()] = json.dumps({'text':task,
     'date': time.ctime(), 'source': source, 'dest': dests, 'done': 0 })
    for x in dests:
        apps[x](task)
if __name__ == '__main__':
    # while 1:
    for task in support.thl.get_tasks():
        add(task, 'thl', ['prod'])
