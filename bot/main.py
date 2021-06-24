import discord
import os
from dotenv import load_dotenv
from api import get_insult, get_joke, get_yo_momma_joke, get_dad_joke, get_chuck_norris_joke
from helpers import get_help_embed, get_info_embed
from keep_alive import keep_alive

load_dotenv()
client: discord.Client = discord.Client()


@client.event
async def on_ready():
    print(f"Bot has logged in as {client.user}")


@client.event
async def on_message(message: discord.Message):
    author: discord.Member = message.author
    if author == client.user:
        return

    channel: discord.TextChannel = message.channel
    mentioned_users = message.mentions
    msg: str = message.content.lower()

    if msg.startswith('$dad'):
        return await channel.send(get_dad_joke())
    elif msg.startswith('$mom'):
        return await channel.send(get_yo_momma_joke())
    elif msg.startswith('$chuck'):
        return await channel.send(get_chuck_norris_joke())
    elif msg.startswith('$insult'):
        names = msg.partition(' ')[2]
        if names.startswith(('me', 'myself')) or not names or author in mentioned_users:
            return await channel.send(f"{author.mention}, {get_insult()}")
        elif mentioned_users:
            mentions = list(map(lambda x: x.mention, mentioned_users))
            return await channel.send(get_insult(mentions))
        return await channel.send(get_insult(names))
    elif msg.startswith('$joke'):
        option = msg.partition(' ')[2]
        if option.startswith(('1', 'one', 'single')):
            setup, punchline = get_joke(1)
        elif option.startswith(('2', 'two', 'dual', 'setup', 'multi')):
            setup, punchline = get_joke(2)
        else:
            setup, punchline = get_joke()
        return await channel.send(punchline if not setup else f"{setup}\n||{punchline}||")
    elif msg.startswith('$nd'):
        option = msg.partition(' ')[2]
        if option.startswith('info'):
            await channel.trigger_typing()
            return await channel.send(embed=get_info_embed())
    elif msg.startswith('$help'):
        return await channel.send(embed=get_help_embed())

    # if any(word in msg for word in potty_words):
    #     await message.channel.send(random.choice(dad_jokes))
    return


token = os.getenv('TOKEN')
# keep_alive()
client.run(token)
