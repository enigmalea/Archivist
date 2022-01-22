
# //          Copyright Amber Whitlock aka enigmalea 2021
# // Distributed under the Boost Software License, Version 1.0.
# //    (See accompanying file LICENSE_1_0.txt or copy at
# //          https://www.boost.org/LICENSE_1_0.txt)

# Requires pip install ao3_api
import discord
from discord.ext import commands
from discord.ext.commands import Cog, CommandError, command
import AO3


class works(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('works')

    @command(name="works", brief="Produces an embed with links to the series' fics.")  
    @commands.guild_only()
    async def works(self, ctx, *, series_link):
        """Produces an embed with links to the series' fics. Please note the \
        number of fics displayed may vary based on title length."""
        sep = '/'
        s = series_link.split(sep)[4]
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

        wo = []
        for series.work_list in series.work_list:
            title = series.work_list.title
            wurl = series.work_list.url
            wo.append(f"[{title}]({wurl})")

        rawworks = '\n'.join(['{}. {}'.format(i, val) for i, val in
                             (enumerate(wo, start=1))])

        if len(rawworks) > 1000:
            rworks = rawworks[0:950]
        else:
            rworks = rawworks

        if rworks.endswith(')'):
            works = rworks
        else:
            wor = rworks.splitlines()
            work = wor[:-1]
            work1 = '\n'.join(work)
            works = f"{work1}\n`Click series link for more works`"

        desc = f"**Authors:** {auth}\n**Works:**\n{works}"

# embed formatting for AO3 series embed
        try:
            embed = embedVar = discord.Embed(
                title=series.name, url=seriesurl, description=desc,
                color=0x2F3136)

            embed.set_author(name="Archive of Our Own")
            embed.set_thumbnail(url="https://i.imgur.com/Ml4X1T6.png")

            embed.set_footer(text='bot not affiliated with OTW or AO3')

# sends embed
            await ctx.channel.send(embed=embedVar)

        except Exception:
            pass

    @works.error
    async def works_error(self, ctx, error):
        if isinstance(error, CommandError):
            await ctx.send('That does not appear to be a link to an AO3 series.\
 Please make sure you are linking to the series and not a work, author, \
 collection, or using a non-AO3 link.')


def setup(bot):
    bot.add_cog(works(bot))
