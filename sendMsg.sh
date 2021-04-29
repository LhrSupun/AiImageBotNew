#!/bin/bash
export BOTTOKEN='<token>'
export REDISURL='redis://127.0.0.1:6379'
#redis-server /etc/redis/6379.conf
python3 sendMsg.py &>/dev/null &
exit 0
