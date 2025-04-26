import ast
import asyncio
from config import acc1, acc2
from telethon import TelegramClient, types
from telethon.sessions import StringSession
from telethon.tl.functions.messages import SendReactionRequest


async def process_account(account_data, chat_list):
    client = TelegramClient(
        StringSession(account_data['session']),
        account_data['api_id'],
        account_data['api_hash']
    )

    try:
        await client.start()
        print(f"Account {account_data.get('name', '')} started")

        chat_entities = []
        for chat_id in chat_list:
            try:
                chat = await client.get_entity(chat_id)
                chat_entities.append(chat)
                print(f"Found chat: {chat_id}")
            except Exception as e:
                print(f"Error finding chat {chat_id}: {e}")

        if not chat_entities:
            return

        last_message_ids = {chat.id: None for chat in chat_entities}
        message_counters = {chat.id: 0 for chat in chat_entities}

        while True:
            for chat in chat_entities:
                try:
                    last_msg = await client.get_messages(chat, limit=1)
                    if not last_msg:
                        continue

                    current_msg = last_msg[0]
                    if current_msg.id != last_message_ids[chat.id]:
                        last_message_ids[chat.id] = current_msg.id
                        message_counters[chat.id] += 1
                        print(f"New message in {chat.id} (#{message_counters[chat.id]})")

                        if message_counters[chat.id] % 2 == 0:
                            try:
                                await client(SendReactionRequest(
                                    peer=chat,
                                    msg_id=current_msg.id,
                                    reaction=[types.ReactionEmoji(emoticon='❤️')]
                                ))
                                print(f"Reaction added in {chat.id}")
                            except Exception as e:
                                print(f"Reaction error in {chat.id}: {e}")

                except Exception as e:
                    print(f"Error in {chat.id}: {e}")

            await asyncio.sleep(1)

    except Exception as e:
        print(f"Account error: {e}")
    finally:
        await client.disconnect()


async def main():
    accounts = []
    accounts.append(ast.literal_eval(acc1))
    accounts.append(ast.literal_eval(acc2))

    chat_list = ['kvdfurry']

    if not chat_list:
        print("No chats provided")
        return

    tasks = [process_account(account, chat_list) for account in accounts]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
