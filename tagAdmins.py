import utilities
import asyncio
from telethon.tl.types import ChannelParticipantsAdmins

async def tagAdmins(message):
    chat_id = message.chat_id

    # get admins of group
    admins = await utilities.client.get_participants(chat_id, filter=ChannelParticipantsAdmins)

    tagged_users = ""   
    user_count = 1

    # tag only admins
    for user in admins:
        if user.bot:
            continue
        if user.username:
            tagged_users += f"{user_count}- @{user.username}\n"
        else:
            name = user.first_name or "Admin"
            tagged_users += f'{user_count}- <a href="tg://user?id={user.id}">{name}</a>\n'
        
        user_count += 1

    # push admins group username or first_name into "admins"
    admins = tagged_users.strip().split("\n")
    admins = [u.strip() for u in admins if u.strip()]
    max_length_per_message = 4080
    chunk = ""

    for admin in admins:
        if len(chunk) + len(admin) + 1 < max_length_per_message:
            chunk += f"{admin}\n"
        else:
            await message.reply(chunk.strip(), parse_mode="html")
            await asyncio.sleep(2)
            chunk = f"{admin}\n"

    # Send the last chunk
    if chunk.strip():
        await utilities.client.send_message(chat_id, chunk.strip(), parse_mode="html")