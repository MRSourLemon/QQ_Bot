from nonebot.adapters.qq import MessageEvent
from nonebot.plugin import on_command
from nonebot.rule import to_me
 
test = on_command("test", rule=to_me(), priority=10, block=True)
@test.handle()
async def test_method(message: MessageEvent):
    member_openid = message.get_user_id()
    await test.send(f"Your OpenID is: {member_openid}", at_sender=True)