import utilities
import asyncio

async def tagAll(message):
    # get group id
    chat_id = message.chat_id
    
    # get group users
    group_users = utilities.client.iter_participants(chat_id)
    max_length_per_message = 4080  # telegram allow arround 4080 chars per message
    batch = []
    user_count = 1

    async for user in group_users:
        if user.bot:
            # if the user is a bot pass to next iteration
            continue
        if user.username:
            # get username
            tag = f'{user_count}- @{user.username}'
        elif user.first_name:
            # user user id + user firstname
            tag = f'{user_count}- <a href="tg://user?id={user.id}">{user.first_name}</a>'
        else:
            continue

        user_count += 1
        batch.append(tag)
        
        # check if the message length exceeds Telegram max message length
        if sum(len(line) for line in batch) + len(batch) > max_length_per_message:
            # send message
            await message.reply("\n".join(batch), parse_mode="html")
            # wait until message is sent
            await asyncio.sleep(2)
            # re-initialize the message batch to tag the rest of the users
            batch = []
            
    # send the last message batch if exists
    if batch:
        await message.reply("\n".join(batch), parse_mode="html")




















# import utilities
# import asyncio

# async def tagAll(message):
#     # get group id
#     chat_id = message.chat_id
    
#     # get group members
#     participants = await utilities.client.get_participants(chat_id)
    
#     tagged_users = ""   
#     user_counts = {"users": 1, "bots": 1}
    
#     # push all group username or first_name into "tagged_users"
#     for user in participants:
#         if user.username and not user.bot:
#             tagged_users += f"{user_counts['users']}- @{user.username}\n"
#             user_counts["users"] += 1
#         elif user.username is None and user.first_name:
#             tagged_users += f'{user_counts["users"]}- <a href="tg://user?id={user.id}">{user.first_name}</a>\n'
#             user_counts["users"] += 1
#         elif user.bot:
#             user_counts["bots"] += 1
 
#     # split "usernames" to separate usernames, each username in a list cell
#     usernames = tagged_users.strip().split("\n")
#     usernames = [user.strip() for user in usernames]
#     max_length_per_message = 4080 # max length of Telegram message
#     message = ""

#     index = 0
#     while index < len(usernames):
#         username = usernames[index]
        
#         # if the username is empty pass to the next iteration
#         if username == "":
#             index += 1
#             continue
        
#         # if the message length is lower than max Telegram message length push username
#         # else send message and overwrite "message"
#         if len(message) < max_length_per_message:
#             message += f"{username}\n"
#         else:
#             # send message to group
#             await message.reply(message.strip("\n"), parse_mode="html")
            
#             # wait until the message is sent
#             await asyncio.sleep(2)
            
#             # overwrite "message"
#             message = f"{username}\n"

#         index += 1
    
#     # send last "message" usernames list
#     if message.strip():
#         await utilities.client.send_message(chat_id, message.strip("\n"), parse_mode="html")

