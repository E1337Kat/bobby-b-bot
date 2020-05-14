# Standard library imports
import sys
import os
import logging
from logging.config import fileConfig
import argparse
import json
import emoji

# Third party imports
import discord

# Path hack
sys.path.insert(0, os.path.abspath('..'))

# Local application imports
from utils.core import is_keyword_mentioned, get_trigger_from_content, get_random_item # bot standard functions
from utils.scheduler import init_message_scheduler

# validate all mandatory files exist before starting
assert os.path.isfile('../utils/logging_config.ini') # Logs config file
response_config = dict()

# Instantiate logging in accordance with config file
fileConfig('../utils/logging_config.ini')
logger = logging.getLogger('discord')

# Explicit start of the bot runtime
logger.info("Started Discord bot")
try:
    # Instantiate Discord client
    client = discord.Client()
    logger.info("Instantiated Discord client")
except Exception as e:
    logger.exception("Error while instantiating Discord client: {}".format(str(vars(e))))

async def respond(message, response):
    """ Format a response to a message object and yield """
    logger.info("Replied to message of user '{}' in guild '{}' / channel '{}'".format(message.author, message.guild, message.channel))
    msg = response.format(message)
    await message.channel.send(msg)

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
    
    if message.author not in blocked_users:
        # Check for mentions first, otherwise respond to message content based triggers.
        if client.user.mentioned_in(message):
            await respond(message, get_random_item(response_config.get("MENTION_EVENTS", [])))
        else:
            await respond_from_triggers(message, message.content, response_config.get("MESSAGE_EVENTS", []))

@client.event
async def on_reaction_add(reaction, user):
    # Do not listen to reactions from these users, including itself (client.user)
    blocked_users = [ client.user ] 
    
    if user not in blocked_users:
        content = emoji.demojize(reaction.emoji, use_aliases=True)
        await respond_from_triggers(reaction.message, reaction.emoji, response_config.get("REACTION_EVENTS", []))

@client.event
async def on_guild_join(server):
    logger.info("Bot added to guild '{}'".format(server.name))


@client.event
async def on_ready():
    logger.info("Logged in as '{}', client ID '{}'". format(client.user.name, client.user.id))
    logger.info("Bot currently running on {} guild(s)".format(len(client.guilds)))

    # Start the scheduler if there are scheduled jobs
    init_message_scheduler(response_config.get("SCHEDULE_EVENTS", {}), client)


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
