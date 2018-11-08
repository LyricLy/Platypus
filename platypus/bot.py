# TODO: Encode some form of information in status; either what stage of startup the bot is in or notify fatal errors

from traceback import format_tb

from discord.ext import commands

from platypus.commands import invoke_help, group
from platypus.paginator import HelpPaginator


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_extension("platypus.meta")

        if kwargs.pop("pretty_help", True):
            self.remove_command("help")
            self.add_command(self._help)
        self._help_missing_arg = kwargs.pop("help_missing_arg", True)
        self._bot_link = kwargs.pop("bot_link", False)
        self._author_link = kwargs.pop("author_link", False)

        self._general_error_msg = kwargs.pop("general_error_msg", None)
        self._missing_argument_msg = kwargs.pop("missing_argument_msg", None)
        self._bad_argument_msg = kwargs.pop("bad_argument_msg", None)
        self._not_found_msg = kwargs.pop("not_found_msg", None)

    @commands.command(name="help")
    async def _help(self, ctx, *command):
        """Show help about a specific command or all commands."""
        command = " ".join(command) or None
        if command is None:
            p = await HelpPaginator.from_bot(ctx)
        else:
            entity = self.get_cog(command) or self.get_command(command)
            if entity is None:
                clean = command.replace("@", "@\u200b")
                return await ctx.send(f"Command or category '{clean}' not found.")
            elif isinstance(entity, commands.Command):
                p = await HelpPaginator.from_command(ctx, entity)
            else:
                p = await HelpPaginator.from_cog(ctx, entity)
        await p.paginate()

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        print(f"ID: {self.user.id}")

    async def on_command_error(self, ctx, exc):
        exc = getattr(exc, "original", exc)

        if isinstance(exc, commands.MissingRequiredArgument):
            if self._missing_argument_msg is not None:
                await ctx.send(self._missing_argument_msg)
            if self._help_missing_arg:
                await invoke_help(ctx)
        elif isinstance(exc, commands.BadArgument):
            if self._bad_argument_msg is not None:
                await ctx.send(self._bad_argument_msg)
        elif isinstance(exc, commands.CommandNotFound):
            if self._not_found_msg is not None:
                await ctx.send(self._not_found_msg)
        else:
            if self._general_error_msg is not None:
                await ctx.send(self._general_error_msg)
            print(f"Ignoring exception in command '{ctx.command.name}'")
            print("".join(format_tb(exc.__traceback__)), end="")
            print(f"{type(exc).__name__}: {str(exc)}")

    def group(self, name=None, **kwargs):
        def decorator(func):
            result = group(name, **kwargs)(func)
            self.add_command(result)
            return result
        return decorator
