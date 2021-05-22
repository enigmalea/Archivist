# Requires pip install ao3_api
import discord
from discord.ext.commands import Cog
import re
import AO3

from ..db import db


class eventcollink(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('eventcollink')

    @Cog.listener()
    async def on_message(self, message):
        ctx = await self.bot.get_context(message)

        ign = db.field("SELECT Ign FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        pub = db.field("SELECT PubInfo FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        fan = db.field("SELECT Fan FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        rel = db.field("SELECT Rel FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        cha = db.field("SELECT Ch FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        ta = db.field("SELECT AddTags FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        summ = db.field("SELECT Summ FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        summlen = db.field("SELECT SumLength FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        dellink = db.field("SELECT DelLink FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa

        igncheck = f"{ign}http"

        if message.author == self.bot.user:
            return

        if ctx.command is None and igncheck not in message.content and\
                "https://archiveofourown.org/collections/" in message.content:  # noqa

            urls = re.findall(
                'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content.strip())  # noqa
            if urls:
                links = ''.join(urls)
                link = links.replace('>', '')

            sep = '/'
            sep2 = '?'
            w = link.split(sep)[6]
            x = w.split(sep2)[0]
            workid = int(x.split()[0])

            try:
                work = AO3.Work(workid)
            except AO3.utils.AuthError:
                autherr = """I'm sorry. This fic is available to Registered \
Users of AO3 only. In order to protect the author's privacy, I will not \
display an embed. Please go to AO3 directly while logged in to view this fic!"""  # noqa
                await message.channel.send(autherr)

            else:
                warn = ', '.join(work.warnings)

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

                desc = f"by {auth}\n{seri}"

                rawtags = ', '.join(work.tags)
                if len(rawtags) > 1000:
                    tags = f"{rawtags[0:700]}\n`Click link for more info`"
                elif len(rawtags) == 0:
                    tags = "*N/A*"
                else:
                    tags = rawtags

                rawcats = ', '.join(work.categories)
                if len(rawcats) > 1000:
                    categories = f"{rawcats[0:700]}\n`Click link for more info`"  # noqa
                elif len(rawcats) == 0:
                    categories = "*N/A*"
                else:
                    categories = rawcats

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

                if len(work.summary) > summlen:
                    summary = f"{work.summary[0:summlen]}\n`Click link for more info`"  # noqa
                elif len(work.summary) == 0:
                    summary = "*N/A*"
                else:
                    summary = work.summary

    # sets up changing embed color based on rating of work
                if work.rating.startswith('G'):
                    value = 0x77A50E
                elif work.rating.startswith('T'):
                    value = 0xE8D506
                elif work.rating.startswith('M'):
                    value = 0xDE7E28
                else:
                    value = 0x9C0000

    # adds image preview for artwork in chapters
                text = work.get_chapter_images(1)
                try:
                    if text[0] in text:
                        rawimg = text[0]
                        img = f"{rawimg[0]}"
                except Exception:
                    img = "https://i.imgur.com/Ml4X1T6.png"
                    pass

    # embed formatting for AO3 work embed
                try:
                    embed = embedVar = discord.Embed(
                        title=work.title, description=desc, url=work.url,
                        color=value)

                    embed.set_author(name="Archive of Our Own")
                    embed.set_thumbnail(url=img)

                    embedVar.add_field(name="Words:", value=work.words,
                                       inline=True)
                    embedVar.add_field(name="Chapters:", value=chaps,
                                       inline=True)
                    embedVar.add_field(name="Language:", value=work.language,
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

                    embedVar.add_field(name="Rating:", value=work.rating,
                                       inline=True)
                    embedVar.add_field(name="Warnings:", value=warn,
                                       inline=True)
                    embedVar.add_field(name="Categories:", value=categories,
                                       inline=True)

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
                    await message.channel.send(embed=embedVar)

                    if dellink == "on":
                        await self.bot.delete_message(ctx.message)
                    else:
                        pass

                except Exception:
                    raise


def setup(bot):
    bot.add_cog(eventcollink(bot))
