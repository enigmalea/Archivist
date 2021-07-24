
# //          Copyright Amber Whitlock aka enigmalea 2021
# // Distributed under the Boost Software License, Version 1.0.
# //    (See accompanying file LICENSE_1_0.txt or copy at
# //          https://www.boost.org/LICENSE_1_0.txt)
import discord
import AO3

from discord.ext import commands
from discord.ext.commands import Cog, command, MissingRequiredArgument

from ..db import db


class dl(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('dl')

    @command(name="dl",
             brief="Gives you a link to download a fic.")
    @commands.guild_only()
    async def dl(self, ctx, file_type: str, url: str):
        """
        Gives you an with a link to download a fic from AO3. Supports azw3, \
epub, mobi, pdf, or html.\n▸`<p>dl [file_type] [url]`.
        """
        dltype = ["azw3", "epbub", "mobi", "pdf", "html"]
        delerr = db.field("SELECT DelErr FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        delcom = db.field("SELECT DelDL FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa

        if file_type not in dltype:
            message = 'The file type you requested is not available; supported \
file types include: azw3, epbub, mobi, pdf, html. You may also have entered \
the required arguments in the incorrect order. Please try again using the \
format `<p>dl [file_type] [link]`.'
            if delerr == "on":
                await ctx.send(message, delete_after=30)
                if delcom == "on":
                    await ctx.message.delete()
            else:
                await ctx.send(message)
                if delcom == "on":
                    await ctx.message.delete()
            pass

        else:
            if "works" not in url:
                message = 'That does not appear to be a link to an AO3 work. \
Please make sure you are linking to the work and not a series, author, \
collection, or using a non-AO3 link.'
                if delerr == "on":
                    await ctx.send(message, delete_after=30)
                    if delcom == "on":
                        await ctx.message.delete()
                else:
                    await ctx.send(message)
                    if delcom == "on":
                        await ctx.message.delete()
                pass

            else:
                try:
                    workid = AO3.utils.workid_from_url(url)
                    work = AO3.Work(workid)
                    title = work.title
                    punc = '''!()-[]{};:'",<>./\?@#$%^&*_~'''

                    for ele in title:
                        if ele in punc:
                            title = title.replace(ele, "")

                    dltitle = '%20'.join(title.split(' ')[:4])

                    link = f"https://archiveofourown.org/downloads/{workid}/{dltitle}.{file_type}"  # noqa

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

                    if file_type == "html":
                        img = "<:html:848005536347455498>"

                    elif file_type == "epub":
                        img = "<:epub:848005536241680434>"

                    elif file_type == "azw3":
                        img = "<:azw3:848005536283885579>"

                    elif file_type == "mobi":
                        img = "<:mobi:848005536493600768>"

                    elif file_type == "pdf":
                        img = "<:pdf:848005536552976444>"

                    else:
                        img = ""

                    desc = f"by {auth}\n\n*Click the link below to download the \
**{file_type}** you requested.*\n\n{img} [**Download**]({link})\n\n☆ DON'T \
FORGET TO VISIT AO3 TO LEAVE KUDOS OR COMMENTS! ☆"

            # embed formatting for AO3 series embed
                    try:
                        embed = embedVar = discord.Embed(
                            title=work.title, description=desc, url=work.url,
                            color=0x2F3136)

                        embed.set_author(name="Archive of Our Own")
                        embed.set_thumbnail(url="https://i.imgur.com/Ml4X1T6.png")  # noqa

                        embed.set_footer(text='bot not affiliated with OTW or AO3')  # noqa

            # sends embed
                        await ctx.channel.send(embed=embedVar)

                        if delcom == "on":
                            await ctx.message.delete()

                    except Exception:
                        raise

                except AO3.utils.AuthError:
                    autherr = """I'm sorry. This fic is available to Registered \
Users of AO3 only. In order to protect the author's privacy, I will not \
display an embed. Please go to AO3 directly while logged in to view this fic!"""  # noqa
                    if delerr == "on":
                        await ctx.send(autherr, delete_after=30)
                        if delcom == "on":
                            await ctx.message.delete()
                    else:
                        await ctx.send(autherr)
                        if delcom == "on":
                            await ctx.message.delete()

    @dl.error
    async def missingarg(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            delerr = db.field("SELECT DelErr FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
            delcom = db.field("SELECT DelDL FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
            missingarg = 'This command requires two arguments: file type \
and a link to a fic. Please try again using the format \
`<p>dl [file_type] [link]`, i.e. \
`$dl pdf https://archiveofourown.org/works/17363696/chapters/40857350`.'
            if delerr == "on":
                await ctx.send(missingarg, delete_after=30)
                if delcom == "on":
                    await ctx.message.delete()
            else:
                await ctx.send(missingarg)
                if delcom == "on":
                    await ctx.message.delete()


def setup(bot):
    bot.add_cog(dl(bot))
