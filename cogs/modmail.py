import discord
from discord.ext import commands
import config
from utils.logger import log

class Modmail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        modmail_channel = self.bot.get_channel(config.MODMAIL_CHANNEL_ID)
        if not modmail_channel:
            return 
        
        if isinstance(message.channel, discord.DMChannel):
            threads = list(modmail_channel.threads) + [thread async for thread in modmail_channel.archived_threads(limit=None)]
            open_threads = {thread.name: thread for thread in threads}
            user_thread_name = f"{message.author.id} - {message.author}"
            await log(self.bot, f'LOG: Modmail recieved from user <@{message.author.id}>')

            if user_thread_name in open_threads:
                modmail_thread = open_threads[user_thread_name]
            else:
                create_thread = await modmail_channel.create_thread(
                    name = user_thread_name,
                    content = f"Modmail from {message.author.mention}",
                    auto_archive_duration=10080 # 7 days
                )
                modmail_thread = create_thread.thread
                await log(self.bot, f'LOG: Creating modmail thread for user <@{message.author.id}>')
            
            content = f"**[MODMAIL] {message.author.mention}:** {message.content}"
            files = []
            if message.attachments:
                for attachment in message.attachments:
                    file = await attachment.to_file()
                    files.append(file)
            await modmail_thread.send(content=content, files=files)
            await message.add_reaction("📨")
            
        
        if isinstance(message.channel, discord.Thread) and message.channel.parent_id == modmail_channel.id:
            try:
                user = await self.bot.fetch_user(int(message.channel.name.split(" - ")[0]))
                content = f"**[MODMAIL] {message.author.mention}:** {message.content}"
                files = []
                if message.attachments:
                    for attachment in message.attachments:
                        file = await attachment.to_file()
                        files.append(file)
                await user.send(content=content, files=files)
                await message.add_reaction("📨")
            except Exception as e:
                 await log(self.bot, f'ERROR: Failed to send DM to user in modmail: {e}')
        

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author == self.bot.user:
            return
        
        if isinstance(before.channel, discord.DMChannel):
            modmail_channel = self.bot.get_channel(config.MODMAIL_CHANNEL_ID)
            if not modmail_channel:
                 return
            threads = list(modmail_channel.threads) + [thread async for thread in modmail_channel.archived_threads(limit=None)]
            open_threads = {thread.name: thread for thread in threads}
            user_thread_name = f"{before.author.id} - {before.author}"
            
            if user_thread_name in open_threads:
                modmail_thread = open_threads[user_thread_name]
                content = f"**[MODMAIL] {before.author.mention}:** *Edited Message*\n**Before:** {before.content}\n**After:** {after.content}"
                files = []
                if before.attachments:
                    for attachment in before.attachments:
                        file = await attachment.to_file()
                        files.append(file)
                await modmail_thread.send(content=content, files=files)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author == self.bot.user:
            return
        
        if isinstance(message.channel, discord.DMChannel):
            modmail_channel = self.bot.get_channel(config.MODMAIL_CHANNEL_ID)
            if not modmail_channel:
                 return
            threads = list(modmail_channel.threads) + [thread async for thread in modmail_channel.archived_threads(limit=None)]
            open_threads = {thread.name: thread for thread in threads}
            user_thread_name = f"{message.author.id} - {message.author}"
            
            if user_thread_name in open_threads:
                modmail_thread = open_threads[user_thread_name]
                content = f"**[MODMAIL] {message.author.mention}:** *Deleted Message:* {message.content}"
                files = []
                if message.attachments:
                    for attachment in message.attachments:
                        file = await attachment.to_file()
                        files.append(file)
                await modmail_thread.send(content=content, files=files)

async def setup(bot):
    await bot.add_cog(Modmail(bot))
