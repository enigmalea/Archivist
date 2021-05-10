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
like to supress the default Discord embed consider instructing members to use \
`< >` around their link or turning off link embed permissions in the \
channels where links are posted instead.
***Please confirm you want to set the bot to delete the user's message by \
sending `yes`. Update will cancel automatically after 5 seconds.***
"""

            await ctx.send(exp)

            def is_yes(m):
                return m.content == 'yes' and m.channel == channel

            try:
                await self.bot.wait_for('message', check=is_yes, timeout=5.0)
                db.execute("UPDATE settings SET DelLink = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
                await ctx.send(f"Delete link has been turned `{onoff}`.")

            except asyncio.TimeoutError:
                return await ctx.channel.send('Setting update cancelled.')

        elif onoff == "off":
            db.execute("UPDATE settings SET DelLink = ? WHERE GuildID = ?", onoff, ctx.guild.id)  # noqa
            await ctx.send(f"Delete link has been turned `{onoff}`.")

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

        sumlen = f"```fix\n {summlen}```***If off, summary is not hidden, sets \
the maximum number of characters for the summary. Default is 700. Must be \
between 10 and 700.***\nUse `<p>settings len [number]` to change.\n\ufeff"

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

        embed1 = discord.Embed(title="Current Server Settings", color=0x2F3136).add_field(name="Prefix", value=pref, inline=False).add_field(name="Ignore Symbol", value=igno, inline=False).add_field(name="Publishing Info", value=pubin, inline=False).add_field(name="Fandoms", value=fand, inline=False).add_field(name="Relationships", value=rela, inline=False)  # noqa

        embed2 = discord.Embed(title="Current Server Settings", color=0x2F3136).add_field(name="Characters", value=char, inline=False).add_field(name="Tags", value=tags, inline=False).add_field(name="Summary", value=sum, inline=False).add_field(name="Summary Length", value=sumlen, inline=False).add_field(name="Delete Link", value=delli, inline=False)  # noqa

        embeds = [
            embed1,
            embed2
        ]

        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()


def setup(bot):
    bot.add_cog(settings(bot))
