
#已废弃



from nonebot import on_command
from nonebot.adapters.qq import MessageSegment

# 注册命令处理器
menu = on_command("菜单")

@menu.handle()
async def show_menu():
    # 创建带按钮的消息
    message = MessageSegment.text("请选择操作：") + MessageSegment.keyboard(
        [
            [MessageSegment.action_button("按钮1", "action1", "primary")],
            [MessageSegment.action_button("按钮2", "action2", "secondary")],
            [MessageSegment.action_button("按钮3", "action3", "danger")]
        ]
    )
    await menu.send(message)
from nonebot import on_message
from nonebot.adapters.qq import Event, MessageEvent

button_click = on_message()

@button_click.handle()
async def handle_click(event: MessageEvent):
    if hasattr(event, "event_type") and event.event_type == "INTERACTION_CREATE":
        # 获取按钮ID
        button_id = event.data.get("button_id")
        if button_id == "action1":
            await button_click.finish("你点击了按钮1")
        elif button_id == "action2":
            await button_click.finish("你点击了按钮2")