# Requires pip install ao3_api
import discord
from discord.ext.commands import Cog
import re
import AO3

from ..db import db


class eventserieslink(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('eventserieslink')

    @Cog.listener()
    async def on_message(self, message):
        ctx = await self.bot.get_context(message)
        ign = db.field("SELECT Ign FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        igncheck = f"{ign}http"

        dellink = db.field("SELECT DelLink FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa

        if message.author == self.bot.user:
            return

        if ctx.command is None and igncheck not in message.content and\
                "https://archiveofourown.org/series/" in message.content:

            urls = re.findall(
                'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F]\
                [0-9a-fA-F]))+', message.content.strip())
            if urls:
                links = ''.join(urls)
                link = links.replace('>', '')

            sep = '/'
            s = link.split(sep)[4]
            seriesid = int(s.split()[0])
            series = AO3.Series(seriesid)
            seriesurl = f"https://archiveofourown.org/series/{seriesid}"

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
                describe = f"{series.description[0:700]}\n`Click link for more info`"  # noqa
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
                                   value=series.series_begun, inline=True)
                embedVar.add_field(name="Last Updated:",
                                   value=series.series_updated, inline=True)
                embedVar.add_field(name="\ufeff", value="\ufeff", inline=True)

                embedVar.add_field(name="Number of Works:",
                                   value=series.nworks, inline=True)
                embedVar.add_field(name="Total Word Count:",
                                   value=series.words, inline=True)
                embedVar.add_field(name="\ufeff", value="\ufeff", inline=True)

                embedVar.add_field(name="Series Notes:",
                                   value=notes, inline=False)
                embedVar.add_field(name="Series Description:",
                                   value=describe, inline=False)

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
    bot.add_cog(eventserieslink(bot))
