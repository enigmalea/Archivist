
# //          Copyright Amber Whitlock aka enigmalea 2021
# // Distributed under the Boost Software License, Version 1.0.
# //    (See accompanying file LICENSE_1_0.txt or copy at
# //          https://www.boost.org/LICENSE_1_0.txt)

# Requires pip install ao3_api
import discord
from discord.ext.commands import Cog
import re
import AO3

from ..db import db


class eventuser(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('eventuser')

    @Cog.listener()
    async def on_message(self, message):
        ctx = await self.bot.get_context(message)
        ign = db.field("SELECT Ign FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        igncheck = f"{ign}http"

        dellink = db.field("SELECT DelLink FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa

        if message.author == self.bot.user:
            return

        if ctx.command is None and igncheck not in message.content and\
                "https://archiveofourown.org/users/" in message.content:

            urls = re.findall(
                'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content.strip())  # noqa
            if urls:
                links = ''.join(urls)
                link = links.replace('>', '')

            if "pseuds" in link:
                sep = '/'
                userid = link.split(sep)[4]
                dname = link.split(sep)[6]
                displayname = dname.split()[0]
                user = AO3.User(userid)
            else:
                sep = '/'
                u = link.split(sep)[4]
                userid = u.split()[0]
                displayname = userid
                user = AO3.User(userid)

            if len(user.bio) > 1000:
                bio = f"{user.bio[0:700]}\n`Click link for more info`"
            elif len(user.bio) == 0:
                bio = "*N/A*"
            else:
                bio = user.bio

            desc = f"**Number of Works:** {user.works}\n**Number of Bookmarks:** {user.bookmarks}\n\n**Bio:**\n{bio}"  # noqa

    # embed formatting for AO3 work embed
            try:
                embed = embedVar = discord.Embed(
                    title=displayname, url=user.url, description=desc,
                    color=0x2F3136)

                embed.set_author(name="Archive of Our Own")
                embed.set_thumbnail(url="https://i.imgur.com/Ml4X1T6.png")

                embed.set_footer(text='bot not affiliated with OTW or AO3')

    # sends embed
                await message.channel.send(embed=embedVar)

                if dellink == "on":
                    await ctx.message.delete()
                else:
                    pass

            except Exception:
                pass


def setup(bot):
    bot.add_cog(eventuser(bot))
