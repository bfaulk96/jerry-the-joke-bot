import json
import random
import requests
import datetime
from dateutil import tz

headers: dict = {'user-agent': 'jerry-the-joke-bot/0.0.1', 'Accept': 'application/json'}
github_api_url = 'https://api.github.com/repos/bfaulk96/jerry-the-joke-bot/commits/main'


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


def get_joke(num_lines: int = None) -> (str, str):
    num = num_lines
    if num_lines is None:
        num = random.randint(1, 2)

    url = 'https://v2.jokeapi.dev/joke/Any'
    blacklist = 'blacklistFlags=nsfw,racist,sexist'
    response = requests.get(f"{url}?{blacklist}&type={'twopart' if num == 2 else 'single'}", headers=headers)
    joke_json = json.loads(response.text)
    return (None, joke_json['joke']) if 'joke' in joke_json else (joke_json['setup'], joke_json['delivery'])


def get_insult(names: str = '') -> str:
    # TODO: If names is `mentions`, then we need to substitute names and replace them.
    #   If names is just a string, pass it in as-is (current behavior)
    plural = 'plural=on' if names and any([x in names for x in [' ', ',']]) else ''
    who = f"who={names}" if names else ''
    params = "&".join(list(filter(lambda x: bool(x), [plural, who])))
    response = requests.get(f'https://insult.mattbas.org/api/insult?{params}')
    return response.text


# def get_2_part_joke() -> (str, str):
#     response = requests.get("https://official-joke-api.appspot.com/jokes/programming/random", headers=headers)
#     json_data = json.loads(response.text)[0]
#     return json_data['setup'], json_data['punchline']


def last_commit_date() -> datetime.datetime:
    response = requests.get(github_api_url, headers=headers)
    iso_date = json.loads(response.text)['commit']['author']['date']
    date = datetime.datetime.fromisoformat(iso_date[:-1]).astimezone(tz.tzlocal()).replace(tzinfo=tz.tzutc())
    return date.astimezone(tz.tzlocal())
