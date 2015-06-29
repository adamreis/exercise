#!usr/local/bin/python3

from pprint import pprint
import requests
import time
import threading
import random
import os
from datetime import datetime, time

try:
    SLACK_API_GET_TOKEN = os.environ['SLACK_API_GET_TOKEN']
    SLACK_API_POST_TOKEN = os.environ['SLACK_API_POST_TOKEN']
except ImportError:
    from secrets import SLACK_API_GET_TOKEN, SLACK_API_POST_TOKEN

POST_MESSAGE_BASE_URL = "https://makeschool.slack.com/services/hooks/slackbot"
LIST_CHANNEL_BASE_URL = "https://slack.com/api/channels.list"

START_TIME = time(9,0,0)
END_TIME = time(20,0,0)

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

def name_for_id(user_id):
    params = {"token": SLACK_API_GET_TOKEN}
    response = requests.get("https://slack.com/api/users.list", params=params)
    users = response.json().get("members")

    for user in users:
        if user.get("id") == user_id:
            return user.get("name")

def users_in_channel(channel_name):
    params = {"token": SLACK_API_GET_TOKEN}
    response = requests.get(LIST_CHANNEL_BASE_URL, params=params)
    channels = response.json().get("channels")
    ids = []
    for channel in channels:
        if channel.get("name") == channel_name:
            ids = list(channel.get("members"))
            break
    return ids

def random_user_mention(channel_name):
    ids = users_in_channel(channel_name)
    return "@" + name_for_id(random.choice(ids))

def post_to_channel(channel_name, message):
    params = {
        "token": SLACK_API_POST_TOKEN,
        "channel": "#" + channel_name
    }
    return requests.post(POST_MESSAGE_BASE_URL, params=params, data=message)

def activity_and_sleep(channel_name, activities, time_interval):
    if datetime.today().weekday() < 5 and START_TIME <= datetime.now().time() <= END_TIME: #weeekday between 9am EST and 5pm PST
        activity = activities.get(random.choice(list(activities.keys())))
        victim = random_user_mention(channel_name)
        reps = random.randrange(*activity.get("rep_range"))
        message = "{} {}{} RIGHT NOW {}".format(reps, activity.get("units"), activity.get("name"), victim)
        print(message)
        print(post_to_channel(channel_name, message))

    delay = int(random.randrange(*time_interval)/60.0)*60
    time.sleep(delay)
    
    activity_and_sleep(channel_name, activities, time_interval)

def exercise():
    thread = threading.Thread(target=activity_and_sleep, args=("exercise", EXERCISES, (240, 900)), kwargs={})
    thread.start()

def stretch():
    thread = threading.Thread(target=activity_and_sleep, args=("stretching", STRETCHES, (480, 1800)), kwargs={})
    thread.start()

if __name__ == "__main__":
    exercise()
    stretch()
