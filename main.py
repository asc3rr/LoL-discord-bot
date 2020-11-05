import get_build
import get_pos

import discord

PREFIX = "lol."
POSITIONS = ["top", "mid", "adc", "support", "jungle"]
BOT_NAME = "betaLeagueBot#7189" # name on discord

def read_token():
    with open("token.txt", "r") as token_file:
        lines = token_file.readlines()
        return lines[0].strip()

def help_page(error=""):
    output = f"""
===== **Strona Pomocy** ====
{error}
> Aby uzyskać build na daną postać wpisz `{PREFIX}chemp.<NAZWA_POSTACI>`
> Aby zobaczyć jakie postacie idą na daną pozycję, wpisz `{PREFIX}pos.<POZYCJA>` (top, mid, adc, support, jungle)"""

    return output

def execute_command(command):
    command = command.split(".")

    if command[0] == "help":
        return help_page()

    try:
        if command[1] == "get_pos":
            pass
    
    except:
        return help_page("**_BŁĄD: Nie podałeś wystarczającej ilości argumentów (elementy po kropce (np. '.chemp'))_**")

    if command[0] == "pos":
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

    elif command[0] == "chemp":
        champion = get_build.Champion(command[1])

        return champion.get_build()


token = read_token()

client = discord.Client()

### Reading messages
@client.event
async def on_message(msg):
    if msg.content.find(PREFIX) != -1:
        author = str(msg.author)

        if author != BOT_NAME:
            command = str(msg.content).replace(PREFIX, "").lower()
            print(command)

            result = execute_command(command)

            await msg.channel.send(result)

client.run(token)

#TODO pobieranie statystyk z op.gg