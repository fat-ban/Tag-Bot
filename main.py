from telethon import events
from utilities import client
from tagAll import run

# handle /all command
@client.on(events.NewMessage(pattern='/all'))
async def handler(event):
    await run(event)

# running bot
print("Bot is running...")
client.run_until_disconnected()