from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg

url = on_command("url", rule=to_me(),priority=10, block=True)
@url.handle()
async def handle_url(args: Message = CommandArg()):
    await url.finish("https://test. com")