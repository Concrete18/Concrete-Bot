#!/bin/bash
if pgrep -f "python3 Concrete_Bot.py" &>/dev/null; then
    echo "Concrete Bot is already runnning"
    exit
else
    echo "Starting Concrete Bot"
    # change directory to discord bot folder
    cd Coding/Discord-Bots
    # create screen for discord bot
    screen -S discord_bot
    # run discord bot
    python3 Concrete_Bot.py 
fi
