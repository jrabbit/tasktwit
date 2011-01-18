import os

import rtm

import remilk.Milk.Milk as Milk
import directory

API_KEY = '012ddccfd49f6960a979c967b03342db'
API_SECRET = 'a97f7ab9bb0e0495'

def get_settings():
    db = anydbm.open(os.path.join(directory.directory(),
    'settings'), 'c')
    return db

def milk(apiKey, secret):
    settings = get_settings()
    if 'rtm-token' in settings:
        moo = Milk(apiKey, secret, settings['rtm-token'])
    else:
        settings['rtm-token'] = auth()
        moo = Milk(apiKey, secret, settings['rtm-token'])
    return moo

def auth():
    """first time auth with RTM"""
    moo = rtm.createRTM(API_KEY, API_SECRET, token=None)
    print 'Allow tasktwit access: ', moo.getAuthURL()
    raw_input('Press enter once you gave access')
    return moo.getToken()

def get_tasks(moo):
    pass

def add_task(task):
    pass

def finish_task(task):
    pass
