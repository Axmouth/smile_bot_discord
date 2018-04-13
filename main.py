__title__ = 'Discord Bot'
__author__ = 'Axmouth'
__license__ = 'GPL v2'
__copyright__ = 'Copyright 2018-9001 Axmouth'
__version__ = '0.1.0'

from discord.ext.commands import Bot
from discord import Game
from data_loader import load_data, save_data, load_user_data
import discord
import asyncio
import requests
import random
from textblob import TextBlob
import emoji
import re

SETTINGS_CATEGORIES = ["assignable-roles", "warn-words", "strike-words",
                       "channel-info", "welcome-message", "welcome-channel",
                       "server-info", "neg-react" , "pos-react", "textmuted-users",
                       ]
user_data = load_user_data()
TOKEN = user_data["token"]
BOT_PREFIX = user_data["prefix"] #+ ["when_mentioned"]
SETTINGS_DATA = {}
HEART_EMOJI = "❤"
ANGRY_EMOJI = "😠"

reactions1 = ['✅', '❌']
reactions2 = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

client = Bot(command_prefix=BOT_PREFIX)


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
        "It is certain",
        "It is decidedly so",
        "Without a doubt",
        "Yes definitely",
        "You may rely on it",
        "As I see it, yes",
        "Most likely",
        "Outlook good",
        "Yes",
        "Signs point to yes",
        "Reply hazy try again",
        "Ask again later",
        "Better not tell you now",
        "Cannot predict now",
        "Concentrate and ask again",
        "Don't count on it",
        "My reply is no",
        "My sources say no",
        "Outlook not so good",
        "Very doubtful",
    ]

    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention + ".")


