""" Common functions """

# Standard library imports
import re
import random

def get_random_item(choices):
    """ Returns random quote from list of choices, or None if provided no options. """
    if choices:
        return random.choice(choices)
    return None
    
def is_keyword_mentioned(text, triggers):
    """ Checks if configured trigger words to call the bot are present in the text content """
     
    for keyword in triggers:
        # Do a case insensitive search. This should work on regex patterns as well.
        if re.search(keyword, text, re.IGNORECASE):
            return True
    
    return False

def get_trigger_from_content(content, messages_config):
    """ Searches message content and returns a specific trigger configuration if one is found, as defined in the provided config """

    # Check each trigger->action pair
    for config in messages_config:
        if is_keyword_mentioned(content, config.get("TRIGGERS", [])):
            return config
    return None


def get_username(author):
    """ Handles author names when comment was deleted before the bot could reply """

    if not author:
        name = '[deleted]'
    else:
        name = author.name

    return name
