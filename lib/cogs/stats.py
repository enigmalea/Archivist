
# //          Copyright Amber Whitlock aka enigmalea 2021
# // Distributed under the Boost Software License, Version 1.0.
# //    (See accompanying file LICENSE_1_0.txt or copy at
# //          https://www.boost.org/LICENSE_1_0.txt)

# Requires pip install ao3_api
import discord
from discord.ext import commands
from discord.ext.commands import Cog, command
import AO3


class stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('stats')

    @command(name="stats", brief="Shows the stats for the fic.")
    @commands.guild_only()
    async def stats(self, ctx, *, fic_link):
        """Shows the stats for the fic."""
        workid = AO3.utils.workid_from_url(fic_link)

        try:
            work = AO3.Work(workid)
        except AO3.utils.AuthError:
            autherr = """I'm sorry. This fic is available to Registered \
Users of AO3 only. In order to protect the author's privacy, I will not \
display an embed. Please go to AO3 directly while logged in to view this fic!"""  # noqa
            await ctx.channel.send(autherr)
        else:
            rawchap = f"{work.nchapters}/{work.expected_chapters}"
            if "None" in rawchap:
                chaps = f"{work.nchapters}/?"
            else:
                chaps = rawchap

            if len(work.metadata["series"]) != 0:
                dd = work._soup.find("dd", {"class": "series"})
                if dd is None:
                    pass

                for span in dd.find_all("span", {"class":
                                                 "position"}):
                    seriesid = int(span.a.attrs["href"].split("/")[-1])  # noqa

                ser = AO3.Series(seriesid)
                serurl = f"https://archiveofourown.org/series/{seriesid}"  # noqa
                seri = f"\n**Series:** [{ser.name}]({serurl})"
            else:
                seri = ""

            c = []
            for work.authors in work.authors:
                if "(" in work.authors.username:
                    sep1 = ' ('
                    un = work.authors.username.split(sep1)[0]
                    a = work.authors.username.split(sep1)[1]
                    b = a[:-1]
                    li = f"https://archiveofourown.org/users/{b}/pseuds/{un}"  # noqa
                    c.append(f"[{un}]({li})")
                else:
                    un = work.authors.username
                    li = f"https://archiveofourown.org/users/{un}"
                    c.append(f"[{un}]({li})")

            aut = ', '.join(c)

            if " Anonymous " in un:
                auth = "*Anonymous*"
            else:
                auth = aut

            desc = f"by {auth}{seri}"

# sets up changing embed color based on rating of work
            if work.rating.startswith('G'):
                value = 0x77A50E
            elif work.rating.startswith('T'):
                value = 0xE8D506
            elif work.rating.startswith('M'):
                value = 0xDE7E28
            elif work.rating.startswith('E'):
                value = 0x9C0000
            else:
                value = 0xFFFFFF

# sets rating as icon from AO3

            if work.rating.startswith('G'):
                icon = "<:general:866823809180631040>"
            elif work.rating.startswith('T'):
                icon = "<:teen:866823893015330826>"
            elif work.rating.startswith('M'):
                icon = "<:mature:866823956684996628>"
            elif work.rating.startswith('E'):
                icon = "<:explicit:866824069050269736>"
            else:
                icon = "<:notrated:866825856236519426>"

            # embed formatting for AO3 work embed
            try:
                embed = embedVar = discord.Embed(
                    title=f"Stats for {work.title}", description=desc,
                    url=work.url, color=value)

                embed.set_author(name="Archive of Our Own")
                embed.set_thumbnail(url="https://i.imgur.com/Ml4X1T6.png")

                embedVar.add_field(name="Rating:", value=icon,
                                   inline=False)

                embedVar.add_field(name="Date Published:",
                                   value=work.date_published.strftime(
                                       '%b %d, %Y'), inline=True)
                embedVar.add_field(name="Date Updated:",
                                   value=work.date_updated.strftime(
                                       '%b %d, %Y'), inline=True)
                embedVar.add_field(name="\ufeff", value="\ufeff",
                                   inline=True)

                embedVar.add_field(name="Chapters:", value=chaps,
                                   inline=True)
                embedVar.add_field(name="Status:", value=work.status,
                                   inline=True)
                embedVar.add_field(name="\ufeff", value="\ufeff",
                                   inline=True)

                embedVar.add_field(name="Words:", value=work.words,
                                   inline=True)
                embedVar.add_field(name="Hits:", value=work.hits,
                                   inline=True)
                embedVar.add_field(name="\ufeff", value="\ufeff",
                                   inline=True)

                embedVar.add_field(name="Kudos:", value=work.kudos,
                                   inline=True)
                embedVar.add_field(name="Bookmarks:", value=work.bookmarks,
                                   inline=True)
                embedVar.add_field(name="Comments:", value=work.comments,
                                   inline=True)

                embed.set_footer(text='bot not affiliated with OTW or AO3')

            # sends embed
                await ctx.channel.send(embed=embedVar)

            except Exception:
                pass

    @ stats.error
    async def stats_error(self, ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.send('That does not appear to be a link to an AO3 fic or \
work. Please make sure you are linking to the fic and not a series, author, \
collection, or using a non-AO3 link.')


def setup(bot):
    bot.add_cog(stats(bot))
