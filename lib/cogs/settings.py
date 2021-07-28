
# //          Copyright Amber Whitlock aka enigmalea 2021
# // Distributed under the Boost Software License, Version 1.0.
# //    (See accompanying file LICENSE_1_0.txt or copy at
# //          https://www.boost.org/LICENSE_1_0.txt)

# requires pip install disputils
import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Cog, has_permissions, cooldown
from disputils import BotEmbedPaginator

from ..db import db


class settings(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('settings')

    @commands.group(name="settings", aliases=["set"],
                    brief="Shows or sets prefix depending on the subcommand.")
    @commands.guild_only()
    async def myset(self, ctx):
        """
        Shows or sets server settings. For a full list of current settings and
        subcommands use `<p>settings show`.
        """
        msg = "This command requires a subcommand. For a full list of current \
settings and subcommands use `< p > settings show`."

        if ctx.invoked_subcommand is None:
            await ctx.send(msg)

    @myset.command(name="pub")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def change_pub(self, ctx, onoff: str):
        """Toggles publishing date row on or off."""

        if onoff == "on":
            db.execute("UPDATE settings SET PubInfo = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Publishing date row has been turned `{onoff}`.")

        elif onoff == "off":
            db.execute("UPDATE settings SET PubInfo = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Publishing date row has been turned `{onoff}`.")

        else:
            await ctx.send("Invalid setting. Valid choices are `on` or `off`.")

    @myset.command(name="fan")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def change_fan(self, ctx, onoff: str):
        """Toggles fandoms on or off."""

        if onoff == "on":
            db.execute("UPDATE settings SET Fan = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Fandoms have been turned `{onoff}`.")

        elif onoff == "off":
            db.execute("UPDATE settings SET Fan = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Fandoms have been turned `{onoff}`.")

        else:
            await ctx.send("Invalid setting. Valid choices are `on` or `off`.")

    @myset.command(name="img")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def change_img(self, ctx, onoff: str):
        """Toggles image previews on or off in fic and chapter embeds."""

        if onoff == "on":
            db.execute("UPDATE settings SET Image = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Image previews have been turned `{onoff}`.")

        elif onoff == "off":
            db.execute("UPDATE settings SET Image = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Image previews been turned `{onoff}`.")

        else:
            await ctx.send("Invalid setting. Valid choices are `on` or `off`.")

    @myset.command(name="rel")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def change_rel(self, ctx, onoff: str):
        """Toggles relationships on or off."""

        if onoff == "on":
            db.execute("UPDATE settings SET Rel = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Relationships have been turned `{onoff}`.")

        elif onoff == "off":
            db.execute("UPDATE settings SET Rel = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Relationships have been turned `{onoff}`.")

        else:
            await ctx.send("Invalid setting. Valid choices are `on` or `off`.")

    @myset.command(name="cha")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def cha(self, ctx, onoff: str):
        """Toggles characters on or off."""

        if onoff == "on":
            db.execute("UPDATE settings SET Ch = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Characters have been turned `{onoff}`.")

        elif onoff == "off":
            db.execute("UPDATE settings SET Ch = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Characters have been turned `{onoff}`.")

        else:
            await ctx.send("Invalid setting. Valid choices are `on` or `off`.")

    @myset.command(name="tag")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def change_tag(self, ctx, onoff: str):
        """Toggles additional tags on or off."""

        if onoff == "on":
            db.execute("UPDATE settings SET AddTags = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Additional tags have been turned `{onoff}`.")

        elif onoff == "off":
            db.execute("UPDATE settings SET AddTags = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Additional tags been turned `{onoff}`.")

        else:
            await ctx.send("Invalid setting. Valid choices are `on` or `off`.")

    @myset.command(name="sum")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def change_sum(self, ctx, onoff: str):
        """Toggles summary on or off."""  # noqa

        if onoff == "on":
            db.execute("UPDATE settings SET Summ = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Summary has been turned `{onoff}`.")

        elif onoff == "off":
            db.execute("UPDATE settings SET Summ = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Summary has been turned `{onoff}`.")

        else:
            await ctx.send("Invalid setting. Valid choices are `on` or `off`.")

    @myset.command(name="len")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def change_len(self, ctx, length: int):
        """Sets the character length of the summary. Default is 700. Must be
 between 20 and 700. To completely remove summary use `<p>settings sum off`.
        """

        if length < 20 or length > 700:
            await ctx.send("Invalid length. Must be 20-700 characters. To hide summary use `<p>settings sum off` instead.")  # noqa

        else:
            db.execute("UPDATE settings SET SumLength = ? WHERE GuildID = ?", length, ctx.guild.id)  # noqa
            await ctx.send(f"Summary length has been set to `{length}`.")

    @myset.command(name="del")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def change_del(self, ctx, onoff: str):
        """Toggles link delete on or off. Set to off by default."""  # noqa

        if onoff == "on":
            channel = ctx.channel
            exp = """**WARNING!** This will delete the entire message containing the AO3 link, \
which will delete any additional information the user posts. If you would \
like to suppress the default Discord embed consider instructing members to \
use `< >` around their link.
***Please confirm you want to set the bot to delete the user's message by \
sending `yes`. Update will cancel automatically after 15 seconds.***
"""

            await ctx.send(exp)

            def is_yes(m):
                return m.content == 'yes' and m.channel == channel

            try:
                await self.bot.wait_for('message', check=is_yes, timeout=15.0)
                db.execute("UPDATE settings SET DelLink = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
                await ctx.send(f"Delete link has been turned `{onoff}`.")

            except asyncio.TimeoutError:
                return await ctx.channel.send('Setting update cancelled.')

        elif onoff == "off":
            db.execute("UPDATE settings SET DelLink = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Delete link has been turned `{onoff}`.")

        else:
            await ctx.send("Invalid setting. Valid choices are `on` or `off`.")

    @myset.command(name="cpub")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def change_cpub(self, ctx, onoff: str):
        """Toggles publishing date row for chapters on or off."""

        if onoff == "on":
            db.execute("UPDATE settings SET cPubInfo = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Chapter publishing date row has been turned `{onoff}`.")  # noqa

        elif onoff == "off":
            db.execute("UPDATE settings SET cPubInfo = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Chapter publishing date row has been turned `{onoff}`.")  # noqa

        else:
            await ctx.send("Invalid setting. Valid choices are `on` or `off`.")

    @myset.command(name="cfan")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def change_cfan(self, ctx, onoff: str):
        """Toggles fandoms for chapter updates on or off."""

        if onoff == "on":
            db.execute("UPDATE settings SET cFan = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Chapter fandoms for have been turned `{onoff}`.")

        elif onoff == "off":
            db.execute("UPDATE settings SET cFan = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Chapter fandoms have been turned `{onoff}`.")

        else:
            await ctx.send("Invalid setting. Valid choices are `on` or `off`.")

    @myset.command(name="crel")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def change_crel(self, ctx, onoff: str):
        """Toggles chapter relationships on or off."""

        if onoff == "on":
            db.execute("UPDATE settings SET cRel = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Chapter relationships have been turned `{onoff}`.")  # noqa

        elif onoff == "off":
            db.execute("UPDATE settings SET cRel = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Chapter relationships have been turned `{onoff}`.")  # noqa

        else:
            await ctx.send("Invalid setting. Valid choices are `on` or `off`.")

    @myset.command(name="ccha")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def ccha(self, ctx, onoff: str):
        """Toggles chapter characters on or off."""

        if onoff == "on":
            db.execute("UPDATE settings SET cCh = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Chapter characters have been turned `{onoff}`.")

        elif onoff == "off":
            db.execute("UPDATE settings SET cCh = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Chapter characters have been turned `{onoff}`.")

        else:
            await ctx.send("Invalid setting. Valid choices are `on` or `off`.")

    @myset.command(name="ctag")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def change_ctag(self, ctx, onoff: str):
        """Toggles additional tags for chapters on or off."""

        if onoff == "on":
            db.execute("UPDATE settings SET cAddTags = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Chapter additional tags have been turned `{onoff}`.")  # noqa

        elif onoff == "off":
            db.execute("UPDATE settings SET cAddTags = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Chapter additional tags been turned `{onoff}`.")

        else:
            await ctx.send("Invalid setting. Valid choices are `on` or `off`.")

    @myset.command(name="csum")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def change_csum(self, ctx, onoff: str):
        """Toggles chapter summary on or off."""  # noqa

        if onoff == "on":
            db.execute("UPDATE settings SET cSumm = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Chapter summary has been turned `{onoff}`.")

        elif onoff == "off":
            db.execute("UPDATE settings SET cSumm = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Chapter summary has been turned `{onoff}`.")

        else:
            await ctx.send("Invalid setting. Valid choices are `on` or `off`.")

    @myset.command(name="clen")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def change_clen(self, ctx, length: int):
        """Sets the character length of the chapter summary. Default is 700. \
Must be between 20 and 700. To completely remove summary use `<p>settings sum \
off`.
        """

        if length < 20 or length > 700:
            await ctx.send("Invalid length. Must be 20-700 characters. To hide chapter summary use `<p>settings sum off` instead.")  # noqa

        else:
            db.execute("UPDATE settings SET cSumLength = ? WHERE GuildID = ?", length, ctx.guild.id)  # noqa
            await ctx.send(f"Chapter summary length has been set to `{length}`.")  # noqa

    @myset.command(name="cdel")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def change_cdel(self, ctx, onoff: str):
        """Toggles the setting to delete the chapter command. Set to \
off by default."""  # noqa

        if onoff == "on":
            db.execute("UPDATE settings SET DelUpdate = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Delete chapter commmand has been turned `{onoff}`.")  # noqa

        elif onoff == "off":
            db.execute("UPDATE settings SET DelUpdate = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Delete chapter command has been turned `{onoff}`.")  # noqa

        else:
            await ctx.send("Invalid setting. Valid choices are `on` or `off`.")

    @myset.command(name="derr")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def change_derr(self, ctx, onoff: str):
        """Toggles the setting to delete the chapter command. Set to \
off by default."""  # noqa

        if onoff == "on":
            db.execute("UPDATE settings SET DelErr = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send("Bot has been set to automatically delete error \
messages related to chapter updates commands.")

        elif onoff == "off":
            db.execute("UPDATE settings SET DelErr = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send("Auto deletion of error messages related to \
chapter update commands has been turned off.")

        else:
            await ctx.send("Invalid setting. Valid choices are `on` or `off`.")

    @myset.command(name="chdel")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def change_chapterdelete(self, ctx, onoff: str):
        """Deletes fic links which contain chapter specific info and which \
are posted without using `$update` command. Instructs users that chapter links \
must use `$update [chapter#] [link]` in this server."""  # noqa

        if onoff == "on":
            db.execute("UPDATE settings SET DelChapter = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send("Chapter links will not be autodetected. Users \
must use `$update [chapter#] [link]` in this server to post chapter updates.")

        elif onoff == "off":
            db.execute("UPDATE settings SET DelChapter = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send("Chapter links will be autodetected.")

        else:
            await ctx.send("Invalid setting. Valid choices are `on` or `off`.")

    @myset.command(name="dcha")
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @cooldown(1, 10, commands.BucketType.guild)
    async def change_deletechaptercommand(self, ctx, onoff: str):
        """Deletes chapter command executions."""  # noqa

        if onoff == "on":
            db.execute("UPDATE settings SET DelUpdate = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send("Chapter commands will be deleted after execution.")

        elif onoff == "off":
            db.execute("UPDATE settings SET DelUpdate = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send("Chapter commands will not be deleted.")

        else:
            await ctx.send("Invalid setting. Valid choices are `on` or `off`.")

    @myset.command(name="show", aliases=["view"],
                   brief="Shows the server's settings")
    @commands.guild_only()
    async def show_settings(self, ctx):

        pre = db.field("SELECT Prefix FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        ign = db.field("SELECT Ign FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        pub = db.field("SELECT PubInfo FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        fan = db.field("SELECT Fan FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        rel = db.field("SELECT Rel FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        cha = db.field("SELECT Ch FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        ta = db.field("SELECT AddTags FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        summ = db.field("SELECT Summ FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        summlen = db.field("SELECT SumLength FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        dellink = db.field("SELECT DelLink FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        cpub = db.field("SELECT cPubInfo FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        cfan = db.field("SELECT cFan FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        crel = db.field("SELECT cRel FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        ccha = db.field("SELECT cCh FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        cta = db.field("SELECT cAddTags FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        csumm = db.field("SELECT cSumm FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        csummlen = db.field("SELECT cSumLength FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        delcom = db.field("SELECT DelUpdate FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        delerr = db.field("SELECT DelErr FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        delch = db.field("SELECT DelChapter FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa
        image = db.field("SELECT Image FROM settings WHERE GuildID = ?", ctx.guild.id)  # noqa

        pref = f"```fix\n {pre}```Use `<p>prefix set` to change.\n\ufeff"
        igno = f"```fix\n {ign}```Use `<p>ignore set` to change.\n\ufeff"

        if pub == "on":
            pubin = f"```diff\n+ {pub}```***If off, hides the row with publishing \
dates in fic link embeds.***\nUse `<p>settings pub [on or off]` to change.\n\ufeff"  # noqa
        else:
            pubin = f"```diff\n- {pub}```***If off, hides the row with publishing \
dates in fic link embeds.***\nUse `<p>settings pub [on or off]` to change.\n\ufeff"  # noqa

        if fan == "on":
            fand = f"```diff\n+ {fan}```***If off, hides fandoms in fic link \
embeds.***\nUse `<p>settings fan [on or off]` to change.\n\ufeff"
        else:
            fand = f"```diff\n- {fan}```***If off, hides fandoms in fic link \
embeds.***\nUse `<p>settings fan [on or off]` to change.\n\ufeff"

        if rel == "on":
            rela = f"```diff\n+ {rel}```***If off, hides relationships in fic \
link embeds.***\nUse `<p>settings rel [on or off]` to change.\n\ufeff"
        else:
            rela = f"```diff\n- {rel}```***If off, hides relationships in fic \
link embeds.***\nUse `<p>settings rel [on or off]` to change.\n\ufeff"

        if cha == "on":
            char = f"```diff\n+ {cha}```***If off, hides characters in fic \
link embeds.***\nUse `<p>settings cha [on or off]` to change.\n\ufeff"
        else:
            char = f"```diff\n- {cha}```***If off, hides characters in fic \
link embeds.***\nUse `<p>settings cha [on or off]` to change.\n\ufeff"

        if ta == "on":
            tags = f"```diff\n+ {ta}```***If off, hides additional tags in fic \
link embeds.***\nUse `<p>settings tag [on or off]` to change.\n\ufeff"
        else:
            tags = f"```diff\n- {ta}```***If off, hides additional tags in fic \
link embeds.***\nUse `<p>settings tag [on or off]` to change.\n\ufeff"

        if summ == "on":
            sum = f"```diff\n+ {summ}```***If off, hides summary in fic link \
embeds.***\nUse `<p>settings sum [on or off]` to change.\n\ufeff"
        else:
            sum = f"```diff\n- {summ}```***If off, hides summary in fic link \
embeds.***\nUse `<p>settings sum [on or off]` to change.\n\ufeff"

        if image == "on":
            img = f"```diff\n+ {image}```***If off, hides image preview in fic \
link embeds.***\nUse `<p>settings img [on or off]` to change.\n\ufeff"
        else:
            img = f"```diff\n- {image}```***If off, hides image preview in fic \
link embeds.***\nUse `<p>settings sum [on or off]` to change.\n\ufeff"

        sumlen = f"```fix\n {summlen}```***Sets the maximum number of \
characters for the summary. Default is 700. Must be between 20 and \
700.***\nUse `<p>settings len [number]` to change.\n\ufeff"

        if dellink == "on":
            delli = f"```diff\n+ {dellink}```***If off, original user message \
will not be deleted.*** Default is off so members may post any message with \
their link. Please consider asking members to surround their links with \
`< >` to hide the default Discord display instead.\nUse \
`<p>settings del [on or off]` to change."
        else:
            delli = f"```diff\n- {dellink}```***If off, original user message \
will not be deleted.*** Default is off so members may post any message with \
their link. Please consider asking members to surround their links with \
`< >` to hide the default Discord display instead.\nUse \
`<p>settings del [on or off]` to change."

        if cpub == "on":
            cpubin = f"```diff\n+ {cpub}```***If off, hides the row with publishing \
dates in chapter update embeds.***\nUse `<p>settings cpub [on or off]` to change.\n\ufeff"  # noqa
        else:
            cpubin = f"```diff\n- {cpub}```***If off, hides the row with publishing \
dates in chapter update embeds.***\nUse `<p>settings cpub [on or off]` to change.\n\ufeff"  # noqa

        if cfan == "on":
            cfand = f"```diff\n+ {cfan}```***If off, hides fandoms in \
chaper update embeds.***\nUse `<p>settings cfan [on or off]` to change.\n\ufeff"  # noqa
        else:
            cfand = f"```diff\n- {cfan}```***If off, hides fandoms in \
chapter update embeds.***\nUse `<p>settings cfan [on or off]` to change.\n\ufeff"  # noqa

        if crel == "on":
            crela = f"```diff\n+ {crel}```***If off, hides relationships in \
chapter update embeds.***\nUse `<p>settings crel [on or off]` to change.\n\ufeff"  # noqa
        else:
            crela = f"```diff\n- {crel}```***If off, hides relationships in \
chapter update embeds.***\nUse `<p>settings crel [on or off]` to change.\n\ufeff"  # noqa

        if ccha == "on":
            cchar = f"```diff\n+ {ccha}```***If off, hides characters in \
chapter update embeds.***\nUse `<p>settings ccha [on or off]` to change.\n\ufeff"  # noqa
        else:
            cchar = f"```diff\n- {ccha}```***If off, hides characters in \
chapter update embeds.***\nUse `<p>settings ccha [on or off]` to change.\n\ufeff"  # noqa

        if cta == "on":
            ctags = f"```diff\n+ {cta}```***If off, hides additional tags in \
chapter update embeds.***\nUse `<p>settings ctag [on or off]` to change.\n\ufeff"  # noqa
        else:
            ctags = f"```diff\n- {cta}```***If off, hides additional tags in fic \
link embeds.***\nUse `<p>settings ctag [on or off]` to change.\n\ufeff"

        if csumm == "on":
            csum = f"```diff\n+ {csumm}```***If off, hides summary in fic link \
embeds.***\nUse `<p>settings csum [on or off]` to change.\n\ufeff"
        else:
            csum = f"```diff\n- {csumm}```***If off, hides summary in fic link \
embeds.***\nUse `<p>settings csum [on or off]` to change.\n\ufeff"

        csumlen = f"```fix\n {csummlen}```***Sets the maximum number of \
characters for the summary in the chapter update embed. Default is 700. Must \
be between 20 and 700.***\nUse `<p>settings clen [number]` to change.\n\ufeff"

        if delcom == "on":
            delco = f"```diff\n+ {delcom}```***If off, any use of `$update` or\
its aliases will not be deleted. Default is off.***\nUse \
`<p>settings cdel [on or off]` to change."
        else:
            delco = f"```diff\n- {delcom}```***If off, any use of `$update` or\
its aliases will not be deleted. Default is off.***\nUse \
`<p>settings cdel [on or off]` to change."

        if delerr == "on":
            deler = f"```diff\n+ {delerr}```***If off, error messages related \
to use of `$update` and its aliases will not be autodeleted by the bot. \
Default is off.***\nUse `<p>settings derr [on or off]` to change."
        else:
            deler = f"```diff\n- {delerr}```***If off, error messages related \
to use of `$update` and its aliases will not be autodeleted by the bot. \
Default is off.***\nUse `<p>settings derr [on or off]` to change."

        if delch == "on":
            delc = f"```diff\n+ {delch}```***If off, links to chapters will \
post as if normal fic links unless users use `$update` command. If on, users \
will be reminded to use command instead. Default is \
off.***\nUse `<p>settings chdel [on or off]` to change."
        else:
            delc = f"```diff\n- {delch}```***If off, links to chapters will \
post as if normal fic links unless users use `$update` command. If on, users \
will be reminded to use command instead. Default is \
off.***\nUse `<p>settings chdel [on or off]` to change."

        embed1 = discord.Embed(title="Current Server Settings", color=0x2F3136).add_field(name="Prefix", value=pref, inline=False).add_field(name="Ignore Symbol", value=igno, inline=False).add_field(name="Publishing Info", value=pubin, inline=False).add_field(name="Fandoms", value=fand, inline=False).add_field(name="Relationships", value=rela, inline=False)  # noqa

        embed2 = discord.Embed(title="Current Server Settings", color=0x2F3136).add_field(name="Characters", value=char, inline=False).add_field(name="Tags", value=tags, inline=False).add_field(name="Summary", value=sum, inline=False).add_field(name="Image Previews", value=img, inline=False).add_field(name="Summary Length", value=sumlen, inline=False)  # noqa

        embed3 = discord.Embed(title="Current Server Settings", color=0x2F3136).add_field(name="Delete Link", value=delli, inline=False).add_field(name="Chapter Publishing Info", value=cpubin, inline=False).add_field(name="Chapter Fandoms", value=cfand, inline=False).add_field(name="Chapter Relationships", value=crela, inline=False).add_field(name="Chapter Characters", value=cchar, inline=False)  # noqa

        embed4 = discord.Embed(title="Current Server Settings", color=0x2F3136).add_field(name="Chapter Tags", value=ctags, inline=False).add_field(name="Chapter Summary", value=csum, inline=False).add_field(name="Chapter Summary Length", value=csumlen, inline=False).add_field(name="Delete Update Command", value=delco, inline=False).add_field(name="Delete Update Errors", value=deler, inline=False)  # noqa

        embed5 = discord.Embed(title="Current Server Settings", color=0x2F3136).add_field(name="Update Command Enforced", value=delc, inline=False)  # noqa

        embeds = [
            embed1,
            embed2,
            embed3,
            embed4,
            embed5
        ]

        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()


def setup(bot):
    bot.add_cog(settings(bot))
