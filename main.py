from telethon import events
from utilities import client
from tagAll import tagAll
from tagAdmins import tagAdmins

# check if the sender is an admin
async def is_admin(event):
    if event.is_private:
        return False
    user = await event.client.get_permissions(event.chat_id, event.sender_id)
    return user.is_admin

# handle /all command
@client.on(events.NewMessage(pattern='/all'))
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

# running bot
print("Bot is running...")
client.run_until_disconnected()
