<<<<<<< HEAD
__title__ = 'Discord Bot'
__author__ = 'Axmouth'
__license__ = 'GPL v2'
__copyright__ = 'Copyright 2018-9001 Axmouth'
__version__ = '0.1.0'

from discord.ext.commands import Bot
from discord import Game
import discord
import asyncio
import requests
import random

TOKEN = 'NDMzMjUwNjcxNTIxNjkzNzAz.Da5N-g.RYd58OiLLVxRls3CrlxZe3wvyaM'
BOT_PREFIX = ('~')
SELF_ASSIGN_ROLES = []

client = Bot(command_prefix = BOT_PREFIX)

@client.command(name='8ball',
                description='Answer a yes or no question',
                brief='Answers from the beyond..',
                aliases=['eightball', 'eight_ball', '8_ball'],
                pass_context=True,)
async def eight_ball(context):
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
    ]

    await client.say(nocodify(random.choice(possible_responses) + ", " + context.message.author.mention))


@client.command(name='gimme',
                description='Give yourself a self-assignable role',
                brief='Self assign roles',
                aliases=['iam', 'nome', 'assignme'],
                pass_context=True,)
async def gimme(context):
    server = context.message.server
    member = context.message.author
    member_roles = member.roles
    try:
        rolename = context.message.content.split(" ", 1)[1]
        role = discord.utils.get(server.roles, name=rolename)
        if not discord.utils.get(server.roles, name=rolename):
            await client.say(nocodify("There is no such role" + ", " + context.message.author.mention))
            return
        if discord.utils.get(member_roles, name=rolename):
            await client.say(nocodify("You already have this role" + ", " + context.message.author.mention))
            return
        await client.add_roles(member, role)
        await client.say(nocodify("You now have the role " + rolename + ", " + context.message.author.mention))
    except:
        await client.say(nocodify("You cannot assign this role" + ", " + context.message.author.mention))


@client.command(name='offofme',
                description='Remove from yourself a self-assignable role',
                brief='Self remove roles',
                aliases=['iamnot', 'noyou', 'no_u', 'remove'],
                pass_context=True,)
async def offofme(context):
    server = context.message.server
    member = context.message.author
    member_roles = member.roles
    try:
        rolename = context.message.content.split(" ", 1)[1]
        if not discord.utils.get(server.roles, name=rolename):
            await client.say(nocodify("There is no such role" + ", " + context.message.author.mention))
            return
        if not discord.utils.get(member_roles, name=rolename):
            await client.say(nocodify("You do not have this role" + ", " + context.message.author.mention))
            return
        role = discord.utils.get(server.roles, name=rolename)
        await client.remove_roles(member, role)
        await client.say(nocodify("You now do not have the role " + rolename + ", " + context.message.author.mention))
    except:
        await client.say(nocodify("You cannot remove this role" + ", " + context.message.author.mention))


@client.command(name='listroles',
                description='List of all roles',
                brief='List roles',
                aliases=['roles', 'serverroles', 'assignableroles', 'roles?'],
                pass_context=True,)
async def listroles(context):
    server = context.message.server
    member = context.message.author
    member_roles = member.roles
    rolestext = "The server allows you to assign the following roles:\n\n"
    try:
        for role in server.roles:
            if role.is_everyone or role.managed:
                continue

            rolestext += role.name + "\n"
        await client.say(codifyplus(rolestext))
    except:
        await client.say(nocodify("Ops?"))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=Game(name='with Elisa'))


@client.command()
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    try:
        response = requests.get(url)
        value = response.json()['bpi']['USD']['rate']
        await client.say("Bitcoin price is: $" + value)
    except:
        await client.say("Error contacting server..")


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print("\t" + server.name)

        await asyncio.sleep(120)


def nocodify(text):
    return text


def nocodifyplus(text):
    return text


def codify(text):
    return "`" + text + "`"


def codifyplus(text):
    return "```" + text + "```"


if __name__ == "__main__":
    print("started \n")
    client.loop.create_task(list_servers())