@client.command(name='gimme',
                description='Give yourself a self-assignable role.',
                brief='Self assign roles.',
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
            await client.say("There is no such role" + ", " + context.message.author.mention + ".")
            return
        if discord.utils.get(member_roles, name=rolename):
            await client.say("You already have this role" + ", " + context.message.author.mention + ".")
            return
        await client.add_roles(member, role)
        await client.say("You now have the role " + rolename + ", " + context.message.author.mention + ".")
    except:
        await client.say("You cannot assign this role" + ", " + context.message.author.mention + ".")


@client.command(name='offofme',
                description='Remove from yourself a self-assignable role.',
                brief='Self remove roles.',
                aliases=['iamnot', 'noyou', 'no_u', 'remove'],
                pass_context=True,)
async def offofme(context):
    server = context.message.server
    member = context.message.author
    member_roles = member.roles
    try:
        rolename = context.message.content.split(" ", 1)[1]
        if not discord.utils.get(server.roles, name=rolename):
            await client.say("There is no such role" + ", " + context.message.author.mention + ".")
            return
        if not discord.utils.get(member_roles, name=rolename):
            await client.say("You do not have this role" + ", " + context.message.author.mention + ".")
            return
        role = discord.utils.get(server.roles, name=rolename)
        await client.remove_roles(member, role)
        await client.say("You now do not have the role " + rolename + ", " + context.message.author.mention + ".")
    except:
        await client.say("You cannot remove this role" + ", " + context.message.author.mention + ".")


@client.command(name='listroles',
                description='List of all roles.',
                brief='List roles.',
                aliases=['roles', 'serverroles', 'assignableroles', 'roles?'],
                pass_context=True,)
async def listroles(context):
    global SETTINGS_DATA
    server = context.message.server
    member = context.message.author
    rolestext = "The server allows you to assign the following roles:\n\n"
    try:
        if not SETTINGS_DATA[server.id]["assignable-roles"]:
            await client.say("No roles")
            return
        for rolename in SETTINGS_DATA[server.id]["assignable-roles"]:
            rolestext += rolename + "\n"
        await client.say("```" + rolestext + "```")
    except:
        await client.say("Ops?")


@client.command(name='userid',
                description='Get the id of a mentioned user.',
                brief='Get user id.',
                pass_context=True,)
async def userid(context):
    members = context.message.mentions
    for member in members:
        await client.say("User ID for " + member.mention + " : " + member.id + ".")


@client.command(name='ban',
                description='Ban a user and kick them from the server, preventing them from rejoining.',
                brief='Ban a user.',
                pass_context=True,)
async def ban(context):
    is_admin = check_admin(context.message)
    if not is_admin:
        await client.say("You do not have permissions to use this command.")
        return
    id_list = []
    args = parse_arguments(context.message)
    numdays = 1
    if args:
        if args[0].lower() == "id":
            id_list = args[1:-1]
            if args[-1].isdigit() and len(args[-1]) == 18:
                id_list.append(args[-1])
            elif args[-1].isdigit():
                numdays = int(args[-1])
            for member_id in id_list:
                member = client.get_user_info(member_id)
                if member is None:
                    await client.say("The user with ID " + member_id + " could not be accessed.")
                    continue
                else:
                    id_list.append(member_id)
        else:
            for mention in args:
                member_id = re.sub('[<@>]', '', mention)
                member = await client.get_user_info(member_id)
                if member is None:
                    await client.say("The user with ID " + member_id + " could not be accessed.")
                    continue
                else:
                    id_list.append(member_id)
    for member_id in id_list:
        user = (await client.get_user_info(member_id))
        if user in (await client.get_bans(context.message.server)):
            await client.say(user.mention + " is already banned.")
            continue
        member = discord.Object(id=member_id)
        member.server = discord.Object(id=context.message.server.id)
        try:
            await client.ban(member, delete_message_days=numdays)
            await client.say(user.mention + " has been banned from " + context.message.server.name + ".")
        except:
            await client.say("You didn't have the privilege needed to ban " + user.mention + ".")


@client.command(name='unban',
                description='Unban a user from joining the server.',
                brief='Unban a user.',
                pass_context=True,)
async def unban(context):
    is_admin = check_admin(context.message)
    if not is_admin:
        await client.say("You do not have permissions to use this command.")
        return
    members = context.message.mentions
    args = parse_arguments(context.message)
    if not args:
        banned_users = await client.get_bans(context.message.server)
        new_message_content = "```The following users have been banned on this server:\n\n"
        if not banned_users:
            new_message_content += "None"
        for banned_user in banned_users:
            new_message_content += banned_user.name + " -- " + banned_user.mention + " : " + banned_user.id
        new_message_content += "\n\nUse this command again with the id parameter amd " \
                               "an appropriate user ID or copy the mention code."
        new_message_content += "```"
        await client.say(new_message_content)
    elif not members and args[0].lower() == "id":
        for member_id in args[1:]:
            member = await client.get_user_info(member_id)
            members.append(member)
    else:
        for mention in args:
            member_id = re.sub('[<@>]', '', mention)
            member = await client.get_user_info(member_id)
            if member is None:
                await client.say("The user with ID " + member_id + " could not be accessed.")
                continue
            else:
                members.append(member)
    for member in members:
        if member not in (await client.get_bans(context.message.server)):
            await client.say(member.mention + " is not banned.")
            continue
        await client.unban(context.message.server, member)
        await client.say(member.mention + " has been unbanned from " +
                         context.message.server.name + ".")


@client.command(name='bitcoin',
                description='Display the current value of one bitcoin, based on internet data.',
                brief='Bitcoin price.',)
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    try:
        response = requests.get(url)
        value = response.json()['bpi']['USD']['rate']
        await client.say("Bitcoin price is: $" + value + ".")
    except:
        await client.say("Error contacting server..")


@client.command(name='asr',
                description='Add a role to the list of self-assignable roles.',
                brief='Add a self-assignable role.',
                pass_context=True,)
async def asr(context):
    is_admin = check_admin(context.message)
    if not is_admin:
        await client.say("You do not have permissions to use this command.")
        return
    global SETTINGS_DATA
    server = context.message.server
    try:
        rolenames = parse_arguments(context.message)
        for rolename in rolenames:
            if not discord.utils.get(server.roles, name=rolename):
                await client.say("There is no such role" + ", " + context.message.author.mention + ".")
                continue
            if rolename in SETTINGS_DATA[server.id]["assignable-roles"]:
                await client.say("The role " + rolename + " is already on the list of self-assignable roles.")
                continue
            await client.say("The role " + rolename + " was added to the list of self-assignable roles.")
            SETTINGS_DATA[server.id]["assignable-roles"].append(rolename)
    except:
        await client.say("Error adding role.")

    save_data(SETTINGS_DATA)


@client.command(name='rsr',
                description='Remove a role from the list of self-assignable roles.',
                brief='Remove a self-assignable role.',
                pass_context=True,)
async def rsr(context):
    is_admin = check_admin(context.message)
    if not is_admin:
        await client.say("You do not have permissions to use this command.")
        return
    global SETTINGS_DATA
    server = context.message.server
    try:
        rolenames = parse_arguments(context.message)
        for rolename in rolenames:
            if not discord.utils.get(server.roles, name=rolename):
                await client.say("There is no such role" + ", " + context.message.author.mention + ".")
                continue
            if rolename not in SETTINGS_DATA[server.id]["assignable-roles"]:
                await client.say("The role " + rolename + " is already not on the list of self-assignable roles.")
                continue
            SETTINGS_DATA[server.id]["assignable-roles"].remove(rolename)
            await client.say("The role " + rolename + " was removed from the list of self-assignable roles.")
    except:
        await client.say("Error removing role.")

    save_data(SETTINGS_DATA)


@client.command(name='addwarnword',
                description='Add a word/saying that will give a warning to users.',
                brief='Add a warning worthy word.',
                pass_context=True,)
async def addwarnword(context):
    is_admin = check_admin(context.message)
    if not is_admin:
        await client.say("You do not have permissions to use this command.")
        return
    global SETTINGS_DATA
    server = context.message.server
    try:
        words = parse_arguments(context.message)
        for word in words:
            if word in SETTINGS_DATA[server.id]["warn-words"]:
                await client.say(word + " is already on the list of warn words.")
                continue
            await client.say(word + " was added to the list of warn words.")
            SETTINGS_DATA[server.id]["warn-words"].append(word)
    except:
        await client.say("Error adding word")

    save_data(SETTINGS_DATA)


@client.command(name='removewarnword',
                description='Remove a word/saying that will give a warning to users.',
                brief='Remove a warning worthy word.',
                pass_context=True,)
async def removewarnword(context):
    is_admin = check_admin(context.message)
    if not is_admin:
        await client.say("You do not have permissions to use this command.")
        return
    global SETTINGS_DATA
    server = context.message.server
    try:
        words = parse_arguments(context.message)
        for word in words:
            if word not in SETTINGS_DATA[server.id]["warn-words"]:
                await client.say(word + " is already not on the list of warn words.")
                continue
            await client.say(word + " was removed the list of warn words.")
            SETTINGS_DATA[server.id]["warn-words"].remove(word)
    except:
        await client.say("Error removing word.")

    save_data(SETTINGS_DATA)


@client.command(name='welcomemsg',
                description='Add a welcome message for new members.',
                brief='Add a welcome message.',
                pass_context=True,)
async def welcomemsg(context):
    is_admin = check_admin(context.message)
    if not is_admin:
        await client.say("You do not have permissions to use this command.")
        return
    global SETTINGS_DATA
    member = context.message.author
    welcome_message = context.message.content.split(" ", 1)[1]
    SETTINGS_DATA[member.server.id]["welcome-message"] = welcome_message
    save_data(SETTINGS_DATA)
    await client.say("The welcome message has been changed to:\n" +
                     "" + welcome_message + "")


@client.command(name='setwelcomechannel',
                description='Choose the channel where welcome messages are displayed.',
                brief='Choose the welcome channel.',
                pass_context=True,)
async def setwelcomechannel(context):
    is_admin = check_admin(context.message)
    if not is_admin:
        await client.say("You do not have permissions to use this command.")
        return
    if not context.message.channel_mentions:
        await client.say("No channel was specified, mention a channel : #channelname.")
        return
    elif len(context.message.channel_mentions) > 1:
        await client.say("Multiple channels specified, the first channel on the list, " +
                         context.message.channel_mentions[0].mention + ", will be the one set as welcome channel.")
    else:
        await client.say("The channel " + context.message.channel_mentions[0].mention +
                         " will be the one set as welcome channel.")

    SETTINGS_DATA[context.message.server.id]["welcome-channel"] = context.message.channel_mentions[0].id
    save_data(SETTINGS_DATA)


@client.command(name='setserverinfo',
                description='Add a server info message.',
                brief='Add server info.',
                pass_context=True,)
async def setserverinfo(context):
    is_admin = check_admin(context.message)
    if not is_admin:
        await client.say("You do not have permissions to use this command.")
        return
    global SETTINGS_DATA
    member = context.message.author
    if not " " in context.message.content:
        return
    server_info = context.message.content.split(" ", 1)[1]
    SETTINGS_DATA[member.server.id]["server-info"] = server_info
    save_data(SETTINGS_DATA)
    await client.say("The server info message has been changed to:\n\n" +
                     "```" + server_info + "```")


@client.command(name='serverinfo',
                description='Display server info message.',
                brief='Display server info.',
                pass_context=True,)
async def serverinfo(context):
    member = context.message.author
    if not SETTINGS_DATA[member.server.id]["server-info"]:
        await client.say("The server info message for this server has not been set.")
        return
    await client.say(SETTINGS_DATA[member.server.id]["server-info"]
                     .replace("@user", context.message.author.mention))



@client.command(name='setchannelinfo',
                description='Add a channel info message.',
                brief='Add channel info.',
                pass_context=True,)
async def setchannelinfo(context):
    is_admin = check_admin(context.message)
    if not is_admin:
        await client.say("You do not have permissions to use this command.")
        return
    global SETTINGS_DATA
    member = context.message.author
    if not SETTINGS_DATA[member.server.id]["channel-info"]:
        SETTINGS_DATA[member.server.id]["channel-info"] = {}
        save_data(SETTINGS_DATA)
    channel_info = context.message.content.split(" ", 1)[1]
    SETTINGS_DATA[member.server.id]["channel-info"][context.message.channel.id] = channel_info
    save_data(SETTINGS_DATA)
    await client.say("The channel info message for" + " has been changed to:\n\n" +
                     "```" + channel_info + "```")


@client.command(name='channelinfo',
                description='Display server info message.',
                brief='Display server info.',
                pass_context=True,)
async def channelinfo(context):
    member = context.message.author
    if context.message.channel.id not in SETTINGS_DATA[member.server.id]["channel-info"] \
            or not SETTINGS_DATA[member.server.id]["channel-info"][context.message.channel.id]:
        await client.say("The channel info message for this channel has not been set.")
        return
    await client.say(SETTINGS_DATA[member.server.id]["channel-info"][context.message.channel.id]
                     .replace("@user", context.message.author.mention))



@client.command(name='setnegreact',
                description='Set negative reaction when bot is mentioned.',
                brief="Set bot's negative reaction.",
                pass_context=True,)
async def setnegreact(context):
    is_admin = check_admin(context.message)
    if not is_admin:
        await client.say("You do not have permissions to use this command.")
        return
    words = parse_arguments(context.message)
    checked_acquire_setting_dict(context.message.server.id, "neg-react")
    SETTINGS_DATA[context.message.server.id]["neg-react"] = []
    for word in words:
        for char in word:
            if char_is_emoji(char):
                if char in SETTINGS_DATA[context.message.server.id]["neg-react"]:
                    continue
                SETTINGS_DATA[context.message.server.id]["neg-react"].append(char)
                await client.add_reaction(context.message, word)
    save_data(SETTINGS_DATA)


@client.command(name='setposreact',
                description='Set positive reaction when bot is mentioned.',
                brief="Set bot's positive reaction.",
                pass_context=True,)
async def setnegreact(context):
    is_admin = check_admin(context.message)
    if not is_admin:
        await client.say("You do not have permissions to use this command.")
        return
    words = parse_arguments(context.message)
    checked_acquire_setting_dict(context.message.server.id, "pos-react")
    SETTINGS_DATA[context.message.server.id]["pos-react"] = []
    for word in words:
        for char in word:
            if char_is_emoji(char):
                if char in SETTINGS_DATA[context.message.server.id]["pos-react"]:
                    continue
                SETTINGS_DATA[context.message.server.id]["pos-react"].append(char)
                await client.add_reaction(context.message, word)
    save_data(SETTINGS_DATA)


@client.command(name='kick',
                description='Kick a user from the server.',
                brief='Kick a user out.',
                pass_context=True,)
async def kick(context, *args):
    is_admin = check_admin(context.message)
    if not is_admin:
        await client.say("You do not have permissions to use this command.")
        return
    for target in args:
        user_id = re.sub('[<@>]', '', target)
        member = context.message.server.get_member(user_id)
        if member is None:
            await client.say("Could not access user " + target + ".")
            continue
        await client.kick(member)
        await client.say(member.mention + " has been kicked from " + context.message.server.name + ".")


@client.command(name='textmute',
                description='Mute a user from typing. Their messages are deleted.',
                brief='Mute someone from text chat.',
                pass_context=True,)
async def textmute(context, *args):
    is_admin = check_admin(context.message)
    if not is_admin:
        await client.say("You do not have permissions to use this command.")
        return
    for target in args:
        user_id = re.sub('[<@>]', '', target)
        member = context.message.server.get_member(user_id)

        if checked_acquire_setting_dict(context.message.server.id, "textmuted-users") is None:
            SETTINGS_DATA[context.message.server.id]["textmuted-users"] = []
        if user_id not in SETTINGS_DATA[context.message.server.id]["textmuted-users"]:
            SETTINGS_DATA[context.message.server.id]["textmuted-users"].append(user_id)
            save_data(SETTINGS_DATA)
        else:
            await client.say('{} is already muted.'.format(member.mention))
            continue
        await client.say('{} has been text muted.'.format(member.mention))


@client.command(name='textunmute',
                description='Unmute a user from typing. Their messages are no longer deleted.',
                brief='Unmute someone from text chat.',
                pass_context=True,)
async def textunmute(context, *args):
    is_admin = check_admin(context.message)
    if not is_admin:
        await client.say("You do not have permissions to use this command.")
        return
    for target in args:
        user_id = re.sub('[<@>]', '', target)
        member = context.message.server.get_member(user_id)

        if checked_acquire_setting_dict(context.message.server.id, "textmuted-users") is None:
            SETTINGS_DATA[context.message.server.id]["textmuted-users"] = []
        if user_id in SETTINGS_DATA[context.message.server.id]["textmuted-users"]:
            SETTINGS_DATA[context.message.server.id]["textmuted-users"].remove(user_id)
            save_data(SETTINGS_DATA)
        else:
            await client.say('{} is not muted.'.format(member.mention))
            continue
        await client.say('{} has been text unmuted.'.format(member.mention))


@client.command(name='voicemute',
                description='Mute  a user from talking on voice channels.',
                brief='Mute someone from voice.',
                pass_context=True,)
async def voicemute(context, *args):
    is_admin = check_admin(context.message)
    if not is_admin:
        await client.say("You do not have permissions to use this command.")
        return
    for target in args:
        user_id = re.sub('[<@>]', '', target)
        member = context.message.server.get_member(user_id)
        await client.server_voice_state(member, mute=True)
        await client.say('{} has been voice muted.'.format(member.mention))


@client.command(name='voicunmute',
                description='Unmute a user from talking on voice channels.',
                brief='Unmute someone from voice.',
                pass_context=True,)
async def voiceunmute(context, *args):
    is_admin = check_admin(context.message)
    if not is_admin:
        await client.say("You do not have permissions to use this command.")
        return
    for target in args:
        user_id = re.sub('[<@>]', '', target)
        member = context.message.server.get_member(user_id)
        await client.server_voice_state(member, mute=False)
        await client.say('{} has been voice unmuted.'.format(member.mention))


@client.command(name='fullmute',
                description='Mute a user from both voice chat and typing.',
                brief='Mute someone.',
                pass_context=True,)
async def fullmute(context, target: str):
    is_admin = check_admin(context.message)
    if not is_admin:
        await client.say("You do not have permissions to use this command.")
        return
    await textmute(context, target)
    await voicemute(context, target)


@client.command(name='fullunmute',
                description='Mute a user from typing for a specified amount of time. Their messages are deleted.',
                brief='Mute someone.',
                pass_context=True,)
async def fullunmute(context, target: str):
    is_admin = check_admin(context.message)
    if not is_admin:
        await client.say("You do not have permissions to use this command.")
        return
    await textunmute(context, target)
    await voiceunmute(context, target)


@client.command(name='dangerwords',
                description='List of words than can get you in trouble.',
                brief='Words you should avoid.',
                pass_context=True,)
async def dangerwords(context):
    msg = "These words will lead to a warning:\n\n"
    if SETTINGS_DATA[context.message.server.id]["warn-words"] is None:
        SETTINGS_DATA[context.message.server.id]["warn-words"] = []
    if not SETTINGS_DATA[context.message.server.id]["warn-words"]:
        msg += "None\n"
    for warn_word in SETTINGS_DATA[context.message.server.id]["warn-words"]:
        msg += warn_word + "\n"
    msg = "```" + msg + "```"
    await client.say(msg)


@client.command(name='ping',
                description='Ping pong.',
                brief='Boop.',)
async def ping():
    await client.say("Pong!")


@client.command(name='test',
                description='test',
                brief='test',
                pass_context=True,)
async def test(context, *args):
    member = context.message.author


@client.command(name='link',
                description='Provide link to invite the bot.',
                brief='Invite link for the bot.',
                pass_context=True,)
async def link(context):
    await client.\
        say("https://discordapp.com/api/oauth2/authorize?client_id=433250671521693703&permissions=2146958583&scope=bot")


@client.event
async def on_ready():
    global SETTINGS_DATA
    SETTINGS_DATA = load_data()
    settings_init()
    print('Logged in as:')
    print(client.user.name)
    print(client.user.id)
    print('------')

    await client.change_presence(game=Game(name=random.choice(user_data["games"])))


@client.event
async def on_server_join(server):
    if server.id not in SETTINGS_DATA.keys():
        SETTINGS_DATA[server.id] = {}
        for setting in SETTINGS_CATEGORIES:
            SETTINGS_DATA[server.id][setting] = []
        save_data(SETTINGS_DATA)


@client.event
async def on_member_join(member):
    if SETTINGS_DATA[member.server.id]["welcome-message"]:
        msg = SETTINGS_DATA[member.server.id]["welcome-message"].replace("@user", member.mention)\
            .replace("!user", member.name)
        welcome_channel_id = SETTINGS_DATA[member.server.id]["welcome-channel"]
        server = member.server
        await client.send_message((server.get_channel(welcome_channel_id)), msg)


@client.event
async def on_message(message):
    bot_id = client.user.id

    if checked_acquire_setting_dict(message.server.id, "textmuted-users") is not None:
        if message.author.id in checked_acquire_setting_dict(message.server.id, "textmuted-users"):
            await client.delete_message(message)
            return

    if message.content == "Ping!":
        msg = "Pong!"
        await client.send_message(message.channel, msg)

    message_content_lower = message.content.lower()
    for warn_word in SETTINGS_DATA[message.server.id]["warn-words"]:
        if re.search(warn_word, message_content_lower):
            msg = "Careful with those words " + message.author.mention + "."
            await client.send_message(message.channel, msg)
            break

    if bot_id in message.raw_mentions:
        if TextBlob(message.content).sentiment[0] >= 0:
            if SETTINGS_DATA[message.server.id]["pos-react"] is None:
                SETTINGS_DATA[message.server.id]["pos-react"] = []
            for emoji in SETTINGS_DATA[message.server.id]["pos-react"]:
                await client.add_reaction(message, emoji)
        else:
            if SETTINGS_DATA[message.server.id]["neg-react"] is None:
                SETTINGS_DATA[message.server.id]["neg-react"] = []
            for emoji in SETTINGS_DATA[message.server.id]["neg-react"]:
                await client.add_reaction(message, emoji)
    await client.process_commands(message)


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print("\t" + server.name)

        await asyncio.sleep(120)
        await client.change_presence(game=Game(name=random.choice(user_data["games"])))


def check_admin(message):
    author = message.author
    author_permissions = author.permissions_in(message.channel)

    return author_permissions.administrator


async def check_admin_plus(message):
    is_admin = check_admin(message)
    if not is_admin:
        await client.say("You do not have permissions to use this command.")


def checked_acquire_setting_dict(server_id, setting_category):
    if setting_category not in SETTINGS_DATA[server_id].keys() and setting_category in SETTINGS_CATEGORIES:
        SETTINGS_DATA[server_id][setting_category] = None
        save_data(SETTINGS_DATA)
        return SETTINGS_DATA[server_id][setting_category]
    return SETTINGS_DATA[server_id][setting_category]


def settings_init():
    global SETTINGS_DATA
    for server in client.servers:
        if server.id not in SETTINGS_DATA.keys():
            SETTINGS_DATA[server.id] = {}
            for setting in SETTINGS_CATEGORIES:
                SETTINGS_DATA[server.id][setting] = []
            save_data(SETTINGS_DATA)


def parse_arguments(message):
    if not " " in message.content:
        return []
    arguments_string = message.content.split(" ", 1)[1]
    arguments_list = arguments_string.split(" ")
    return arguments_list


def char_is_emoji(character):
    return character in emoji.UNICODE_EMOJI


def text_has_emoji(text):
    for character in text:
        if character in emoji.UNICODE_EMOJI:
            return True
    return False


if __name__ == "__main__":
    print("started \n")
    client.loop.create_task(list_servers())
    client.run(TOKEN)