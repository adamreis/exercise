#!usr/local/bin/python3

from pprint import pprint
import requests
import time
import threading
import random
import os
import datetime

try:
    SLACK_API_TOKEN = os.environ['SLACK_API_TOKEN']
except ImportError:
    from secrets import SLACK_API_TOKEN

SLACK = Slacker(SLACK_API_TOKEN)

START_TIME = datetime.time(9,0,0)
END_TIME = datetime.time(20,0,0)

EXERCISES = {
    "pushups": {
        "name": "PUSHUPS",
        "units": "",
        "rep_range": (10, 35)
    },
    "plank": {
       "name": "PLANK",
        "units": "SECOND ",
        "rep_range": (10,35)
    },
    "situps": {
       "name": "SITUPS",
        "units": "",
        "rep_range": (10,35)
    },
    "wall_sit": {
       "name": "WALL SIT",
        "units": "SECOND ",
        "rep_range": (10,35)
    },
    "laps": {
       "name": "LAP(S) AROUND OFFICE",
        "units": "",
        "rep_range": (1,3)
    },
    "burpies": {
       "name": "BURPIES",
        "units": "",
        "rep_range": (10,25)
    },
}

STRETCHES = {
    "calf": {
       "name": "CALF STRETCH",
        "units": "SECOND ",
        "rep_range": (7,21)
    },
    "quad": {
       "name": "QUAD STRETCH",
        "units": "SECOND ",
        "rep_range": (7,21)
    },
    "hip_flexor": {
       "name": "HIP FLEXOR STRETCH",
        "units": "SECOND ",
        "rep_range": (7,21)
    },
    "side": {
       "name": "SIDE STRETCH",
        "units": "SECOND ",
        "rep_range": (7,21)
    },
    "knee_to_chest": {
       "name": "KNEE TO CHEST STRETCH",
        "units": "SECOND ",
        "rep_range": (7,21)
    },
    "shoulder": {
       "name": "SHOULDER STRETCH",
        "units": "SECOND ",
        "rep_range": (7,21)
    },
    "neck": {
       "name": "NECK STRETCH",
        "units": "SECOND ",
        "rep_range": (7,21)
    },
}

def names_for_ids(user_ids):
    names = []
    user_ids = set(user_ids)

    response = SLACK.users.list()
    users = response.body.get('members')
    for user in users:
        if user.get("id") in user_ids:
            names.append(user.get("name"))

def users_in_channel(channel_name):
    response = SLACK.channels.list()
    channels = response.body.get('channels')
    for channel in channels:
        if channel.get("name") == channel_name:
            ids = list(channel.get("members"))
            return names_for_ids(ids)

def random_user_mention(channel_name):
    users = users_in_channel(channel_name)
    return "@" + random.choice(users)

def activity_and_sleep(channel_name, activities, time_interval):
    weekday_condition = datetime.datetime.today().weekday() < 5
    time_condition = START_TIME <= datetime.datetime.now().time() <= END_TIME
    
    if weekday_condition and time_condition : #weekday between 9am EST and 5pm PST
        activity = activities.get(random.choice(list(activities.keys())))
        victim = random_user_mention(channel_name)
        reps = random.randrange(*activity.get("rep_range"))
        message = "{} {}{} RIGHT NOW {}".format(reps, activity.get("units"), activity.get("name"), victim)
        print(message)
        print(SLACK.chat.post_message(channel_name, message))

    delay = int(random.randrange(*time_interval)/60.0)*60
    time.sleep(delay)
    
    activity_and_sleep(channel_name, activities, time_interval)

def exercise():
    thread = threading.Thread(target=activity_and_sleep, args=("#exercise", EXERCISES, (240, 900)), kwargs={})
    thread.start()

def stretch():
    thread = threading.Thread(target=activity_and_sleep, args=("#stretching", STRETCHES, (480, 1800)), kwargs={})
    thread.start()

if __name__ == "__main__":
    exercise()
    stretch()
