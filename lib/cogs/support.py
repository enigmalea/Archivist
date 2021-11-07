
# //          Copyright Amber Whitlock aka enigmalea 2021
# // Distributed under the Boost Software License, Version 1.0.
# //    (See accompanying file LICENSE_1_0.txt or copy at
# //          https://www.boost.org/LICENSE_1_0.txt)

import discord

from discord.ext import commands
from discord.ext.commands import Cog, command


class support(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('support')

    @command(name="support", brief="Gives users ideas on how to support the bot.")  # noqa
    @commands.guild_only()
    async def support(self, ctx):
        """Want to help support **Archivist**? This command can tell you \
how!"""

        name = ctx.me.display_name
        title = f"Support {name}"
        user = ctx.message.author.mention
        desc = f"{user}, thank you for wanting to support \
the bot. Below you'll find some ideas for what you can do to help {name} grow!"

        Free = """**▸ [Follow on Twitter](https://twitter.com/_ArchivistBot_)**
\u279f Make sure to like and retweet **@\_ArchivistBot\_'s**  tweets.

**▸ [Join the Support Server](https://discord.gg/FzhC9bVFva)**
\u279f Have an idea for a feature or something you'd like to see? Join the \
Support Server to share it with the dev.

**▸ Vote and rate the bot on botlists**
\u279f [DiscordBotList](https://discordbotlist.com/bots/archivist)
\u279f [top.gg](https://top.gg/bot/812505952959856690)

**▸ Tell your friends**
\u279f Post about <:logo:848627809647329320> **Archivist** on tumblr, \
twitter, or other fandom spaces.
\u279f Ask mods to add <:logo:848627809647329320> **Archivist** to Discord \
servers you're in."""

        Paid = """__There are no premium or paid features to use \
<:logo:848627809647329320> **Archivist**.__ This is not a for profit project. \
However, if you would like to donate to help offset the cost of hosting or to \
just say thank you, feel free to visit my ko-fi.

<:kofi:848631801046892604> **[enigmalea](https://ko-fi.com/enigmalea)**"""

        embed = embedVar = discord.Embed(
            title=title, description=desc,
            color=0x2F3136)

        embedVar.add_field(name="\u2606 How to Support for Free \u2606",
                           value=Free, inline=False)

        embedVar.add_field(name="Paid Support Options", value=Paid,
                           inline=False)

        embed.set_footer(text=f"Thank you for using {name}!")

# sends embed
        await ctx.channel.send(embed=embedVar)


def setup(bot):
    bot.add_cog(support(bot))
