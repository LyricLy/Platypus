class DiscordInput:
    def __init__(self, ctx):
        self.ctx = ctx
        self.buffer = ""

    async def read(self, amount):
        response = []
        for _ in range(amount):
            if not self.buffer:
                def check(message):
                    return (message.channel == self.ctx.channel
                        and message.author != self.ctx.bot.user
                        and message.author == self.ctx.author)
                message = await self.ctx.bot.wait_for("message", check=check)
                self.buffer = message.content + "\n"
            response.append(self.buffer[0])
            self.buffer = self.buffer[1:]
        return "".join(response)

    async def readline(self):
        result = []
        while result[-1] != "\n":
            result.append(await self.read(1))
        return "".join(result)


class DiscordOutput:
    def __init__(self, message):
        self.message = message
        self.output = ""

    async def write(self, text):
        self.output += text
        if text.endswith("\n"):
            await self.flush()

    async def flush(self):
        await self.message.edit(content="```\n" + self.output.replace("`", "\u200b`") + "\n```")
