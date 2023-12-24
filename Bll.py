import asyncio
import re

profanity_words = set()

def load_profanity_words():
    with open("profanity_words.txt", "r") as file:
        for word in file:
            profanity_words.add(word.strip().lower())

async def msg_delete(message):
    await message.delete()

async def profanity_warn(message, content, detected_words):
    if detected_words:
        try:
            channel = message.channel
            warning_msg = await channel.send(
                f"Please refrain from using vulgar words!🙏 {message.author.mention}\nProfanity detected ⚠️= {detected_words}"
            )
            await asyncio.sleep(2)
            for i in range(5, 0, -1):
                await asyncio.sleep(0.5)
                await warning_msg.edit(content=f"{message.author.mention}, your message will be deleted in {i} seconds")

            await warning_msg.delete()
            asyncio.create_task(msg_delete(message))

            server_name = f"[{message.guild.name}]"
            for word in detected_words:
                print("\nCode 1= Success!")
                print(f"Profanity word detected ⚠️: {word}\nServer: {server_name} User: {message.author}")
        except Exception as e:
            error_msg = "Unable to delete messages. \nError: {}".format(str(e))
            channel = message.channel
            await channel.send(error_msg)

    else:
        try:
            # Replace repeated characters with a single character
            content = re.sub(r"(.)\1{1,}", r"\1", content)

            # Check if the modified message contains any profanity words
            detected_words = [word for word in profanity_words if word in content]
            if detected_words:
                channel = message.channel
                warning_msg = await channel.send(
                    f"Please refrain from using vulgar words!🙏 {message.author.mention}\nProfanity detected ⚠️= {detected_words}"
                )
                await asyncio.sleep(2)
                for i in range(5, 0, -1):
                    await asyncio.sleep(0.5)
                    await warning_msg.edit(content=f"{message.author.mention}, your message will be deleted in {i} seconds")

                await warning_msg.delete()
                await message.delete()

                server_name = f"[{message.guild.name}]"
                for word in detected_words:
                    print("\nCode Success!")
                    print(f"Profanity word detected ⚠️: {word}\nServer: {server_name} User: {message.author}")
        except Exception as e:
            error_msg = "Unable to delete messages. \nError: {}".format(str(e)) 
            channel = message.channel
            await channel.send(error_msg)