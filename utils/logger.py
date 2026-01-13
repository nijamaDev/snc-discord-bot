import discord
import config

async def log(bot, message):
    print(message)
    try:
        log_channel = bot.get_channel(config.LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(message.replace("LOG:","**LOG:**").replace("WARN:","**WARN:**").replace("ERROR:","**ERROR:**"))
        else:
            print(f"Could not find log channel with ID {config.LOG_CHANNEL_ID}")
    except Exception as e:
        print(f"Failed to log to channel: {e}")
