__title__ = 'Discord Bot'
__author__ = 'Axmouth'
__license__ = 'GPL v2'
__copyright__ = 'Copyright 2018- Axmouth'
__version__ = '0.1.0'


import discord
from data_loader import load_user_data
#from discord.ext.commands import Bot

#TOKEN = '433250671521693703'
user_data = load_user_data()
TOKEN = user_data["token"]

client = discord.Client()
#my_bot = Bot(command_prefix="!")
#My_Bot = Bot()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    elif message.content.startswith('bitconnect'):
        msg = 'BITCONNEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEECT'
        await client.send_message(message.channel, msg)

    elif message.content.startswith("what's up"):
        msg = 'wasawasawasawasa'
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')



if __name__ == "__main__":
    print("started \n")
    #My_Bot.login(TOKEN)
client.run(TOKEN)