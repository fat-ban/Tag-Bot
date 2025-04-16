import utilities
import asyncio

async def run(message):
    chat_id = message.chat_id
    participants = await utilities.client.get_participants(chat_id)

    tagged_users = ""
    user_counts = {"humans": 1, "bots": 1}
    
    for user in participants:
        if user.username and not user.bot:
            tagged_users += f"{user_counts['humans']}- @{user.username}\n"
            user_counts["humans"] += 1
        elif user.username is None and user.first_name:
            tagged_users += f"{user_counts['humans']}- {user.first_name}\n"
            user_counts["humans"] += 1
        elif user.bot:
            user_counts["bots"] += 1
 
    usernames = tagged_users.strip().split("\n")
    usernames = [user.strip() for user in usernames]
    max_length_per_message = 4080
    message_chunk = ""

    index = 0
    while index < len(usernames):
        username = usernames[index]

        if username == "":
            index += 1
            continue

        if len(message_chunk) < max_length_per_message:
            message_chunk += f"{username}\n"
        else:
            await message.reply(message_chunk.strip("\n"))
            await asyncio.sleep(2)
            message_chunk = f"{username}\n"

        index += 1

    if message_chunk.strip():
        await utilities.client.send_message(chat_id, message_chunk.strip("\n"))
