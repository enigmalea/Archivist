
# //          Copyright Amber Whitlock aka enigmalea 2021
# // Distributed under the Boost Software License, Version 1.0.
# //    (See accompanying file LICENSE_1_0.txt or copy at
# //          https://www.boost.org/LICENSE_1_0.txt)

import discord
import logging
import time

from pytz import timezone
from asyncio import sleep
from discord import Intents
from pathlib import Path

import os
from dotenv import load_dotenv

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands
from discord.ext.commands import AutoShardedBot as BotBase
from discord.ext.commands import CommandNotFound, NoPrivateMessage, UserInputError
from discord.ext.commands import when_mentioned_or

from ..db import db


# ========== SETS UP LOGGING ===========
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# ========== DECLARES INTENTS ===========
intents = Intents.default()
intents.typing = False
intents.presences = False

# ========== LOADS TOKEN ===========
load_dotenv()
token = os.getenv("DISCORD_TOKEN")

COGS = [p.stem for p in Path(".").glob("./lib/cogs/*.py")]


def get_prefix(bot, message):
    if message.guild:
        prefix = db.field(
            "SELECT Prefix FROM settings WHERE GuildID = ?", message.guild.id)
        return when_mentioned_or(prefix)(bot, message)


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f" {cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.start_time = time.time()
        self.ready = False
        self.cogs_ready = Ready()

        self.scheduler = AsyncIOScheduler(
            timezone=timezone('America/New_York'))

        db.autosave(self.scheduler)
        super().__init__(
            command_prefix=get_prefix,
            case_insensitive=True,
            owner_ids=[508726665199747100, 398431412983824386],
            intents=intents,
            help_command=None,
            activity=discord.Activity(type=discord.ActivityType.watching,
                                      name="$help | archivistbot.com")
        )


    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")

    def update_db(self):
        guildids = []
        for guild in self.guilds:
            guildids.append(guild.id)

        db.multiexec("INSERT OR IGNORE INTO settings (GuildID) VALUES (?)",
                     ((guild.id,) for guild in self.guilds))

        to_remove = []
        stored_guilds = db.column("SELECT GuildID from settings")
        for GuildID in stored_guilds:
            if GuildID not in guildids:
                to_remove.append(GuildID)

        db.multiexec("DELETE FROM settings WHERE GuildID = ?",
                     ((GuildID,) for GuildID in to_remove))

        db.commit()

    def run(self, version):
        self.VERSION = version
        self.TOKEN = token

        self.setup()

        print("attempting to start bot...")
        print(' ')
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        self.update_db()
        print(f"successfully logged in as {bot.user.name}.")
        print(' ')

    async def on_disconnect(self):
        print("logged out.")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")

        raise

    async def on_command_error(self, ctx, exc):
        ignored = (CommandNotFound, UserInputError, NoPrivateMessage)
        if isinstance(exc, ignored):
            return

        if isinstance(exc, commands.CommandOnCooldown):
            m, s = divmod(exc.retry_after, 60)
            h, m = divmod(m, 60)
            if int(h) == 0 and int(m) == 0:
                await ctx.send(f"Command on cooldown. You must wait {int(s)} seconds to use this command. ")

        elif isinstance(exc, commands.CheckFailure):
            await ctx.send("You do not have the required permissions for this command.")

        elif hasattr(exc, "original"):
            raise exc.original

        else:
            raise exc

    async def on_guild_join(self, guild):
        db.multiexec("INSERT OR IGNORE INTO settings (GuildID) VALUES (?)",
                     ((guild.id,) for guild in self.guilds))

        db.commit()

    async def on_guild_remove(self, guild):
        guildids = []
        for guild in self.guilds:
            guildids.append(guild.id)

        to_remove = []
        stored_guilds = db.column("SELECT GuildID from settings")
        for GuildID in stored_guilds:
            if GuildID not in guildids:
                to_remove.append(GuildID)

        db.multiexec("DELETE FROM settings WHERE GuildID = ?",
                     ((GuildID,) for GuildID in to_remove))

        db.commit()

# ========== BOT STATUS ===========

    async def on_ready(self):
        if not self.ready:
            self.cogs_ready = Ready()
            self.scheduler.start()

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            self.ready = True
            print(" ")
            print("BOT READY!")

    async def on_message(self, message):
        if message.author == self.user and message.guild:
            return

        await bot.process_commands(message)


bot = Bot()
