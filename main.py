from get_stats import Player
import get_build
import get_pos

import discord
import json
import os

def get_config():
    DIR = os.getcwd()

    try:
        json_data = json.load(open(f"{DIR}/config.json"))

        return json_data

    except:
        raise FileNotFoundError(f"Unable to open config.json")

def help_page(error=""):
    output = f"""
===== **Strona Pomocy** ====
{error}
> Aby uzyskać build na daną postać wpisz `{PREFIX}chemp.<NAZWA_POSTACI>`
> Aby zobaczyć jakie postacie idą na daną pozycję, wpisz `{PREFIX}pos.<POZYCJA>` (top, mid, adc, support, jungle)
> Aby uzyskać statystyki innego gracza, wpisz `{PREFIX}stats.<NAZWA_GRACZA>`(nazwa gracza z zachowaniem wielkości liter)"""

    return output

def execute_command(command):
    command = command.split(".")

    if command[0].lower() == "help":
        return help_page()

    try:
        if command[1].lower() == "get_pos":
            pass
    
    except:
        return help_page("**_BŁĄD: Nie podałeś wystarczającej ilości argumentów (elementy po kropce (np. '.chemp'))_**")

    if command[0].lower() == "pos":
        global POSITIONS

        current_pos = command[1]

        is_position_valid = False

        for position in POSITIONS:
            if current_pos == position:
                is_position_valid = True

        if not is_position_valid:
            return help_page()

        else:
            position = get_pos.Position(current_pos)
            return position.get_champions()

    elif command[0].lower() == "chemp":
        champion = get_build.Champion(command[1])

        return champion.get_build()

    elif command[0].lower() == "stats":
        summoner_name = command[1]

        player = Player(summoner_name, API_KEY, "eun1", "europe")

        return player.get_stats()

## setting up
client = discord.Client()

config = get_config()

PREFIX = config["prefix"]
POSITIONS = ["top", "mid", "adc", "support", "jungle"]
BOT_NAME = config["bot_name"] # name on discord
API_KEY = config["api_key"]
TOKEN = config["token"]

### Reading messages
@client.event
async def on_message(msg):
    if msg.content.find(PREFIX) != -1:
        author = str(msg.author)

        if author != BOT_NAME:
            command = str(msg.content).replace(PREFIX, "")

            result = execute_command(command)

            await msg.channel.send(result)

client.run(TOKEN)
