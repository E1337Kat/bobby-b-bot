from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.core import get_random_quote
import logging
from logging.config import fileConfig

fileConfig('../utils/logging_config.ini')
logger = logging.getLogger('discord')


def init_message_scheduler(config, client):

    jobs = config.get("SCHEDULES")
    if not jobs or not jobs[0]["MESSAGES"]:
        "No jobs found in provided config."
        return

    scheduler = AsyncIOScheduler()
    scheduler.start()

    async def send_scheduled_message(msg):
        for guild in client.guilds:
            for channel in guild.text_channels:
                try:
                    await channel.send(msg)
                except Exception as ex:
                    logger.debug('Channel {} ignored due to insufficient access permissions: {}', channel.name, ex)

    for job in jobs:
        scheduler.add_job(send_scheduled_message, args=[get_random_quote(job["MESSAGES"])], **job["ARGS"])
