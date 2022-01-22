
# //          Copyright Amber Whitlock aka enigmalea 2021
# // Distributed under the Boost Software License, Version 1.0.
# //    (See accompanying file LICENSE_1_0.txt or copy at
# //          https://www.boost.org/LICENSE_1_0.txt)

# requires pip install disputils
import typing
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import Cog, has_permissions, cooldown

from ..db import db


class redirect(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('redirect')

    @commands.group(name="redirect", aliases=["red"],
                    brief="Allows you to redirect certain messages to a set channel.")
    @commands.guild_only()
    async def myset(self, ctx):
        """
        Shows, sets, updates, or clears the settings to redirect embeds to \
        specific channels depending on the subcommand. For a full list of \
        current redirects and subcommands use `<p>redirect show`.
        """
        msg = "This command requires a subcommand. For a full list of current \
redirects and subcommands use `< p > redirect show`."

        if ctx.invoked_subcommand is None:
            await ctx.send(msg)

    @myset.command(name="all")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def redirect_all(self, ctx, channel: typing.Union[discord.TextChannel, discord.Thread]):
        """Sets or updates the redirect for all embeds."""

        db.execute("UPDATE settings SET redFic = ? WHERE GuildID = ?",
                   channel.id, ctx.guild.id)
        db.execute("UPDATE settings SET redCh = ? WHERE GuildID = ?",
                   channel.id, ctx.guild.id)
        db.execute("UPDATE settings SET redSer = ? WHERE GuildID = ?",
                   channel.id, ctx.guild.id)
        db.execute("UPDATE settings SET redUse = ? WHERE GuildID = ?",
                   channel.id, ctx.guild.id)
        await ctx.send(f"All embeds will be sent to {channel.mention}.")

    @myset.command(name="allclear")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def all_clear(self, ctx):
        """Removes the redirect so embeds are posted in the same channel as the link. (Default)"""

        clear = ""

        db.execute("UPDATE settings SET redFic = ? WHERE GuildID = ?",
                   clear, ctx.guild.id)
        db.execute("UPDATE settings SET redCh = ? WHERE GuildID = ?",
                   clear, ctx.guild.id)
        db.execute("UPDATE settings SET redSer = ? WHERE GuildID = ?",
                   clear, ctx.guild.id)
        db.execute("UPDATE settings SET redUse = ? WHERE GuildID = ?",
                   clear, ctx.guild.id)
        await ctx.send("Embeds will no longer be redirected.")

    @myset.command(name="fic")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def redirect_fic(self, ctx, channel: typing.Union[discord.TextChannel, discord.Thread]):
        """Sets or updates the redirect for fic embeds."""

        allembed = " Would you like to set chapter, series, and user embed to redirect to the same channel? Please answer yes or no."
        def check(m): return m.author == ctx.author and m.channel == ctx.channel

        db.execute("UPDATE settings SET redFic = ? WHERE GuildID = ?",
                   channel.id, ctx.guild.id)
        await ctx.send(f"Fic embeds will be sent to {channel.mention}." + allembed)

        try:
            confirm = await self.bot.wait_for("message", check=check, timeout=15.0)
        except asyncio.TimeoutError:
            await ctx.send("Timed out. Other embeds will not be redirected.")
            return

        if confirm.content == "yes":
            db.execute("UPDATE settings SET redCh = ? WHERE GuildID = ?",
                       channel.id, ctx.guild.id)
            db.execute(
                "UPDATE settings SET redSer = ? WHERE GuildID = ?", channel.id, ctx.guild.id)
            db.execute(
                "UPDATE settings SET redUse = ? WHERE GuildID = ?", channel.id, ctx.guild.id)
            await ctx.send(f"Chapter, series, and user embeds will be redirected to {channel.mention}.")
            return
        else:
            await ctx.send("Other embeds will not be redirected.")
            return

    @myset.command(name="ficclear")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def fic_clear(self, ctx):
        """Removes the redirect so fic embeds are posted in the same channel as the link. (Default)"""

        clear = ""

        db.execute("UPDATE settings SET redFic = ? WHERE GuildID = ?",
                   clear, ctx.guild.id)
        await ctx.send("Fic embeds will no longer be redirected.")

    @myset.command(name="ch")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def redirect_ch(self, ctx, channel: typing.Union[discord.TextChannel, discord.Thread]):
        """Sets or updates the redirect for chapter embeds."""

        allembed = " Would you like to set fic, series, and user embed to redirect to the same channel? Please answer yes or no."
        def check(m): return m.author == ctx.author and m.channel == ctx.channel

        db.execute("UPDATE settings SET redCh = ? WHERE GuildID = ?",
                   channel.id, ctx.guild.id)
        await ctx.send(f"Chapter embeds will be sent to {channel.mention}." + allembed)

        try:
            confirm = await self.bot.wait_for("message", check=check, timeout=15.0)
        except asyncio.TimeoutError:
            await ctx.send("Timed out. Other embeds will not be redirected.")
            return

        if confirm.content == "yes":
            db.execute("UPDATE settings SET redFic = ? WHERE GuildID = ?",
                       channel.id, ctx.guild.id)
            db.execute(
                "UPDATE settings SET redSer = ? WHERE GuildID = ?", channel.id, ctx.guild.id)
            db.execute(
                "UPDATE settings SET redUse = ? WHERE GuildID = ?", channel.id, ctx.guild.id)
            await ctx.send(f"Fic, series, and user embeds will be redirected to {channel.mention}.")
            return
        else:
            await ctx.send("Other embeds will not be redirected.")
            return

    @myset.command(name="chclear")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def ch_clear(self, ctx):
        """Removes the redirect so chapter embeds are posted in the same channel as the link. (Default)"""

        clear = ""

        db.execute("UPDATE settings SET redCh = ? WHERE GuildID = ?",
                   clear, ctx.guild.id)
        await ctx.send("Chapter embeds will no longer be redirected.")

    @myset.command(name="ser")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def redirect_ser(self, ctx, channel: typing.Union[discord.TextChannel, discord.Thread]):
        """Sets or updates the redirect for series embeds."""

        allembed = " Would you like to set fic, chapter, and user embed to redirect to the same channel? Please answer yes or no."
        def check(m): return m.author == ctx.author and m.channel == ctx.channel

        db.execute("UPDATE settings SET redSer = ? WHERE GuildID = ?",
                   channel.id, ctx.guild.id)
        await ctx.send(f"Series embeds will be sent to {channel.mention}." + allembed)

        try:
            confirm = await self.bot.wait_for("message", check=check, timeout=15.0)
        except asyncio.TimeoutError:
            await ctx.send("Timed out. Other embeds will not be redirected.")
            return

        if confirm.content == "yes":
            db.execute("UPDATE settings SET redCh = ? WHERE GuildID = ?",
                       channel.id, ctx.guild.id)
            db.execute(
                "UPDATE settings SET redFic = ? WHERE GuildID = ?", channel.id, ctx.guild.id)
            db.execute(
                "UPDATE settings SET redUse = ? WHERE GuildID = ?", channel.id, ctx.guild.id)
            await ctx.send(f"Fic, chapter, and user embeds will be redirected to {channel.mention}.")
            return
        else:
            await ctx.send("Other embeds will not be redirected.")
            return

    @myset.command(name="serclear")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def ser_clear(self, ctx):
        """Removes the redirect so series embeds are posted in the same channel as the link. (Default)"""

        clear = ""

        db.execute("UPDATE settings SET redSer = ? WHERE GuildID = ?",
                   clear, ctx.guild.id)
        await ctx.send("Series embeds will no longer be redirected.")

    @myset.command(name="user")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def redirect_user(self, ctx, channel: typing.Union[discord.TextChannel, discord.Thread]):
        """Sets or updates the redirect for user embeds."""

        allembed = " Would you like to set fic, chapter, and series embeds to redirect to the same channel? Please answer yes or no."
        def check(m): return m.author == ctx.author and m.channel == ctx.channel

        db.execute("UPDATE settings SET redUse = ? WHERE GuildID = ?",
                   channel.id, ctx.guild.id)
        await ctx.send(f"User embeds will be sent to {channel.mention}." + allembed)

        try:
            confirm = await self.bot.wait_for("message", check=check, timeout=15.0)
        except asyncio.TimeoutError:
            await ctx.send("Timed out. Other embeds will not be redirected.")
            return

        if confirm.content == "yes":
            db.execute("UPDATE settings SET redCh = ? WHERE GuildID = ?",
                       channel.id, ctx.guild.id)
            db.execute(
                "UPDATE settings SET redSer = ? WHERE GuildID = ?", channel.id, ctx.guild.id)
            db.execute(
                "UPDATE settings SET redFic = ? WHERE GuildID = ?", channel.id, ctx.guild.id)
            await ctx.send(f"Fic, chapter, and series embeds will be redirected to {channel.mention}.")
            return
        else:
            await ctx.send("Other embeds will not be redirected.")
            return

    @myset.command(name="userclear")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def user_clear(self, ctx):
        """Removes the redirect so user embeds are posted in the same channel as the link. (Default)"""

        clear = ""

        db.execute("UPDATE settings SET redUse = ? WHERE GuildID = ?",
                   clear, ctx.guild.id)
        await ctx.send("User embeds will no longer be redirected.")

    @myset.command(name="show", aliases=["view"],
                   brief="Shows the server's redirect settings.")
    @commands.guild_only()
    async def show_settings(self, ctx):

        fic = db.field("SELECT redFic FROM settings WHERE GuildID = ?", ctx.guild.id)
        ch = db.field("SELECT redCh FROM settings WHERE GuildID = ?", ctx.guild.id)
        ser = db.field("SELECT redSer FROM settings WHERE GuildID = ?", ctx.guild.id)
        user = db.field("SELECT redUse FROM settings WHERE GuildID = ?", ctx.guild.id)

        if fic == "":
            ficdes = "No redirect. (Default)."
        else:
            ficdes = f"<#{fic}>"

        if ch == "":
            chdes = "No redirect. (Default)."
        else:
            chdes = f"<#{ch}>"

        if ser == "":
            serdes = "No redirect. (Default)."
        else:
            serdes = f"<#{ser}>"

        if user == "":
            userdes = "No redirect. (Default)."
        else:
            userdes = f"<#{user}>"

        embed = embedVar = discord.Embed(
            title="Current Redirects", color=0x2F3136)

        embedVar.add_field(name="Fic embeds sent to:",
                           value=ficdes,
                           inline=False)

        embedVar.add_field(name="Chapter embeds sent to:", value=chdes,
                           inline=False)

        embedVar.add_field(name="Series embeds sent to:",
                           value=serdes,
                           inline=False)

        embedVar.add_field(name="User embeds sent to:",
                           value=userdes,
                           inline=False)

        await ctx.send(embed=embedVar)


def setup(bot):
    bot.add_cog(redirect(bot))
