
# //          Copyright Amber Whitlock aka enigmalea 2021
# // Distributed under the Boost Software License, Version 1.0.
# //    (See accompanying file LICENSE_1_0.txt or copy at
# //          https://www.boost.org/LICENSE_1_0.txt)

# Requires pip install ao3_api
from ..db import db
import discord
from discord.ext.commands import Cog
import re
import AO3

import warnings
warnings.simplefilter('ignore', UserWarning)


class eventfic(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('eventfic')

    @Cog.listener()
    async def on_message(self, message):
        ctx = await self.bot.get_context(message)

        ign = db.field("SELECT Ign FROM settings WHERE GuildID = ?", ctx.guild.id)
        pub = db.field("SELECT PubInfo FROM settings WHERE GuildID = ?", ctx.guild.id)
        fan = db.field("SELECT Fan FROM settings WHERE GuildID = ?",  ctx.guild.id)
        rel = db.field("SELECT Rel FROM settings WHERE GuildID = ?",  ctx.guild.id)
        cha = db.field("SELECT Ch FROM settings WHERE GuildID = ?",  ctx.guild.id)
        ta = db.field("SELECT AddTags FROM settings WHERE GuildID = ?",  ctx.guild.id)
        summ = db.field("SELECT Summ FROM settings WHERE GuildID = ?",  ctx.guild.id)
        summlen = db.field("SELECT SumLength FROM settings WHERE GuildID = ?",  ctx.guild.id)
        dellink = db.field("SELECT DelLink FROM settings WHERE GuildID = ?",  ctx.guild.id)
        delch = db.field("SELECT DelChapter FROM settings WHERE GuildID = ?",  ctx.guild.id)
        image = db.field("SELECT Image FROM settings WHERE GuildID = ?",  ctx.guild.id)
        num = db.field("SELECT Num FROM settings WHERE GuildID = ?",  ctx.guild.id)

        igncheck = f"{ign}http"

        # checks for message redirect
        redirect = db.field("SELECT redFic FROM settings WHERE GuildID = ?", ctx.guild.id)

        if message.author == self.bot.user:
            return

        if redirect != "":
            channel = self.bot.get_channel(int(redirect))
        else:
            channel = ctx

        if ctx.command is None and igncheck not in message.content and \
                "archiveofourown.org/" in message.content or \
                "ao3.org/" in message.content and "works/" in message.content:

            urls = re.findall(
                'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content.strip())  

            for url in urls:
                if "works" in url and "Sort+and+Filter" not in url:
                    url1 = re.sub('>', '', url)
                    workid = AO3.utils.workid_from_url(url1)

                    if delch == "on" and "chapters" in url:
                        chaptererr = "You've posted a link which has chapter \
        information. This server requires you to use `$update [chapter#] [link]` to \
        post updates to your fics."  
                        await message.channel.send(chaptererr, delete_after=30)

                    else:

                        try:
                            work = AO3.Work(workid)

                        except AO3.utils.AuthError:
                            autherr = "I'm sorry. This fic is available to Registered \
        Users of AO3 only. In order to protect the author's privacy, I will not \
        display an embed. Please go to AO3 directly while logged in to view this fic!"  
                            await message.channel.send(autherr)

                        except AO3.utils.InvalidIdError:
                            iderr = "This work does not seem to exist. Please try again."  
                            await message.channel.send(iderr)

                        else:
                            warn = ', '.join(work.warnings)
                            pubd = work.date_published.strftime('%b %d, %Y')
                            upd = work.date_updated.strftime('%b %d, %Y')

                            if num != "," and num == "space":
                                wordi = "{:,}".format(work.words)
                                word = wordi.replace(",", " ")
                            elif num != ",":
                                wordi = "{:,}".format(work.words)
                                word = wordi.replace(",", " ")
                            else:
                                word = "{:,}".format(work.words)

                            rawchap = f"{work.nchapters}/{work.expected_chapters}"
                            if "None" in rawchap:
                                chaps = f"{work.nchapters}/?"
                            else:
                                chaps = rawchap

                            if len(work.metadata["series"]) != 0:
                                dd = work._soup.find("dd", {"class": "series"})
                                if dd is None:
                                    pass

                                se = []
                                for work.series in work.series:
                                    ser = AO3.Series(work.series.id)
                                    serurl = f"https://archiveofourown.org/series/{work.series.id}"  
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

                            desc = f"by {auth}{seri}"

                            rawtags = ', '.join(work.tags)
                            if len(rawtags) > 1000:
                                tag = rawtags[0:700]
                                atag = tag.rsplit(' ', 1)[0]
                                tags = f"{atag}\n`Click link for more info`"
                            elif len(rawtags) == 0:
                                tags = "*N/A*"
                            else:
                                tags = rawtags

                            rawcats = ', '.join(work.categories)
                            if len(rawcats) > 1000:
                                categories = f"{rawcats[0:700]}\n`Click link for more info`"  
                            elif len(rawcats) == 0:
                                categories = "*N/A*"
                            else:
                                categories = rawcats

                            rawfan = ', '.join(work.fandoms)
                            if len(rawfan) > 1000:
                                fan = rawfan[0:700]
                                fand = fan.rsplit(' ', 1)[0]
                                fandoms = f"{fand}\n`Click link for more info`"
                            else:
                                fandoms = rawfan

                            ships = ', '.join(work.relationships)
                            if len(ships) > 1000:
                                shi = ships[0:700]
                                ship = shi.rsplit(' ', 1)[0]
                                relationships = f"{ship}\n`Click link for more info`"  
                            elif len(ships) == 0:
                                relationships = "*N/A*"
                            else:
                                relationships = ships

                            chars = ', '.join(work.characters)
                            if len(chars) > 1000:
                                cha = chars[0:700]
                                char = cha.rsplit(' ', 1)[0]
                                characters = f"{char}\n`Click link for more info`"
                            elif len(chars) == 0:
                                characters = "*N/A*"
                            else:
                                characters = chars

                            if len(work.summary) > summlen:
                                sum = work.summary[0:summlen]
                                summa = sum.rsplit(' ', 1)[0]
                                summary = f"{summa}\n`Click link for more info`"
                            elif len(work.summary) == 0:
                                summary = "*N/A*"
                            else:
                                summary = work.summary

                    # DICT & variable for embed sidebar color
                            rating_bar = dict([
                                ('General Audiences', 0x77A50E),
                                ('Teen And Up Audiences', 0xE8D506),
                                ('Mature', 0xDE7E28),
                                ('Explicit', 0x9C0000),
                                ('Not Rated', 0xFFFFFF),
                            ])

                            color = rating_bar[work.rating]

                    # DICT & variable for rating icon
                            rating_icon = dict([
                                ('General Audiences', '<:general:866823809180631040>'),
                                ('Teen And Up Audiences', '<:teen:866823893015330826>'),
                                ('Mature', '<:mature:866823956684996628>'),
                                ('Explicit', '<:explicit:866824069050269736>'),
                                ('Not Rated', '<:notrated:866825856236519426>'),
                            ])

                            icon = rating_icon[work.rating]

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
                                    title=work.title, description=desc,
                                    url=work.url, color=color)

                                embed.set_author(name="Archive of Our Own")
                                embed.set_thumbnail(url=img)

                                embedVar.add_field(name="Words:", value=word,
                                                   inline=True)
                                embedVar.add_field(name="Chapters:", value=chaps,
                                                   inline=True)
                                embedVar.add_field(name="Language:",
                                                   value=work.language,
                                                   inline=True)
                                if pub == "on":
                                    embedVar.add_field(name="Published:",
                                                       value=pubd,
                                                       inline=True)
                                    embedVar.add_field(name="Updated:",
                                                       value=upd,
                                                       inline=True)
                                    embedVar.add_field(name="Status:",
                                                       value=work.status,
                                                       inline=True)
                                else:
                                    pass

                                embedVar.add_field(name="Rating:",
                                                   value=icon,
                                                   inline=True)
                                embedVar.add_field(name="Warnings:", value=warn,
                                                   inline=True)
                                embedVar.add_field(name="Categories:",
                                                   value=categories,
                                                   inline=True)

                                if fan == "on":
                                    embedVar.add_field(name="Fandoms:",
                                                       value=fandoms,
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
                                                       value=characters,
                                                       inline=False)
                                else:
                                    pass

                                if ta == "on":
                                    embedVar.add_field(name="Additional Tags:",
                                                       value=tags,
                                                       inline=False)
                                else:
                                    pass

                                if summ == "on":
                                    embedVar.add_field(name="Summary:",
                                                       value=summary,
                                                       inline=False)
                                else:
                                    pass

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
    bot.add_cog(eventfic(bot))
