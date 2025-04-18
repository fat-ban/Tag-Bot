from telethon import events, functions, types
from utilities import client
from tagAll import tagAll
from tagAdmins import tagAdmins

# check if the sender is an admin
async def is_admin(event):
    if event.is_private:
        return False
    user = await event.client.get_permissions(event.chat_id, event.sender_id)
    return user.is_admin

# handle tag all members command
@client.on(events.NewMessage(pattern=r"/(tagall|ناديلي_الفحلات)"))
async def handler(event):
    if await is_admin(event):
        await tagAll(event)
    else:
        await event.reply("🚫 المشرفون فقط من يمكنهم استخدام هذا البوت")
        
# handle /admins command
@client.on(events.NewMessage(pattern='/admins'))
async def handler(event):
    if await is_admin(event):
        await tagAdmins(event)
    else:
        await event.reply("🚫 المشرفون فقط من يمكنهم استخدام هذا البوت")

# handle /stop command
@client.on(events.NewMessage(pattern='/stop'))
async def handler_stop(event):
    if await is_admin(event):
        await event.reply("🛑 تم إيقاف تشغيل البوت.")
        await client.disconnect()  # This will stop the bot
    else:
        await event.reply("🚫 المشرفون فقط يمكنهم إيقاف تشغيل البوت")

async def set_bot_commands():
    await client(functions.bots.SetBotCommandsRequest(
        scope=types.BotCommandScopeDefault(),
        lang_code='ar',
        commands=[
            types.BotCommand(command='tagall', description='مناداة جميع الأعضاء'),
            types.BotCommand(command='admins', description='مناداة جميع المشرفين'),
            types.BotCommand(command='stop', description='إيقاف تشغيل البوت'),
        ]
    ))

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    await set_bot_commands()
    await event.respond("🤖 البوت جاهز! اكتب '/' لرؤية الأوامر.")

# running bot
print("Bot is running...")
client.run_until_disconnected()
