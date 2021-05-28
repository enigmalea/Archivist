
# //          Copyright Amber Whitlock aka enigmalea 2021
# // Distributed under the Boost Software License, Version 1.0.
# //    (See accompanying file LICENSE_1_0.txt or copy at
# //          https://www.boost.org/LICENSE_1_0.txt)

from discord.ext import commands
from discord.ext.commands import Cog, has_permissions, cooldown

from ..db import db


class ignore(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('ignore')

    @commands.group(name="ignore", aliases=["ign"],
                    brief="Shows or sets ignore symbol depending on the subcommand.")  # noqa
    @commands.guild_only()
    async def ign(self, ctx):
        """
        Shows or sets ignore symbol depending on the subcommand.\n\n*Requires \
a subcommand:*\n▸`<p>ignore set`: set a new ignore symbol\n▸`<p>ignore show`: \
see the current ignore symbol
        """
        msg = "This command needs a subcommand. Please use `<p>ignore set` to \
set a new ignore symbol or `<p>ignore show` to see the current ignore symbol."

        if ctx.invoked_subcommand is None:
            await ctx.send(msg)

    @ign.command(name="set", brief="Sets a new ignore symbol")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def change_ignore(self, ctx, new_symbol: str):
        """Sets a custom symbol which tells the bot to ignore an AO3 link.

        __**ɴᴏᴛᴇ:**__ You must have **Manage Server** permissions to use this command."""  # noqa
        if len(new_symbol) > 3:
            await ctx.send("Please select a shorter ignore symbol. The ignore symbol cannot be \
more than three characters in length.")

        else:
            db.execute("UPDATE settings SET Ign = ? WHERE GuildID = ?", new_symbol, ctx.guild.id)  # noqa
            await ctx.send(f"Ignore symbol has been set to {new_symbol}.")

    @ign.command(name="show", brief="Shows the server's ignore symbol.")
    @commands.guild_only()
    async def show_ignore(self, ctx):
        ign = db.field("SELECT Ign FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        await ctx.send(f"Current ignore symbol is `{ign}`.")


def setup(bot):
    bot.add_cog(ignore(bot))
