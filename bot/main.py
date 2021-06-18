import datetime
import discord
import os
from pathlib import Path
from dotenv import load_dotenv
import requests
import json
from dateutil import tz
from git import Repo, Commit
# import random

load_dotenv()
client: discord.Client = discord.Client()
potty_words: [str] = ["shit", "fuck", "damn", "pussy", "crap"]
dad_jokes: [str] = [
    "Please don't say that shit.",
    "Fuck outta here with that language.",
    "What the hell kind of potty mouth is that?",
    "Damn, where did you learn to talk like that?",
    "I'm tired of that damn potty mouth of yours.",
    "You must have a shitty vocabulary to be cussing like that.",
    "Are you fucking kidding me? Watch your mouth."
]

info_icon = 'https://emoji.gg/assets/emoji/3224_info.png'
github_api_url = 'https://api.github.com/repos/bfaulk96/no-daddy/commits/main'
github_url = 'https://github.com/bfaulk96/no-daddy'
headers: dict = {'user-agent': 'no-daddy/0.0.1', 'Accept': 'application/json'}


def get_dad_joke() -> str:
    response = requests.get("https://icanhazdadjoke.com/", headers=headers)
    json_data = json.loads(response.text)
    return json_data['joke']


def get_yo_momma_joke() -> str:
    response = requests.get("https://api.yomomma.info/", headers=headers)
    json_data = json.loads(response.text)
    return json_data['joke']


def get_chuck_norris_joke() -> str:
    response = requests.get("https://api.chucknorris.io/jokes/random", headers=headers)
    json_data = json.loads(response.text)
    return json_data['value']


def get_2_part_joke() -> (str, str):
    response = requests.get("https://official-joke-api.appspot.com/jokes/programming/random", headers=headers)
    json_data = json.loads(response.text)[0]
    return json_data['setup'], json_data['punchline']


def last_commit_date() -> datetime.datetime:
    response = requests.get(github_api_url, headers=headers)
    iso_date = json.loads(response.text)['commit']['author']['date']
    date = datetime.datetime.fromisoformat(iso_date[:-1]).astimezone(tz.tzlocal()).replace(tzinfo=tz.tzutc())
    return date.astimezone(tz.tzlocal())


def get_info_embed() -> discord.Embed:
    embed = discord.Embed(color=0x7289da)
    embed.set_author(name="Info", icon_url=info_icon)
    lcd = last_commit_date()
    embed.set_footer(text=f"Bot last updated {lcd:%m/%d/%Y at %I:%M:%S %p %Z}.")
    embed.add_field(name="Github", value=github_url, inline=False)
    embed.add_field(name="Written in", value="[Python](https://www.python.org/)")
    embed.add_field(name="Hosted on", value="[Heroku](https://dashboard.heroku.com/)")
    return embed


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    channel: discord.TextChannel = message.channel
    msg: str = message.content.lower()

    if msg.startswith('$dad'):
        return await channel.send(get_dad_joke())
    elif msg.startswith('$mom'):
        return await channel.send(get_yo_momma_joke())
    elif msg.startswith('$chuck'):
        return await channel.send(get_chuck_norris_joke())
    elif msg.startswith('$joke'):
        setup, punchline = get_2_part_joke()
        await channel.send(setup)
        return await channel.send(f"||{punchline}||")
    elif msg.startswith('$nd'):
        args = msg.split()[1:]
        if args[0].startswith('info'):
            await channel.trigger_typing()
            return await channel.send(embed=get_info_embed())
    elif msg.startswith('$help'):
        return await channel.send(embed=discord.Embed(title='Command Options', description='''
```bash
$dad         – Get a random dad joke
$mom         – Get a random "yo momma" joke
$chuck       – Get a random Chuck Norris joke
$joke        – Get a random setup/punchline joke
$nd [info]   – View Bot info
$help        – View this help list
```
'''))

    # if any(word in msg for word in potty_words):
    #     await message.channel.send(random.choice(dad_jokes))
    return

token = os.getenv('TOKEN')
client.run(token)
