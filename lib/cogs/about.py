
# //          Copyright Amber Whitlock aka enigmalea 2021
# // Distributed under the Boost Software License, Version 1.0.
# //    (See accompanying file LICENSE_1_0.txt or copy at
# //          https://www.boost.org/LICENSE_1_0.txt)

import discord
import time
import datetime

from discord.ext import commands
from discord.ext.commands import Cog, command


class about(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):

        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('about')

    @command(name="about", brief="Provides info about the bot.")
    @commands.guild_only()
    async def support(self, ctx):
        """Provides info about Archivist."""

        name = ctx.me.display_name
        servers = len(self.bot.guilds)
        secs = int(round(time.time() - self.bot.start_time))
        uptime = str(datetime.timedelta(seconds=secs))
        version = self.bot.VERSION
        launch = "16 Mar 2021"
        shard = ctx.guild.shard_id

        title = f"About {name}"


        sup = "Support Server"
        supurl = "https://discord.gg/FzhC9bVFva"
        twit = "@\_ArchivistBot\_"
        twiturl = "https://twitter.com/_ArchivistBot_"
        web = "archivistbot.com"
        weburl = "https://www.archivistbot.com"
        inv = "Invite to Your Server"
        invurl = "https://discord.com/api/oauth2/authorize?client_id=812505952959856690&permissions=294205549632&scope=bot"
        pri = "Privacy Policy"
        priurl = "https://www.archivistbot.com/privacy-policy"


        links = f"""<:add:906993610329841734> [{inv}]({invurl})\n❔ \
        [{sup}]({supurl})\n💻 [{web}]({weburl})\n \
        <:twitter:906993635508248596> [{twit}]({twiturl})\n🔒 \
        [{pri}]({priurl})"""

        stats = f"""**Servers:** {servers}\n**Shard ID:** {shard}\n**Launched:** {launch}"""

        disc = f"*{name} does not store any user messages. For information on \
        what information the bot stores and how it uses the information \
        please review the privacy policy at the link above.*"

        embed = embedVar = discord.Embed(
            title=title, color=0x2F3136)

        embedVar.add_field(name="Owner/Developer", value="enigmalea#6509",
                           inline=True)

        embedVar.add_field(name="Version",
                           value=version, inline=True)

        embedVar.add_field(name="Uptime",
                           value=uptime, inline=True)

        embedVar.add_field(name="Stats", value=stats,
                           inline=False)

        embedVar.add_field(name="Links", value=links,
                           inline=False)

        embedVar.add_field(name="\u200b", value=disc,
                           inline=False)

        embed.set_footer(text=f"Thank you for using {name}!")

# sends embed
        await ctx.channel.send(embed=embedVar)


def setup(bot):
    bot.add_cog(about(bot))
