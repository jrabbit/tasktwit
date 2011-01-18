#import oauth2 as oauth
import urllib2
import urllib
import hashlib
import getpass
import json

API_KEY ='4610d9ec2da135a2af02663519e7d2a3'
API_SECRET = '5ae73f6172fbaa3aa6244897a4a0cdae'
url = 'https://api.producteev.com/'


def auth(user):
    password = getpass.getpass('Your producteev password:')
    raw_values = {'email': user, 'password': password, 'api_key': API_KEY}
    data = hancock(raw_values)
    # print values
    login_json = urllib2.urlopen(url + 'users/login.json', data).read()
    print login_json
    print "Authenticated with producteev!"
    return json.loads(login_json)['login']['token']

def hancock(values):
    """take a dict of REST data and make md5 signature"""
    phrases = []
    for x,y in values.iteritems():
        phrases.append(x+y)
    phrases.sort() 
    hash_me =  ''.join(phrases) + API_SECRET
    #cat the phrases together
    signature = hashlib.md5(hash_me).hexdigest()
    values['api_sig'] = signature
    data = urllib.urlencode(values)
    return data

def get_tasks(token):
    """Convience function to return the user's tasks"""
    raw_values = {'token': token, 'api_key': API_KEY}
    data = hancock(raw_values)
    tasks_json = urllib2.urlopen(url + 'tasks/show_list.json', data).read()
    print json.loads(tasks_json)

def add_task(task, token):
    """Convience function to add a task"""
    raw_values = {'token': token, 'api_key': API_KEY, 'title': task}
    data = hancock(raw_values)
    confirm_json = urllib2.urlopen(url + 'tasks/create.json', data).read()
    return confirm_json


if __name__ == '__main__':
    import sys
    if sys.argv[1]:
        auth(sys.argv[1])
    else:
        print "Provide a username."
    auth(sys.argv[1])