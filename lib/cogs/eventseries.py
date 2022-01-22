
# //          Copyright Amber Whitlock aka enigmalea 2021
# // Distributed under the Boost Software License, Version 1.0.
# //    (See accompanying file LICENSE_1_0.txt or copy at
# //          https://www.boost.org/LICENSE_1_0.txt)

import discord
from discord.ext.commands import Cog
import re
import AO3

from ..db import db


class eventseries(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('eventseries')

    @Cog.listener()
    async def on_message(self, message):
        ctx = await self.bot.get_context(message)
        ign = db.field("SELECT Ign FROM settings WHERE GuildID = ?", ctx.guild.id)  
        num = db.field("SELECT Num FROM settings WHERE GuildID = ?", ctx.guild.id)  
        dellink = db.field("SELECT DelLink FROM settings WHERE GuildID = ?", ctx.guild.id)  
        igncheck = f"{ign}http"

        # checks for message redirect
        redirect = db.field("SELECT redSer FROM settings WHERE GuildID = ?", ctx.guild.id)

        if redirect != "":
            channel = redirect
        else:
            channel = ctx

        if message.author == self.bot.user:
            return

        if ctx.command is None and igncheck not in message.content and \
                "archiveofourown.org/series" in message.content or \
                "ao3.org/series" in message.content:

            urls = re.findall(
                'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content.strip())  

            for url in urls:
                if "series" in url:
                    sep = '/'
                    s = url.split(sep)[4]
                    s2 = re.sub('>', '', s)
                    seriesid = int(s2.split(sep)[0])

                    try:
                        series = AO3.Series(seriesid)

                    except AO3.utils.InvalidIdError:
                        iderr = "This series does not seem to exist. Please try again."  
                        await message.channel.send(iderr)

                    seriesurl = f"https://archiveofourown.org/series/{seriesid}"

                    if num != "," and num == "space":
                        wordi = "{:,}".format(series.words)
                        word = wordi.replace(",", " ")
                    elif num != ",":
                        wordi = "{:,}".format(series.words)
                        word = wordi.replace(",", " ")
                    else:
                        word = "{:,}".format(series.words)

                    c = []
                    for series.creators in series.creators:

                        if "(" in series.creators.username:
                            sep1 = ' ('
                            un = series.creators.username.split(sep1)[0]
                            a = series.creators.username.split(sep1)[1]
                            b = a[:-1]
                            li = f"https://archiveofourown.org/users/{b}/pseuds/{un}"
                            c.append(f"[{un}]({li})")
                        else:
                            un = series.creators.username
                            li = f"https://archiveofourown.org/users/{un}"
                            c.append(f"[{un}]({li})")

                    aut = ', '.join(c)

                    if " Anonymous " in un:
                        auth = "*Anonymous*"
                    else:
                        auth = aut

                    if len(series.description) > 1000:
                        describe = f"{series.description[0:700]}\n`Click link for more info`"  
                    elif len(series.description) == 0:
                        describe = "*N/A*"
                    else:
                        describe = series.description

                    if len(series.notes) > 1000:
                        notes = f"{series.notes[0:700]}\n`Click link for more info`"
                    elif len(series.notes) == 0:
                        notes = "*N/A*"
                    else:
                        notes = series.notes

                    if series.complete is False:
                        complete = "No"
                    else:
                        complete = series.complete

                    desc = f"**Authors:** {auth}\n**Complete:** {complete}"

            # embed formatting for AO3 series embed
                    try:
                        embed = embedVar = discord.Embed(
                            title=series.name, url=seriesurl, description=desc,
                            color=0x2F3136)

                        embed.set_author(name="Archive of Our Own")
                        embed.set_thumbnail(url="https://i.imgur.com/Ml4X1T6.png")

                        embedVar.add_field(name="Series Begun:",
                                           value=series.series_begun.strftime(
                                               '%b %d, %Y'), inline=True)
                        embedVar.add_field(name="Last Updated:",
                                           value=series.series_updated.strftime(
                                               '%b %d, %Y'), inline=True)
                        embedVar.add_field(name="\ufeff", value="\ufeff", inline=True)

                        embedVar.add_field(name="Number of Works:",
                                           value=series.nworks, inline=True)
                        embedVar.add_field(name="Total Word Count:",
                                           value=word, inline=True)
                        embedVar.add_field(name="\ufeff", value="\ufeff", inline=True)

                        embedVar.add_field(name="Series Notes:",
                                           value=notes, inline=False)

                        embedVar.add_field(name="Series Description:",
                                           value=describe, inline=False)

                        embed.set_footer(text='bot not affiliated with OTW or AO3')

            # sends embed
                        await channel.send(embed=embedVar)

                        if dellink == "on":
                            await channel.message.delete()
                        else:
                            pass

                    except discord.errors.Forbidden:
                        permerror = "The embed can't be posted in the selected channel. Please make sure the bot has permissions to see and post in the channel."  
                        await message.channel.send(permerror)

                    except Exception:
                        raise


def setup(bot):
    bot.add_cog(eventseries(bot))
