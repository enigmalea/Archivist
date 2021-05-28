
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
        if "collections" in fic_link:
            sep = '/'
            sep2 = '?'
            w = fic_link.split(sep)[6]
            x = w.split(sep2)[0]
            workid = int(x.split()[0])
            work = AO3.Work(workid)

        else:
            sep = '/'
            sep2 = '?'
            w = fic_link.split(sep)[4]
            x = w.split(sep2)[0]
            workid = int(x.split()[0])
            work = AO3.Work(workid)

            rawchap = f"{work.chapters}/{work.expected_chapters}"
            if "None" in rawchap:
                chaps = f"{work.chapters}/?"
            else:
                chaps = f"{work.chapters}/{work.expected_chapters}"

            if work.metadata["series"]:
                ser = ''.join(work.metadata["series"])
                seri = f"**Series:** {ser}"
            else:
                seri = ""

            c = []
            for work.authors in work.authors:

                if "(" in work.authors.username:
                    sep1 = ' ('
                    un = work.authors.username.split(sep1)[0]
                    a = work.authors.username.split(sep1)[1]
                    b = a[:-1]
                    li = f"https://archiveofourown.org/users/{b}/pseuds/{un}"
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

            desc = f"by {auth}\n{seri}"

# sets up changing embed color based on rating of work
        if work.rating.startswith('G'):
            value = 0x77A50E
        elif work.rating.startswith('T'):
            value = 0xE8D506
        elif work.rating.startswith('M'):
            value = 0xDE7E28
        else:
            value = 0x9C0000

# embed formatting for AO3 work embed
        try:
            embed = embedVar = discord.Embed(
                title=f"Stats for {work.title}", description=desc,
                url=work.url, color=value)

            embed.set_author(name="Archive of Our Own")
            embed.set_thumbnail(url="https://i.imgur.com/Ml4X1T6.png")

            embedVar.add_field(name="Rating:", value=work.rating, inline=False)

            embedVar.add_field(name="Date Published:",
                               value=work.date_published.strftime(
                                   '%b %d, %Y'), inline=True)
            embedVar.add_field(name="Date Updated:",
                               value=work.date_updated.strftime(
                                   '%b %d, %Y'), inline=True)
            embedVar.add_field(name="\ufeff", value="\ufeff", inline=True)

            embedVar.add_field(name="Chapters:", value=chaps,
                               inline=True)
            embedVar.add_field(name="Status:", value=work.status,
                               inline=True)
            embedVar.add_field(name="\ufeff", value="\ufeff", inline=True)

            embedVar.add_field(name="Words:", value=work.words, inline=True)
            embedVar.add_field(name="Hits:", value=work.hits, inline=True)
            embedVar.add_field(name="\ufeff", value="\ufeff", inline=True)

            embedVar.add_field(name="Kudos:", value=work.kudos, inline=True)
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
