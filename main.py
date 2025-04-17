from telethon import events
from utilities import client
from tagAll import run

@client.on(events.NewMessage(pattern='/all'))
async def handler(event):
    await run(event)

print("Bot is running...")
client.run_until_disconnected()