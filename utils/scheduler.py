from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.core import get_random_quote
import logging
import json

from logging.config import fileConfig

fileConfig('../utils/logging_config.ini')
logger = logging.getLogger('discord')


def init_message_scheduler(config, client, time_in_seconds):

    async def send_scheduled_messages():
        msg = get_random_quote(config.get("SCHEDULES")["RESPONSES"])
        for guild in client.guilds:
            for channel in guild.text_channels:
                try:
                    await channel.send(msg)
                except Exception as ex:
                    logger.info('Channel {} ignored due to insufficient access permissions: {}', channel.name, ex)

    sched = AsyncIOScheduler()
    sched.add_job(send_scheduled_messages, 'interval', seconds=time_in_seconds)
    sched.start()
