import discord
from api import last_commit_date

info_icon = 'https://emoji.gg/assets/emoji/3224_info.png'
question_icon = 'https://emoji.gg/assets/emoji/2825_question.png'
github_url = 'https://github.com/bfaulk96/jerry-the-joke-both'

# potty_words: [str] = ["shit", "fuck", "damn", "pussy", "crap"]
# dad_jokes: [str] = [
#     "Please don't say that shit.",
#     "Fuck outta here with that language.",
#     "What the hell kind of potty mouth is that?",
#     "Damn, where did you learn to talk like that?",
#     "I'm tired of that damn potty mouth of yours.",
#     "You must have a shitty vocabulary to be cussing like that.",
#     "Are you fucking kidding me? Watch your mouth."
# ]


def get_info_embed() -> discord.Embed:
    embed = discord.Embed(color=0x7289da)
    embed.set_author(name="Info", icon_url=info_icon)
    lcd = last_commit_date()
    embed.set_footer(text=f"Bot last updated {lcd:%m/%d/%Y at %I:%M:%S %p %Z}.")
    embed.add_field(name="Github", value=github_url, inline=False)
    embed.add_field(name="Written in", value="[Python](https://www.python.org/)")
    embed.add_field(name="Hosted on", value="[Heroku](https://dashboard.heroku.com/)")
    return embed


def get_help_embed() -> discord.Embed:
    embed = discord.Embed(color=0x3E6CA0)
    embed.set_author(name='Help', icon_url=question_icon)
    options = {
        '$dad': 'Get a random dad joke',
        '$mom': 'Get a random "yo momma" joke',
        '$chuck': 'Get a random Chuck Norris joke',
        '$joke': 'Get a random setup/punchline joke',
        '$nd [info]': 'View Bot info',
        '$help': 'View this help list'
    }

    help_text = "\n".join(list(map(lambda i: f"{i[0]:<14}{i[1]}", list(options.items()))))
    embed.add_field(name='Options', value=f"```bash\n{help_text}\n```")
    return embed
