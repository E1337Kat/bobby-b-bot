# Standard library imports
import sys
import os
import logging
from logging.config import fileConfig
import argparse
import json

# Third party imports
import discord

# Path hack
sys.path.insert(0, os.path.abspath('..'))

# Local application imports
from utils.core import get_random_quote, is_keyword_mentioned, generate_message_response # bot standard functions

# validate all mandatory files exist before starting
assert os.path.isfile('../utils/logging_config.ini') # Logs config file
response_config = dict()

# Instantiate logging in accordance with config file
fileConfig('../utils/logging_config.ini')
logger = logging.getLogger('discord')

# Explicit start of the bot runtime
logger.info("Started Discord bot")
try:
    # Instatiate Discord client
    client = discord.Client()
    logger.info("Instantiated Discord client")
except Exception as e:
    logger.exception("Error while instantiating Discord client: {}".format(str(vars(e))))

@client.event
async def on_message(message):
    # Do not reply to comments from these users, including itself (client.user)
    blocked_users = [ client.user ] 

    if message.author not in blocked_users:
        # Check for mentions first. 
        if client.user.mentioned_in(message):
            logger.info("Replied to message of user '{}' in guild '{}' / channel '{}'".format(message.author, message.guild, message.channel))
            msg = get_random_quote(response_config.get("MENTIONS", [])).format(message)
            await message.channel.send(msg)
        else:
            # Try to find a suitable response from all the possible message based triggers
            response = generate_message_response(message.content, response_config.get("MESSAGES", []))
            if response is not None:
                logger.info("Replied to message of user '{}' in guild '{}' / channel '{}'".format(message.author, message.guild, message.channel))
                msg = response.format(message)
                await message.channel.send(msg)
        
@client.event
async def on_guild_join(server):
    logger.info("Bot added to server '{}'".format(server.name))
    logger.info("Bot currently running on {} guild(s)".format(len(client.guilds)))
    
@client.event
async def on_ready():
    logger.info("Logged in as '{}', client ID '{}'". format(client.user.name, client.user.id))
    logger.info("Bot currently running on {} guild(s)".format(len(client.guilds)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=str, help="Configuration file containing triggers and responses which define bot behavior")
    parser.add_argument("token", type=str, help="Discord bot token, or a file containing it.")
    args = parser.parse_args()
    
    # Check to see if a file was provided, rather than a token string
    if os.path.isfile(args.token):
        with open(args.token) as tokenfile:
            token = tokenfile.read().strip()
    else:
        # We didn't get a valid file, assume we were provided a token directly
        token = args.token

    with open(args.config) as config:
        response_config.update(json.load(config))
    try:
        # Run Discord bot
        client.run(token)
        logger.info("Started Discord client")
    except Exception as e:
        logger.exception("Error while running Discord client: {}".format(str(vars(e))))
