from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.core import get_random_item
import logging
from logging.config import fileConfig

fileConfig('../utils/logging_config.ini')
logger = logging.getLogger('discord')

# Pass in a configuration and scheduled jobs will be added accordingly
def init_message_scheduler(jobs, client):

    if not jobs or not len(jobs) or not any(job.get("MESSAGES") for job in jobs):
        logger.info("No jobs found in provided config.")
        return

    scheduler = AsyncIOScheduler()
    scheduler.start()

    # Send a message to all channels for which the bot is allowed
    async def send_scheduled_message(msg):
        for guild in client.guilds:
            for channel in guild.text_channels:
                try:
                    await channel.send(msg)
                except Exception as ex:
                    logger.debug('Channel {} ignored due to insufficient access permissions: {}', channel.name, ex)

    for job in jobs:
        messages = job.get("MESSAGES")
        if messages:
            scheduler.add_job(send_scheduled_message,
                            args=[get_random_item(messages)],
                            **job.get("ARGS", dict())
                            )
