
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

        if ctx.command is None and igncheck not in message.content and \
                "archiveofourown.org/users/" in message.content or \
                "ao3.org/users/" in message.content:

            urls = re.findall(
                'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content.strip())  # noqa

            for url in urls:
                if "users" in url:

                    if "pseuds" in url:
                        try:
                            sep = 'users/'
                            sep2 = 'pseuds/'
                            u = url.split(sep)[1]
                            userid = re.sub('/>', '', u)
                            dname = url.split(sep2)[1]
                            displayname = re.sub('[!@#$%^&*()-=+:;,.><"/\|]', '', dname)
                            user = AO3.User(userid)
                        except Exception:
                            usererr = f"""This user does not exist. Please \
report this error to the developer by joining the support server and sharing \
a screenshot.
**Support Server:** https://discord.gg/FzhC9bVFva"""  # noqa
                            await message.channel.send(usererr)

                    else:
                        try:
                            sep = 'users/'
                            u = url.split(sep)[1]
                            userid = re.sub('[!@#$%^&*()-=+:;,.><"/\|]', '', u)
                            displayname = userid
                            user = AO3.User(userid)
                        except Exception:
                            usererr = f"""This user does not exist. Please \
report this error to the developer by joining the support server and sharing \
a screenshot.
**Support Server:** https://discord.gg/FzhC9bVFva"""  # noqa
                            await message.channel.send(usererr)

            try:
                if len(user.bio) > 1000:
                    bio = f"{user.bio[0:700]}\n`Click link for more info`"
                elif len(user.bio) == 0:
                    bio = "*N/A*"
                else:
                    bio = user.bio
            except Exception:
                usererr = f"""This user does not exist. Please \
report this error to the developer by joining the support server and sharing \
a screenshot.
**Support Server:** https://discord.gg/FzhC9bVFva"""  # noqa
                await message.channel.send(usererr)

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
