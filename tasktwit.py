import sys
import TheHitList

import support.twitter as twitter
from conf import *

api = twitter.Api(consumer_key,consumer_secret, access_token_key,
access_token_secret)

if api.GetDirectMessages():
    for msg in api.GetDirectMessages():
        if str(msg.sender_screen_name) in authorized_users:
            add_task(msg.AsDict())


def add_task(msg):
    task = msg.text
    thl = TheHitList.Application()
    thl_task = TheHitList.Task()
    thl_task.title = task
    thl.inbox().add_task(thl_task)