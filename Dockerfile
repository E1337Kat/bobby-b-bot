FROM python:3.7-slim-stretch

RUN apt-get -y update && apt-get -y install gcc

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip uninstall discord.py -y
RUN pip install discord.py
RUN python3 -m pip install -U discord.py

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY discord/ ./discord
COPY utils/ ./utils
COPY configs/ ./configs
COPY LICENSE .
COPY start.sh .

# CMD ["/bin/cd", "/discord", "&&" "python3", "discord_bot.py", "../configs/billybot.json"]
CMD ["./start.sh"]