import copy

from discord.ext import commands


command = commands.command


async def invoke_help(ctx):
    await ctx.invoke(ctx.bot.get_command('help'), *ctx.command.qualified_name.split())


class Group(commands.Group):
    def __init__(self, **kwargs):
        self.help_no_subcommand = kwargs.pop("help_no_subcommand", False)
        super().__init__(**kwargs)

    async def invoke(self, ctx):
        if self.help_no_subcommand:
            view = copy.copy(ctx.view)
            view.skip_ws()
            trigger = view.get_word()
            invoked_subcommand = self.all_commands.get(trigger, None)
            if invoked_subcommand is None:
                await invoke_help(ctx)
                return
        await super().invoke(ctx)

    async def reinvoke(self, ctx, *, call_hooks=False):
        if self.help_no_subcommand:
            view = copy.copy(ctx.view)
            view.skip_ws()
            trigger = view.get_word()
            invoked_subcommand = self.all_commands.get(trigger, None)
            if invoked_subcommand is None:
                await invoke_help(ctx)
                return
        await super().reinvoke(ctx, call_hooks=call_hooks)


def group(self, name=None, **kwargs):
    invoke_without_command = kwargs.pop("invoke_without_command", True)
    help_no_subcommand = kwargs.pop("help_no_subcommand", False)
    return command(name=name, cls=Group,
                   invoke_without_command=invoke_without_command, help_no_subcommand=help_no_subcommand, **kwargs)
