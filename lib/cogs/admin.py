
# //          Copyright Amber Whitlock aka enigmalea 2021
# // Distributed under the Boost Software License, Version 1.0.
# //    (See accompanying file LICENSE_1_0.txt or copy at
# //          https://www.boost.org/LICENSE_1_0.txt)

# ========== IMPORT MODULES ==========
import discord
import platform
import asyncio
import dbots

from discord.ext import commands
from discord.ext.commands import Cog, command
from glob import glob

COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]


class admin(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('admin')

    # Displays number of servers bot is in

    @command(name="admin", aliases=['serv'])
    @commands.is_owner()
    @commands.guild_only()
    async def _stats(self, ctx):
        """
        Shows bot stats for bot owner.
        """
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        guild = ctx.guild
        nservs = len(self.bot.guilds)
        name = guild.me.display_name

        pymsg = f"**{name}** is running *Python v{pythonVersion}* and"
        discmsg = f"*Discord.py v{dpyVersion}*."

        if nservs > 1:
            servs = f"**{name}** is in {nservs} servers."
        else:
            servs = f"**{name}** is in {nservs} server."

        msg = f"{pymsg} {discmsg} {servs}"

        await ctx.send(msg)

    @command(name="logout", aliases=['disconnect', 'close', 'stopbot'])
    @commands.is_owner()
    @commands.guild_only()
    async def logout(self, ctx):
        """
        Disconnects bot from Discord.
        """
        await ctx.send("**Archivist** is logging out.")
        await self.bot.logout()

    @command(name='reload', brief="Reloads cogs.")
    @commands.is_owner()
    @commands.guild_only()
    async def reload(self, ctx):
        """
        Reloads cogs when updates have been done.
        """
        global COGS
        async with ctx.typing():
            embed = discord.Embed(
                title="Reloading All Cogs",
                color=0x2F3136,
                timestamp=ctx.message.created_at
            )
            for cog in COGS:
                try:
                    self.bot.unload_extension(f"lib.cogs.{cog}")
                    self.bot.load_extension(f"lib.cogs.{cog}")
                    embed.add_field(
                        name=f"Reloaded: `{cog}`",
                        value='\uFeFF',
                        inline=False
                    )
                except Exception as e:
                    embed.add_field(
                        name=f"Failed to Reload: `{cog}`",
                        value=e,
                        inline=False
                    )

                await asyncio.sleep(0.5)

            await ctx.send(embed=embed)

    @command(name='ping', brief="pings the server")
    @commands.is_owner()
    @commands.guild_only()
    async def ping(self, ctx):
        """
        Pings, pings, and provides latency.
        """
        latency = round(self.bot.latency * 1000)
        msg = f"Pong! The server responded in {latency}ms."
        await ctx.send(msg)


def setup(bot):
    bot.add_cog(admin(bot))
