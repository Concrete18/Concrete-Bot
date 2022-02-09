# Concrete Bot

Custom discord bot for my discord server. It is build using the following modules

* discord&#46;py
* requests
* Natural Language Tool Kit

## Auto Startup

Allows easy start up if bot on reboot

```crontab
@reboot `path to startup.bash `
```

## Cogs

* Admin
* AI
* Fun
* Misc
* Member Logging

## Commands

### Admin

* **purge**: Deletes n messages from newest to oldest.

* **changeactivity**: Change the bot's current game with an admin command.

* **pid**: Sends current bot PID.

### Fun

* **flip**: Flip a coin.

* **hello**: Greets Bot and causes the bot to greet you.

* **taco**: Taco

### Member Log

* **active**: Lists active members for the day.

* **inactive**: Lists inactive members. Defaults to 60 days.

* **updatemembers**: Adds members to self.member_data if they are not already in it.

### Misc

* **membercount**: Gets the total members and bots in server.

* **ping**: Fetches latency in milliseconds.

* **poll**: Creates a poll that allows voting with reactions and allows entering an end time in hours.

* **schedulemsg**: Schedule a message to be sent after a specific number o...

* **servertime**: Fetches current date and time for the server.

* **uptime**: Gets Bot uptime.

### RPG

* **roll**: Roll dice with the NdN format.

* **groupsplit**: Splits Plat, Gold, Silver and Copper n ways.

### ReactRole

* **reactrole**: Creates a Embed that allows for gaining a role by react...

### Steam

* **sharedgames**: Finds owned games in common using steam id's.
