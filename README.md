# Trigger Happy Bot

**TODO: Agree on good bot name now that BobbyB has been abstracted**

This is a bot, based off of the popular Bobby B bot, with extended functionality which allows quick creation of new bot behaviors, and various types of triggers.

## Installation

```bash
$ python -m venv <venv_name>
$ cd <venv_name>
$ source bin/activate
(venv_name) $ git clone <repo>
(venv_name) $ cd discord
(venv_name) $ pip install -r requirements.txt
```

## Before you can run

1. Generate a token for your bot. Store it directly in a file, or simply save it for later.
2. Create and mantain a logging_config.ini file in utils folder for logging configuration ([see documentation](https://docs.python.org/3/library/logging.config.html#logging-config-fileformat));
3. [Create a configuration file](#creating-bot-configuration) to describe the bots behavior
4. Run the bot: (`python discord_bot.py --help` for usage)

## Creating Bot Configuration

The configuration file describes the bots behavior. Very different bots with various complexity can be created through this interface. The BobbyB bot behavior is reproduced through this interface, and the configuration file is available in configs/

There is also a sample file in configs/ which provide a template for all currently supported triggers and responses.

**TODO: Expand on this**

## Usage

```bash
usage: discord_bot.py [-h] config token

positional arguments:
  config      Configuration file containing triggers and responses which
              define bot behavior
  token       Discord bot token, or a file containing it.

optional arguments:
  -h, --help  show this help message and exit
```

It should be noted that the token can be passed in as ```python discord_bot.py ../configs/my-bot-config.json MY-DISCORD-TOKEN``` or ```MY-DISCORD-TOKEN``` can be saved in a file, and passed in directly as ```python discord_bot.py ../configs/my-bot-config.json tokens/my-bot.token```
