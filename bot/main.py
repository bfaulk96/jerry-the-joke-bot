import discord
import os
from dotenv import load_dotenv
import requests
import json
# import random

load_dotenv()
client = discord.Client()
potty_words = ["shit", "fuck", "damn", "pussy", "crap"]
dad_jokes = [
    "Please don't say that shit.",
    "Fuck outta here with that language.",
    "What the hell kind of potty mouth is that?",
    "Damn, where did you learn to talk like that?",
    "I'm tired of that damn potty mouth of yours.",
    "You must have a shitty vocabulary to be cussing like that.",
    "Are you fucking kidding me? Watch your mouth."
]

headers = {'user-agent': 'no-daddy/0.0.1', 'Accept': 'application/json'}


def get_dad_joke():
    response = requests.get("https://icanhazdadjoke.com/", headers=headers)
    json_data = json.loads(response.text)
    return json_data['joke']


def get_yo_momma_joke():
    response = requests.get("https://api.yomomma.info/", headers=headers)
    json_data = json.loads(response.text)
    return json_data['joke']


def get_chuck_norris_joke():
    response = requests.get("https://api.chucknorris.io/jokes/random", headers=headers)
    json_data = json.loads(response.text)
    return json_data['value']


def get_2_part_joke():
    response = requests.get("https://official-joke-api.appspot.com/jokes/programming/random", headers=headers)
    json_data = json.loads(response.text)[0]
    return json_data['setup'], json_data['punchline']


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content.lower()

    if msg.startswith('$dad'):
        await message.channel.send(get_dad_joke())
    if msg.startswith('$mom'):
        await message.channel.send(get_yo_momma_joke())
    if msg.startswith('$chuck'):
        await message.channel.send(get_chuck_norris_joke())
    if msg.startswith('$joke'):
        setup, punchline = get_2_part_joke()
        await message.channel.send(setup)
        await message.channel.send(f"||{punchline}||")
    if msg.startswith('$help'):
        await message.channel.send('''
Options include:
```bash
$dad    – Get a random dad joke
$mom    – Get a random "yo momma" joke
$chuck  – Get a random Chuck Norris joke
$joke   – Get a random setup/punchline joke
$help   – View this help list
```
''')

    # if any(word in msg for word in potty_words):
    #     await message.channel.send(random.choice(dad_jokes))

token = os.getenv('TOKEN')
client.run(token)
