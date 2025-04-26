import ast
from telethon import TelegramClient, events, types
from telethon.sessions import StringSession
import asyncio
from telethon.tl.functions.messages import SendReactionRequest

async def main():
    acc_str = input().strip()
    account = ast.literal_eval(acc_str)
    CHAT_ID = 'kvdfurry'
    reaction_emoji = '❤️'
    message_counter = 0
    last_message_id = None

    client = TelegramClient(StringSession(account['session']), account['api_id'], account['api_hash'])

    try:
        await client.start()
        print("Bot started")

        try:
            chat = await client.get_entity(CHAT_ID)
            print(f"Chat found: {chat.id}")
        except Exception as e:
            print(f"Chat error: {e}")
            return

        while True:
            try:
                last_msg = await client.get_messages(chat, limit=1)
                if not last_msg:
                    await asyncio.sleep(5)
                    continue

                current_msg = last_msg[0]
                if current_msg.id != last_message_id:
                    last_message_id = current_msg.id
                    message_counter += 1
                    print(f"New message #{message_counter}")

                    if message_counter % 2 == 0:
                        try:
                            await client(SendReactionRequest(
                                peer=chat,
                                msg_id=current_msg.id,
                                reaction=[types.ReactionEmoji(emoticon=reaction_emoji)]
                            ))
                            print(f"Reaction added to {current_msg.id}")
                        except Exception as e:
                            print(f"Reaction error: {e}")

                await asyncio.sleep(5)

            except Exception as e:
                print(f"Error: {e}")
                await asyncio.sleep(10)

    except Exception as e:
        print(f"Critical error: {e}")
    finally:
        await client.disconnect()

asyncio.run(main())
