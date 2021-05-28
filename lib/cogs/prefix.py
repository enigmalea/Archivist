
# //          Copyright Amber Whitlock aka enigmalea 2021
# // Distributed under the Boost Software License, Version 1.0.
# //    (See accompanying file LICENSE_1_0.txt or copy at
# //          https://www.boost.org/LICENSE_1_0.txt)

from discord.ext import commands
from discord.ext.commands import Cog, has_permissions, cooldown

from ..db import db


class prefix(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('prefix')

    @commands.group(name="prefix", aliases=["pre"],
                    brief="Shows or sets prefix depending on the subcommand.")
    @commands.guild_only()
    async def pre(self, ctx):
        """
        Shows or sets prefix depending on the subcommand.\n\n*Requires a \
subcommand:*\n▸`<p>prefix set`: set a new prefix\n▸`<p>prefix show`: see the \
current prefix
        """
        msg = "This command requires a subcommand. Please use `<p>prefix set` to \
set a new prefix or `<p>prefix show` to see the current prefix."

        if ctx.invoked_subcommand is None:
            await ctx.send(msg)

    @pre.command(name="set", brief="Sets a new prefix")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def change_prefix(self, ctx, new_prefix: str):
        """Sets a new prefix for the bot.

        __**ɴᴏᴛᴇ:**__ You must have **Manage Server** permissions to use this command."""  # noqa

        if len(new_prefix) > 3:
            await ctx.send("Please select a shorter prefix. The prefix cannot be more than three characters in length.")  # noqa

        else:
            db.execute("UPDATE settings SET Prefix = ? WHERE GuildID = ?", new_prefix, ctx.guild.id)  # noqa
            await ctx.send(f"Prefix has been set to `{new_prefix}`.")

    @pre.command(name="show", brief="Shows the server's prefix")
    @commands.guild_only()
    async def show_prefix(self, ctx):
        pre = db.field("SELECT Prefix FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        await ctx.send(f"Current prefix is `{pre}`.")


def setup(bot):
    bot.add_cog(prefix(bot))
