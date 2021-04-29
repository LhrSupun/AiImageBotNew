#!/usr/bin/env python3
import os
import requests
import redis
import time
from pathlib import Path

def tester(rq,keys):
    keys_values = rq.get(keys).decode("UTF-8")
    print(keys_values)
    return keys_values

def send_announcments(bot_message,db_keys,bot_token,rq):
    for keys in db_keys:
        keys_values = tester(rq,keys)
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?c                                                                                        hat_id=' + keys_values + '&text=' + bot_message
        print(send_text)
        response = requests.get(send_text).json()
        print (response)
        time.sleep(1)


def main():
    r = redis.from_url(os.environ.get(('REDISURL')))
    db_keys = r.keys(pattern="*")
    bot_token = os.environ.get(('BOTTOKEN'))
    p = Path("message_bot.txt").resolve()
    bot_message = open(str(p))
    text_content = bot_message.read()
    send_announcments(bot_message = text_content,db_keys=db_keys,bot_token=bot_t                                                                                        oken,rq=r)

if __name__ == '__main__':
    main()
