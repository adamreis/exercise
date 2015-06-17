from secrets import SLACK_API_GET_TOKEN, SLACK_API_POST_TOKEN
from pprint import pprint
import requests
import time
import threading
import random

POST_MESSAGE_BASE_URL = "https://makeschool.slack.com/services/hooks/slackbot"
LIST_CHANNEL_BASE_URL = "https://slack.com/api/channels.list"

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
        "units": "",
        "rep_range": (1,2)
    },
    "quad": {
       "name": "QUAD STRETCH",
        "units": "",
        "rep_range": (1,2)
    },
    "hip_flexor": {
       "name": "HIP FLEXOR STRETCH",
        "units": "",
        "rep_range": (1,2)
    },
    "side": {
       "name": "SIDE STRETCH",
        "units": "",
        "rep_range": (1,2)
    },
    "knee_to_chest": {
       "name": "KNEE TO CHEST STRETCH",
        "units": "",
        "rep_range": (1,2)
    },
    "shoulder": {
       "name": "SHOULDER STRETCH",
        "units": "",
        "rep_range": (1,2)
    },
    "neck": {
       "name": "NECK STRETCH",
        "units": "",
        "rep_range": (1,2)
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

def sleep_and_activity(channel_name, activities, time_interval):
    activity = activities.get(random.choice(list(activities.keys())))
    delay = int(random.randrange(*time_interval)/60.0)*60
    
    announcement = "NEXT LOTTERY FOR {} IS IN {} MINUTES".format(activity.get("name"), int(delay/60))
    print(announcement)
    print(post_to_channel(channel_name, announcement))
    time.sleep(delay)
    
    victim = random_user_mention(channel_name)
    reps = random.randrange(*activity.get("rep_range"))
    message = "{} {}{} RIGHT NOW {}".format(reps, activity.get("units"), activity.get("name"), victim)
    print(message)
    print(post_to_channel(channel_name, message))
    sleep_and_activity(channel_name, activities, time_interval)

def exercise():
    thread = threading.Thread(target=sleep_and_activity, args=("exercise", EXERCISES, (240, 900)), kwargs={})
    thread.start()

def stretch():
    thread = threading.Thread(target=sleep_and_activity, args=("stretching", STRETCHES, (240, 900)), kwargs={})
    thread.start()

if __name__ == "__main__":
    exercise()
    stretch()
