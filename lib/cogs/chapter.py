
# //          Copyright Amber Whitlock aka enigmalea 2021
# // Distributed under the Boost Software License, Version 1.0.
# //    (See accompanying file LICENSE_1_0.txt or copy at
# //          https://www.boost.org/LICENSE_1_0.txt)

# Requires pip install ao3_api
import discord
from discord.ext import commands
from discord.ext.commands import Cog, command, MissingRequiredArgument
import AO3

from ..db import db


class chapter(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('chapter')

    @command(name="update", aliases=["up", "chapter", "ch"],
             brief="Provides an embed for a chapter update.")
    @commands.guild_only()
    async def ch_update(self, ctx, chnum, link: str):
        """
        Shows an embed for chapter updates.\n▸`<p>update [chapter#] [link]`
        """
        pub = db.field("SELECT cPubInfo FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        fan = db.field("SELECT cFan FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        rel = db.field("SELECT cRel FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        cha = db.field("SELECT cCh FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        ta = db.field("SELECT cAddTags FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        summ = db.field("SELECT cSumm FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        summlen = db.field("SELECT cSumLength FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        delcom = db.field("SELECT DelUpdate FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        delerr = db.field("SELECT DelErr FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        image = db.field("SELECT Image FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        num = db.field("SELECT Num FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa

        if "http" in chnum:
            message = """You may have entered required arguments in the
wrong order. Please try again using the format \
`<p>update [chapter#] [link]`, i.e.
`$update 10 https://archiveofourown.org/works/17363696/chapters/40857350`."""
            if delerr == "on":
                await ctx.send(message, delete_after=30)
                if delcom == "on":
                    await ctx.message.delete()
            else:
                await ctx.send(message)
                if delcom == "on":
                    await ctx.message.delete()
            pass

        elif "works" not in link:
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
            if "works" in link:
                workid = AO3.utils.workid_from_url(link)

                if int(chnum) >= 1:
                    try:
                        ch_int = int(chnum)
                        ch = ch_int - 1
                        work = AO3.Work(workid)
                        chapter = work.chapters[ch]

                    except IndexError:
                        inderror = 'That chapter does not appear to exist. \
Please double check the chapter number you provided and try again.'
                        if delerr == "on":
                            await ctx.send(inderror, delete_after=30)
                            if delcom == "on":
                                await ctx.message.delete()
                        else:
                            await ctx.send(inderror)
                            if delcom == "on":
                                await ctx.message.delete()

                    except AO3.utils.InvalidIdError:
                        iderr = """This work does not seem to exist. Please try again."""  # noqa
                        await message.channel.send(iderr)

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
                else:
                    cherr = 'Chapter number should be greater than 1.'
                    if delerr == "on":
                        await ctx.send(cherr, delete_after=30)
                        if delcom == "on":
                            await ctx.message.delete()
                    else:
                        await ctx.send(cherr)
                        if delcom == "on":
                            await ctx.message.delete()

                if len(chapter.title) != 0:
                    title = f"Chapter {chapter.number}: {chapter.title}"
                    ctitle = title.upper()
                    chtitle = f"**[{ctitle}]({link})**"  # noqa
                else:
                    title = f"Chapter {chapter.number}"
                    ctitle = title.upper()
                    chtitle = f"**[{ctitle}]({link})**"  # noqa

                fic = f"\n\n▸ [__READ FROM BEGINNING__]({work.url})\n\u200B"

                if num != "," and num == "space":
                    cwordi = "{:,}".format(chapter.words)
                    cword = cwordi.replace(",", " ")
                    wwordi = "{:,}".format(work.words)
                    wword = wwordi.replace(",", " ")
                elif num != ",":
                    cwordi = "{:,}".format(chapter.words)
                    cword = cwordi.replace(",", num)
                    wwordi = "{:,}".format(work.words)
                    wword = wwordi.replace(",", num)
                else:
                    cword = "{:,}".format(chapter.words)
                    wword = "{:,}".format(work.words)

                words = f"**{cword}** [{wword}]"

                warn = ', '.join(work.warnings)

                rawchap = f"{chapter.number}/{work.expected_chapters}"
                if "None" in rawchap:
                    chaps = f"{chapter.number}/?"
                else:
                    chaps = rawchap

                if len(work.metadata["series"]) != 0:
                    dd = work._soup.find("dd", {"class": "series"})
                    if dd is None:
                        pass

                    se = []
                    for work.series in work.series:
                        ser = AO3.Series(work.series.id)
                        serurl = f"https://archiveofourown.org/series/{work.series.id}"  # noqa
                        se.append(f"[{ser.name}]({serurl})")

                        mse = ', '.join(se)

                    seri = f"\n**Series:** {mse}"
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

                desc = f"{chtitle}\nby {auth}{seri}{fic}"

                rawtags = ', '.join(work.tags)
                if len(rawtags) > 1000:
                    tags = f"{rawtags[0:700]}\n`Click link for more info`"
                elif len(rawtags) == 0:
                    tags = "*N/A*"
                else:
                    tags = rawtags

                rawfan = ', '.join(work.fandoms)
                if len(rawfan) > 1000:
                    fandoms = f"{rawfan[0:700]}\n`Click link for more info`"
                else:
                    fandoms = rawfan

                ships = ', '.join(work.relationships)
                if len(ships) > 1000:
                    relationships = f"{ships[0:700]}\n`Click link for more info`"  # noqa
                elif len(ships) == 0:
                    relationships = "*N/A*"
                else:
                    relationships = ships

                chars = ', '.join(work.characters)
                if len(chars) > 1000:
                    characters = f"{chars[0:700]}\n`Click link for more info`"
                elif len(chars) == 0:
                    characters = "*N/A*"
                else:
                    characters = chars

                if len(chapter.summary) > summlen:
                    sum = chapter.summary[0:summlen]
                    summa = sum.rsplit(' ', 1)[0]
                    summary = f"{summa}\n`Click link for more info`"
                elif len(chapter.summary) == 0:
                    summary = "*N/A*"
                else:
                    summary = chapter.summary

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

            # adds image preview for artwork in chapters
                if image == "on":
                    try:
                        images = work.get_images()
                        if len(images) == 0:
                            img = "https://i.imgur.com/Ml4X1T6.png"

                        else:
                            chimgs = images.get(1)
                            chimg = chimgs[0]
                            img = chimg[0]

                    except Exception:
                        img = "https://i.imgur.com/Ml4X1T6.png"

                else:
                    img = "https://i.imgur.com/Ml4X1T6.png"

            # embed formatting for AO3 work embed
                try:
                    embed = embedVar = discord.Embed(
                        title=work.title, description=desc, color=value)

                    embed.set_author(name="Archive of Our Own")
                    embed.set_thumbnail(url=img)

                    embedVar.add_field(name="Words:", value=words,
                                       inline=True)
                    embedVar.add_field(name="Chapters:", value=chaps,
                                       inline=True)
                    embedVar.add_field(name="Rating:", value=icon,
                                       inline=True)

                    if pub == "on":
                        embedVar.add_field(name="Published:",
                                           value=work.date_published.strftime(
                                               '%b %d, %Y'), inline=True)
                        embedVar.add_field(name="Updated:",
                                           value=work.date_updated.strftime(
                                               '%b %d, %Y'), inline=True)
                        embedVar.add_field(name="Status:", value=work.status,
                                           inline=True)
                    else:
                        pass

                    embedVar.add_field(name="Warnings:", value=warn,
                                       inline=False)

                    if fan == "on":
                        embedVar.add_field(name="Fandoms:", value=fandoms,
                                           inline=False)
                    else:
                        pass

                    if rel == "on":
                        embedVar.add_field(name="Relationships:",
                                           value=relationships,
                                           inline=False)
                    else:
                        pass

                    if cha == "on":
                        embedVar.add_field(name="Characters:",
                                           value=characters, inline=False)
                    else:
                        pass

                    if ta == "on":
                        embedVar.add_field(name="Additional Tags:", value=tags,
                                           inline=False)
                    else:
                        pass

                    if summ == "on":
                        embedVar.add_field(name="Summary:", value=summary,
                                           inline=False)
                    else:
                        pass

                    embed.set_footer(text='bot not affiliated with OTW or AO3')

            # sends embed
                    await ctx.send(embed=embedVar)

                    if delcom == "on":
                        await ctx.message.delete()

                except Exception:
                    pass

    @ch_update.error
    async def missingarg(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            delerr = db.field("SELECT DelErr FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
            delcom = db.field("SELECT DelUpdate FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
            missingarg = 'This command requires two arguments: chapter number \
and a link to a fic. Please try again using the format \
`<p>update [chapter#] [link]`, i.e. \
`$update 10 https://archiveofourown.org/works/17363696/chapters/40857350`.'
            if delerr == "on":
                await ctx.send(missingarg, delete_after=30)
                if delcom == "on":
                    await ctx.message.delete()
            else:
                await ctx.send(missingarg)
                if delcom == "on":
                    await ctx.message.delete()


def setup(bot):
    bot.add_cog(chapter(bot))
