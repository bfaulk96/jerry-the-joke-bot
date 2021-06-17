import discord
import os
from dotenv import load_dotenv
import requests
import json
import random

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


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " – " + json_data[0]['a']
    return quote


def get_dad_joke():
    headers = {'user-agent': 'no-daddy/0.0.1', 'Accept': 'application/json'}
    response = requests.get("https://icanhazdadjoke.com/", headers=headers)
    json_data = json.loads(response.text)
    return json_data['joke']


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content.lower()

    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if msg.startswith('$dad'):
        dj = get_dad_joke()
        await message.channel.send(dj)

    if msg.startswith('$yobi'):
        await message.channel.send('ahh, he crazy')

    if any(word in msg for word in potty_words):
        await message.channel.send(random.choice(dad_jokes))

token = os.getenv('TOKEN')
client.run(token)
