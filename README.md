# Hacktime project - slackbot

Project: Minigames slackbot
This bot basically is for slack and lets you play various minigames. New, so only has one minimage


How to use?
create a new .env file with this:
```

SLACK_BOT_TOKEN=xoxb-
SLACK_APP_TOKEN=xapp-
```

install the reqs:
```
pip install -r requirements.txt
```
then run the bot:
```
python bot.py
```


# How to setup the bot?
Go here:

https://api.slack.com/apps


Create a new app from scratch

Scroll down in general -> App-Level Token

Create new one with write scope (this is your App Token)



Got to sockets -> enable it

scroll down and click on "Slash commands"

create new slack commad: /3t


for bot token, go to oAuth and perms

scroll down, add the `chat:write` and `commands` perm

scroll back app and create an oAuth token


done

i think

hopefully

idk prob forgot something ig

