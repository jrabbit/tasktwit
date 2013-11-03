import sys
import time
import anydbm
import os
import datetime
import hashlib
try:
  import json
except ImportError:
    import simplejson as json
if sys.platform != "darwin":
    sys.exit("Targets TheHitList on Mac OS X only.")
import TheHitList
import support.directory
import support.twitter as twitter

consumer_key = 'eFbUI4ee3Zb1xpWMoi95A'
consumer_secret = '7PBZdw0QBZb7JtRGdUQRvMpTm9WKUJ9pWSZdAwv1cDE'

def get_settings():
    db = anydbm.open(os.path.join(support.directory.directory(),
    'settings'), 'c')
    return db

def get_db():
    """Get database of synced tasks. db[sha1] = jsonobj"""
    db = anydbm.open(os.path.join(support.directory.directory(), 'sync'), 'c')
    return db

def is_new(task):
    taskdb = get_db()
    if hashlib.sha1(task).hexdigest() in taskdb.keys():
        return False
    else:
        return True

def make_api():
    settings = get_settings()
    access_token_key = settings['twitter-user-key']
    access_token_secret = settings['twitter-user-secret']
    api = twitter.Api(consumer_key,consumer_secret, access_token_key,
    access_token_secret)
    return api

def forward(api):
    settings = get_settings()
    if api.GetDirectMessages():
        for msg in api.GetDirectMessages():
            if str(msg.sender_screen_name) in json.loads(settings['twitter-authorized-users']):
                add_task(msg.AsDict())

def db_setup():
    settings = get_settings()
    settings['twitter-authorized-users'] = json.dumps([raw_input('Which twitter user do you want tasks to come from? ')])
    settings['twitter-user-key'] = raw_input('Your Twitter Access Token key: ')
    settings['twitter-user-secret'] = raw_input('Twitter Access Token secret: ')
    settings['twitter-setup'] = 'done'

def add_task(msg):
    task = str(msg['text'])
    if is_new(task):
        thl = TheHitList.Application()
        thl_task = TheHitList.Task()
        thl_task.title = task
        # thl_task.start_date = datetime.datetime.now()
        thl.inbox().add_task(thl_task)
        taskdb = get_db()
        taskdb[hashlib.sha1(task).hexdigest()] = json.dumps({'text':task,
         'date': time.ctime(), 'source': 'twitter', 'dest': 'thl', 'done': 0 })

def is_first_run():
    if 'twitter-setup' in get_settings():
        return False
    else:
        return True

if __name__ == '__main__':
    if is_first_run():
        db_setup()
    api = make_api()
    pause = 3600. / api.GetRateLimitStatus()['hourly_limit']
    while True:
        forward(api)
        time.sleep(pause)
