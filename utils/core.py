""" Bot common functions """

# Standard library imports
import re
import random
import json
import os
from os.path import join, dirname

# Third party imports
from dotenv import load_dotenv

def get_env(env_key, filepath):
    """ Get environment variables """
    
    # Create .env file path
    dotenv_path = join(dirname(filepath), '.env')
    # Load file from the path
    load_dotenv(dotenv_path)
    
    # Accessing variables
    try: 
        return os.getenv(env_key)
    except Exception as e:
        return e
    
def get_random_quote(responses):
    """ Returns random quote from list of responses"""
    return random.choice(responses)
    
def is_keyword_mentioned(text, triggers):
    """ Checks if configured trigger words to call the bot are present in the message content """
     
    for keyword in triggers:
        # Do a case insensitive search. This should work on regex patterns as well.
        if re.search(keyword, text, re.IGNORECASE):
            return True
    
    return False

def generate_message_response(text, messages_config):
    """ Searches message content and returns a triggered response, if one is needed """

    # Check each trigger->response pair
    for config in messages_config:
        if is_keyword_mentioned(text, config.get("triggers", [])):
            return get_random_quote(config.get("responses", []))
    return None

def get_username(author):
    """ Handles author names when comment was deleted before the bot could reply """

    if not author:
        name = '[deleted]'
    else:
    	name = author.name

    return name