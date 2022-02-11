
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
from urllib.parse import unquote

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
        ign = db.field("SELECT Ign FROM settings WHERE GuildID = ?", ctx.guild.id)  
        igncheck = f"{ign}http"

        dellink = db.field("SELECT DelLink FROM settings WHERE GuildID = ?", ctx.guild.id)

        # checks for message redirect
        redirect = db.field("SELECT redUse FROM settings WHERE GuildID = ?", ctx.guild.id)

        if redirect != "":
            channel = self.bot.get_channel(int(redirect))
        else:
            channel = ctx

        if message.author == self.bot.user:
            return

        if ctx.command is None and igncheck not in message.content and \
                "archiveofourown.org/users/" in message.content or \
                "ao3.org/users/" in message.content:

            urls = re.findall(
                'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content.strip())  

            for url in urls:
                if "users" in url:

                    if "pseuds" in url:

                        sep = 'users/'
                        sep2 = 'pseuds/'
                        u = url.split(sep)[1]
                        userid = u.split(sep2)[0]
                        dname = url.split(sep2)[1]
                        displayname = unquote(re.sub('\>', '', dname))
                        user = AO3.User(userid)

                    else:

                        sep = 'users/'
                        u = url.split(sep)[1]
                        userid = re.sub('[^A-Za-z0-9_]+', '', u)
                        displayname = userid
                        user = AO3.User(userid)

                if len(user.bio) > 1000:
                    bio = f"{user.bio[0:700]}\n`Click link for more info`"
                elif len(user.bio) == 0:
                    bio = "*N/A*"
                else:
                    bio = user.bio

                desc = f"**Number of Works:** {user.works}\n**Number of Bookmarks:** {user.bookmarks}\n\n**Bio:**\n{bio}"  

        # embed formatting for AO3 work embed
                try:
                    embed = embedVar = discord.Embed(
                        title=displayname, url=user.url, description=desc,
                        color=0x2F3136)

                    embed.set_author(name="Archive of Our Own")
                    embed.set_thumbnail(url="https://i.imgur.com/Ml4X1T6.png")

                    embed.set_footer(text='bot not affiliated with OTW or AO3')

        # sends embed
                    await channel.send(embed=embedVar)

                    if dellink == "on":
                        await ctx.message.delete()
                    else:
                        pass

                except discord.errors.Forbidden:
                    permerror = "The embed can't be posted in the selected channel. Please make sure the bot has permissions to see and post in the channel."  
                    await message.channel.send(permerror)

                except Exception:
                    pass


def setup(bot):
    bot.add_cog(eventuser(bot))
