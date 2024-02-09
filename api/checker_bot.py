from telethon import TelegramClient, events
from dotenv import load_dotenv
from time import sleep
import os

#* take environment variables from .env.
load_dotenv()
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_API_HASH= os.getenv('BOT_API_HASH')

client = TelegramClient(BOT_API_HASH, API_ID, API_HASH)


async def message_printer(event):
    print(event.message.message)

async def status(event):
    await event.respond("Ok")

class CheckInfo:
        def __init__(self, add, lost ):
            self.add = add
            self.lost = lost

            self.msg = f"""✔️ find: {' '.join(add)}
            ❌ lost: {' '.join(lost) if lost.__len__() > 0 else "No lost users" }
            📋 added:{add.__len__()}; lost:{lost.__len__()} """


async def check_users(event):
    # Check if the user has been added
    args = event.message.message.split()[1:]

    channel = args[0]
    users = args[1:]

    add = []
    lost = users[:]

    print(f"🔍 search start {len(users)} users", )
    await event.respond(f"🔍 search start {len(users)} users")

    for name in users:
        sleep(1)
        print(f"searched:{name}")
        async for user in client.iter_participants(channel, search=name):
            print(name, user.username)
            if (user.username.removeprefix("@") == name.removeprefix("@")):
                print(f"✔️ find: {user.username}")
                add.append(name)
                lost.remove(name)

    Info = CheckInfo(add, lost)
    print(Info.msg, "\n🔍 search end" )
    await event.respond(Info.msg)
    return Info

"""
    # Show all user IDs in a chat
    async for user in client.iter_participants(chat):
        print(user.id)

    # Search by name
    async for user in client.iter_participants(chat, search='name'):
        print(user.username)

    # Filter by admins
    from telethon.tl.types import ChannelParticipantsAdmins
    async for user in client.iter_participants(chat, filter=ChannelParticipantsAdmins):
        print(user.first_name)
"""



async def main():
    await client.start()
    # Добавьте обработчик событий в вашу функцию main
    client.add_event_handler(message_printer, events.NewMessage())
    client.add_event_handler(status, events.NewMessage(pattern="/status"))
    client.add_event_handler(check_users, events.NewMessage(pattern="/check"))

    print("Run BOT remover ...")
    await client.run_until_disconnected()



with client:
    client.loop.run_until_complete(main())

