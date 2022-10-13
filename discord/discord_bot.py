# Standard library imports
import asyncio
import sys
import os
import logging
from logging.config import fileConfig
import argparse
import json
import threading
from typing import overload
from discord.message import Message
import emoji

# Third party imports
import discord

# Path hack
sys.path.insert(0, os.path.abspath('..'))

# Local application imports
from utils.core import is_keyword_mentioned, get_trigger_from_content, get_random_item, get_random_new_item # bot standard functions
from utils.scheduler import init_message_scheduler

# validate all mandatory files exist before starting
assert os.path.isfile('../utils/logging_config.ini') # Logs config file
response_config = dict()

# Instantiate logging in accordance with config file
fileConfig('../utils/logging_config.ini')
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)


# class BotConf:
#     def __init__(self, *, config_file=None, **options):
#         self.config_file = config_file

#     def fetch_token(self):
#         with open(self.config_file) as config:
#             response_config.update(json.load(config))
#             token = response_config.get("TOKEN", "TOKEN_HERE")
#             if token == "TOKEN_HERE":
#                 return

class LocalClient(discord.Client):
    def __init__(self, *, loop=None, **options):
        super().__init__(intents=discord.Intents.default())
        self.config_file = str()
        self.response_config = dict()

    def add_config(self, config_file):
        self.config_file = config_file

    def fetch_token(self) -> str:
        with open(self.config_file) as config:
            self.response_config.update(json.load(config))
            # logger.info("using config: " + str(client.response_config))
            token = self.response_config.get("TOKEN", "TOKEN_HERE")
            logger.info("using token: " + str(token))
            return token


# Explicit start of the bot runtime
logger.info("Started Discord bot")
try:
    # Instantiate Discord client
    
    client = LocalClient()
    logger.info("Instantiated Discord client")
except Exception as e:
    logger.exception("Error while instantiating Discord client: {}".format(str(vars(e))))

async def respond(message, response):
    """ Format a response to a message object and yield """
    logger.info("Replied to message of user '{}' in guild '{}' / channel '{}'".format(message.author, message.guild, message.channel))
    msg = response.format(message)
    await message.channel.send(msg)

global history

async def respond_from_triggers(message, content, triggers):
    """ Search message content according to provided triggers and yield the best response"""

    # Replace emoji unicode with the CLDR names so that we can properly trigger. 
    # This will safely translate only supported unicode, and leave the rest of the string intact.
    trigger = get_trigger_from_content(emoji.demojize(content, use_aliases=True), triggers)
    if trigger:
        # Try to get a quote and reaction from this trigger. We can do both
        quote = get_random_item(trigger.get("RESPONSES"))
        reaction = get_random_item(trigger.get("REACTIONS"))
        if quote:
            await respond(message, quote)
        if reaction:
            emote = emoji.emojize(reaction, use_aliases=True)
            if emote in emoji.UNICODE_EMOJI:
                await message.add_reaction(emote)

@client.event
async def on_message(message):
    # Do not reply to comments from these users, including itself (client.user)
    blocked_users = [ client.user ] 
    past = get_history()
    if message.author not in blocked_users:
        # Check for mentions first, otherwise respond to message content based triggers.
        if client.user.mentioned_in(message):
            response = get_random_new_item(client.response_config.get("MENTION_EVENTS", []), past)
            add_history(response)
            await respond(message, response)
        else:
            await respond_from_triggers(message, message.content, client.response_config.get("MESSAGE_EVENTS", []))

@client.event
async def on_reaction_add(reaction, user):
    # Do not listen to reactions from these users, including itself (client.user)
    blocked_users = [ client.user ] 
    
    if user not in blocked_users:
        content = emoji.demojize(reaction.emoji, use_aliases=True)
        await respond_from_triggers(reaction.message, content, client.response_config.get("REACTION_EVENTS", []))

@client.event
async def on_guild_join(server):
    logger.info("Bot added to guild '{}'".format(server.name))


@client.event
async def on_ready():
    logger.info("Logged in as '{}', client ID '{}'". format(client.user.name, client.user.id))
    logger.info("Bot currently running on {} guild(s)".format(len(client.guilds)))

    # Start the scheduler if there are scheduled jobs
    init_message_scheduler(response_config.get("SCHEDULE_EVENTS", {}), client)

def get_history() -> list:
    global history
    return history

def add_history(item: str):
    global history
    if len(history) < 50:
        history.insert(0, item)
    else:
        history.pop()
        add_history(item)

def main():
    global history

    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=str, help="Configuration file containing triggers and responses which define bot behavior")
    # parser.add_argument("config_folder", type=str, help="Folder containing Configuration file containing triggers and responses which define bot behavior")
    args = parser.parse_args()

    # running_bots = [{}]
    # fileList = os.listdir(args.config_folder)
    # logger.info("Found configs: " + str(fileList))
    # for file in fileList:
    #     logger.info("initializing bot for config: " + file)
    #     config = os.path.join(args.config_folder + file)
    #     client.add_config(config)
    #     token = client.fetch_token()
    #     logger.info("using token: " + token)
    #     if token == "TOKEN_HERE":
    #         raise "Need to add the token to the config!"
    #     try:
    #         # Run Discord bot
    #         loop = asyncio.get_event_loop()
    #         loop.run_until_complete(client.start(token))
    #         # thr = threading.Thread(target=client.start(token), args=(), kwargs={})
    #         running_bots.append({ file: loop })
    #         # thr.start()
    #         logger.info("Started Discord client")
    #     except Exception as e:
    #         logger.exception("Error while running Discord client: {}".format(str(vars(e))))

    client.add_config(args.config)

    history = []

    try:
        # Run Discord bot
        token = client.fetch_token()
        logger.info("using token: " + token)
        if token == "TOKEN_HERE":
            raise "Need to add the token to the config!"
        client.run(token)
        logger.info("Started Discord client")
    except Exception as e:
        logger.exception("Error while running Discord client: {}".format(str(vars(e))))

if __name__ == '__main__':
    main()
