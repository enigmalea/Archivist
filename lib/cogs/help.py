
# //          Copyright Amber Whitlock aka enigmalea 2021
# // Distributed under the Boost Software License, Version 1.0.
# //    (See accompanying file LICENSE_1_0.txt or copy at
# //          https://www.boost.org/LICENSE_1_0.txt)

# Requires pip install discord-ext-menus
from typing import Optional

from discord import Embed
from discord.utils import get
from discord.ext.menus import MenuPages, ListPageSource
from discord.ext import commands
from discord.ext.commands import Cog

from ..db import db


def syntax(command):
    cmd_and_aliases = " | <p>".join([str(command), *command.aliases])
    params = []

    for key, value in command.params.items():
        if key == "cmd":
            key = "command"

            if key not in ("self", "ctx"):
                params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")  

    params = " ".join(params)

    return f"""<p>{cmd_and_aliases} {params}"""


class HelpMenu(ListPageSource):
    def __init__(self, ctx, data):
        self.ctx = ctx

        super().__init__(data, per_page=3)

    async def write_page(self, menu, fields=[]):
        name = self.ctx.guild.me.display_name
        sup = "Join the Support Server"
        supurl = "https://discord.gg/FzhC9bVFva"
        twit = "Official Twitter"
        twiturl = "https://twitter.com/_ArchivistBot_"
        web = "Website"
        weburl = "https://www.archivistbot.com"
        inv = "Invite to Your Server"
        invurl = "https://discord.com/api/oauth2/authorize?client_id=812505952959856690&permissions=294205549632&scope=bot"  
        ign = db.field("SELECT Ign FROM settings WHERE GuildID = ?", self.ctx.guild.id)  
        pre = db.field("SELECT Prefix FROM settings WHERE GuildID = ?", self.ctx.guild.id)  

        d = f"""**{name}** is a simple Discord bot which automatically detects \
AO3 links for works, series, and users and provides more detailed information \
from the AO3 website. Links should be detected no matter where they are in a \
message. Additional commands for other features are below.\n\nIf you have \
issues with the bot or suggestions for more features, please join the support \
server by clicking the link.\n\n__**To ignore a link:**__\nIf you would like \
to post an AO3 link without having the bot populate an embed, place a `{ign}` \
in front of the link:\n**Ex:** \
`{ign}https://archiveofourown.org/works/26353378`\n\n__**Important \
Links**__\n▸ [{sup}]({supurl})\n▸ [{web}]({weburl})\n▸ [{twit}]({twiturl})\n▸ \
[{inv}]({invurl})"""
        offset = (menu.current_page*self.per_page) + 1
        len_data = len(self.entries)

        embed = Embed(title=f"Help with {name}",
                      description=d,
                      color=0x2F3136)
        embed.set_footer(
            icon_url="https://i.imgur.com/Pv5jRoh.png",
            text=f"Server Prefix: <p> = {pre} | {offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} Commands"  
        )

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        return embed

    async def format_page(self, menu, entries):
        fields = []

        for entry in entries:
            fields.append((syntax(entry), entry.help or "No description."))  

        return await self.write_page(menu, fields)


class help(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def return_filtered_commands(self, walkable, ctx):
        filtered = []

        for c in walkable.walk_commands():
            try:
                if c.hidden:
                    continue

                elif c.parent:
                    continue

                await c.can_run(ctx)
                filtered.append(c)
            except commands.CommandError:
                continue

        return self.return_sorted_commands(filtered)

    def return_sorted_commands(self, commandList):
        return sorted(commandList, key=lambda x: x.name)

    async def cmd_help(self, ctx, command):
        pre = db.field("SELECT Prefix FROM settings WHERE GuildID = ?", ctx.guild.id)  
        embed = Embed(title=f"Help with `{pre}{command}`",
                      description=f"```{syntax(command)}```",
                      color=0x2F3136)
        embed.add_field(name="Command Description:", value=command.help)
        embed.set_footer(
            icon_url="https://i.imgur.com/Pv5jRoh.png",
            text=f"Server Prefix: <p> = {pre}"
        )
        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('help')

    @commands.command(name="help")
    @commands.guild_only()
    async def show_help(self, ctx, cmd: Optional[str]):
        '''
        Shows help for all commands the user has permissions to use.
        '''
        if isinstance(self.bot, commands.Command):
            filtered_commands = (
                list(set(self.bot.all_commands.values()))
                if hasattr(self.bot, "all_commands")
                else []
            )

        else:
            filtered_commands = await self.return_filtered_commands(self.bot, ctx)  

        if cmd is None:
            menu = MenuPages(source=HelpMenu(ctx, list(filtered_commands)),
                             delete_message_after=True,
                             timeout=60.0)
            await menu.start(ctx)

        else:
            if (command := get(self.bot.commands, name=cmd)):
                await self.cmd_help(ctx, command)

            elif cmd not in filtered_commands and self.bot.get_command(cmd) is not None:  
                main = self.bot.get_command(cmd)
                await self.cmd_help(ctx, main)

            else:
                await ctx.send("That command does not exist.")


def setup(bot):
    bot.add_cog(help(bot))
