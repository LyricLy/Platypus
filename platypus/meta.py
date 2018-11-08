import discord

from platypus import command


class Meta:
    GITHUB_LINK = "https://github.com"

    def __init__(self, bot):
        self.bot = bot

    @command()
    async def about(self, ctx):
        info = await self.bot.application_info()

        if self.bot._bot_link is None:
            bot_url = None
        elif not self.bot._bot_link:
            bot_url = f"{self.GITHUB_LINK}/{info.owner.name}/{info.name}"
        else:
            bot_url = self.bot._bot_link

        if self.bot._author_link is None:
            avatar_url = None
        elif not self.bot._author_link:
            avatar_url = f"{self.GITHUB_LINK}/{info.owner.name}"
        else:
            avatar_url = self.bot._author_link

        embed = discord.Embed(title=info.name, description=self.bot.description, url=bot_url)
        embed.add_field(name="Author", value=f"[{info.owner.name}]({avatar_url})" if avatar_url else info.owner.name)
        embed.add_field(name="Total servers", value=str(len(self.bot.guilds)))
        embed.add_field(name="Total users", value=str(len(list(self.bot.get_all_members()))))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Meta(bot))