=======
__title__ = 'Discord Bot'
__author__ = 'Axmouth'
__license__ = 'GPL v2'
__copyright__ = 'Copyright 2018-9001 Axmouth'
__version__ = '0.1.0'

from discord.ext.commands import Bot
from discord import Game
import discord
import asyncio
import requests
import random

TOKEN = 'NDMzMjUwNjcxNTIxNjkzNzAz.Da5N-g.RYd58OiLLVxRls3CrlxZe3wvyaM'
BOT_PREFIX = ('~')
SELF_ASSIGN_ROLES = []

client = Bot(command_prefix = BOT_PREFIX)

@client.command(name='8ball',
                description='Answer a yes or no question',
                brief='Answers from the beyond..',
                aliases=['eightball', 'eight_ball', '8_ball'],
                pass_context=True,)
async def eight_ball(context):
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
    ]

    await client.say(nocodify(random.choice(possible_responses) + ", " + context.message.author.mention))


@client.command(name='gimme',
                description='Give yourself a self-assignable role',
                brief='Self assign roles',
                aliases=['iam', 'nome', 'assignme'],
                pass_context=True,)
async def gimme(context):
    server = context.message.server
    member = context.message.author
    member_roles = member.roles
    try:
        rolename = context.message.content.split(" ", 1)[1]
        role = discord.utils.get(server.roles, name=rolename)
        if not discord.utils.get(server.roles, name=rolename):
            await client.say(nocodify("There is no such role" + ", " + context.message.author.mention))
            return
        if discord.utils.get(member_roles, name=rolename):
            await client.say(nocodify("You already have this role" + ", " + context.message.author.mention))
            return
        await client.add_roles(member, role)
        await client.say(nocodify("You now have the role " + rolename + ", " + context.message.author.mention))
    except:
        await client.say(nocodify("You cannot assign this role" + ", " + context.message.author.mention))


@client.command(name='offofme',
                description='Remove from yourself a self-assignable role',
                brief='Self remove roles',
                aliases=['iamnot', 'noyou', 'no_u', 'remove'],
                pass_context=True,)
async def offofme(context):
    server = context.message.server
    member = context.message.author
    member_roles = member.roles
    try:
        rolename = context.message.content.split(" ", 1)[1]
        if not discord.utils.get(server.roles, name=rolename):
            await client.say(nocodify("There is no such role" + ", " + context.message.author.mention))
            return
        if not discord.utils.get(member_roles, name=rolename):
            await client.say(nocodify("You do not have this role" + ", " + context.message.author.mention))
            return
        role = discord.utils.get(server.roles, name=rolename)
        await client.remove_roles(member, role)
        await client.say(nocodify("You now do not have the role " + rolename + ", " + context.message.author.mention))
    except:
        await client.say(nocodify("You cannot remove this role" + ", " + context.message.author.mention))


@client.command(name='listroles',
                description='List of all roles',
                brief='List roles',
                aliases=['roles', 'serverroles', 'assignableroles', 'roles?'],
                pass_context=True,)
async def listroles(context):
    server = context.message.server
    member = context.message.author
    member_roles = member.roles
    rolestext = "The server allows you to assign the following roles:\n\n"
    try:
        for role in server.roles:
            if role.is_everyone or role.managed:
                continue

            rolestext += role.name + "\n"
        await client.say(codifyplus(rolestext))
    except:
        await client.say(nocodify("Ops?"))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=Game(name='with Elisa'))


@client.command()
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    try:
        response = requests.get(url)
        value = response.json()['bpi']['USD']['rate']
        await client.say("Bitcoin price is: $" + value)
    except:
        await client.say("Error contacting server..")


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print("\t" + server.name)

        await asyncio.sleep(120)


def nocodify(text):
    return text


def nocodifyplus(text):
    return text


def codify(text):
    return "`" + text + "`"


def codifyplus(text):
    return "```" + text + "```"


if __name__ == "__main__":
    print("started \n")
    client.loop.create_task(list_servers())
>>>>>>> 1617fb25361258a7a5490abe68af4d7e1306efa8
    client.run(TOKEN)