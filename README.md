# slackbot-workout
A fun hack that gets Slackbot to force your teammates to work out!

<img src = "https://ctrlla-blog.s3.amazonaws.com/2015/Jun/Screen_Shot_2015_06_10_at_5_57_55_PM-1433984292189.png" width = 500>


# Instructions

1. Clone the repo and navigate into the directory in your terminal.

    `$ git clone git@github.com:adamreis/exercise.git`

2. Go to https://api.slack.com/web, sign in, scroll down, and click "Create Token" for the Slack org you want to get #ripped.

3. Create a `secrets.py` file in that directory with only one line containing your shiny new API token:
```
SLACK_API_TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'
```

4. Customize exercises/stretches/rep counts/channel names in `slackbotEercise.py` (should be self explanatory, but get in touch if you have any questions).

5. If you haven't set up pip for python, go in your terminal and run:

    `$ sudo easy_install pip`

6. While in the project directory, run (preferrably with Python3 ;)

    `$ sudo pip install -r requirements.txt`

    `$ python slackbotExercise.py`

Run the script to start the workouts and hit ctrl+c to stop the script. Hope you have fun with it!
