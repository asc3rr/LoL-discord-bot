from champion import Champion
import discord

PREFIX = "lol."

def read_token():
    with open("token.txt", "r") as token_file:
        lines = token_file.readlines()
        return lines[0].strip()

token = read_token()

client = discord.Client()

### Reading messages
@client.event
async def on_message(msg):
    if msg.content.find(PREFIX) != -1:
        champion_name = str(msg.content).replace(PREFIX, "")

        champion = Champion(champion_name.lower())

        build = champion.get_build()

        await msg.channel.send(f"Champion: `{champion_name.capitalize()}` \nBuild:{build}")

client.run(token)