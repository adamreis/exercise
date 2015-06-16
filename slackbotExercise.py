import random
import time
import requests
import json
import csv

USERTOKENSTRING = ""
URLTOKENSTRING =  ""

def extractSlackUsers(token):
    # Set token parameter of Slack API call
    tokenString = token
    params = {"token": tokenString}

    # Capture Response as JSON
    response = requests.get("https://slack.com/api/users.list", params=params)
    users = json.loads(response.text, encoding='utf-8')["members"]

    def findUserNames(x):
        if getStats(x) == False:
            return None
        name = "@" + x["name"].encode('utf-8')
        return name.encode('utf-8')
    def getStats(x):
        params = {"token": tokenString, "user": x["id"]}
        response = requests.get("https://slack.com/api/users.getPresence",
                params=params)
        status = json.loads(response.text, encoding='utf-8')["presence"]
        return status == "active"

    return filter(None, list(map(findUserNames, users)))

def selectExerciseAndStartTime(exerciseType):

    exercises = []
    exerciseAnnouncements = []
    if exerciseType == "strength":
	# Exercise (2 Forms of Strings)
	exercises = [" PUSHUPS ", " PUSHUPS ", " SECOND PLANK ", " SITUPS ", " SECOND WALL SIT "]
	exerciseAnnouncements = ["PUSHUPS", "PUSHUPS", "PLANK", "SITUPS", "WALLSIT"]

    elif exerciseType == "stretch":
	#Stretch
	exercises = [" SECOND CALF STRETCH ", " SECOND QUAD STRETCH ", " SECOND HIP FLEXOR STRETCH ", 
	" SECOND SIDE STRETCH ", " SECOND KNEE TO CHEST STRETCH ", " SECOND SHOULDER STRETCH ", 
	" SECOND NECK STRETCH "]
	exerciseAnnouncements = ["CALF STRETCH", "QUAD STRETCH", "HIP FLEXOR STRETCH", 
	"SIDE STRETCH", "KNEE TO CHEST STRETCH", "SHOULDER STRETCH", "NECK STRETCH"] 

    # Random Number generator for Reps/Seconds and Exercise
    nextTimeInterval = random.randrange(300, 1200)
    exerciseIndex = random.randrange(0, 5)

    # Announcement String of next lottery time
    if exerciseType == "strength":
	lotteryTimeString = "NEXT LOTTERY FOR " + str(exerciseAnnouncements[exerciseIndex]) + " IS IN " + str(nextTimeInterval/60) + " MINUTES"

	print requests.post("https://makeschool.slack.com/services/hooks/slackbot?token="+URLTOKENSTRING+"&channel=%23exercise", data=lotteryTimeString)
	print lotteryTimeString
	print "sleeping:",nextTimeInterval
	time.sleep(nextTimeInterval)

    return str(exercises[exerciseIndex])


def selectPerson(exercise, exerciseType):

    # Select number of reps
    exerciseReps = random.randrange(10, 35)

    # Pull all users from API
    # slackUsers = extractSlackUsers(USERTOKENSTRING)
    slackUsers = ""
    if exerciseType == "strength":
	slackUsers = ["@jorrie", "@austin_feight", "@jordan", "@adam", "@daniel", "@sara", "@abdul", "@evan", "@jeremy"]
    elif exerciseType == "stretch":
	slackUsers = ["@samara"]

    # Select index of team member from array of team members
    selection = random.randrange(0, len(slackUsers))

    lotteryWinnerString = str(exerciseReps) + str(exercise) + "RIGHT NOW " + slackUsers[selection]
    print lotteryWinnerString
    requests.post("https://makeschool.slack.com/services/hooks/slackbot?token="+URLTOKENSTRING+"&channel=%23exercise", data=lotteryWinnerString)

    """with open("results.csv", 'a') as f:
        writer = csv.writer(f)
        writer.writerow([slackUsers[selection], exerciseReps, exercise])"""

requests.post("https://makeschool.slack.com/services/hooks/slackbot?token="+URLTOKENSTRING+"&channel=%23exercise", data="Good morning, @channel! Who's ready to get ripped?")
for i in range(10000):
    exercise = selectExerciseAndStartTime("strength")
    stretch = selectExerciseAndStartTime("stretch")
    selectPerson(exercise, "strength")
    selectPerson(stretch, "stretch")


