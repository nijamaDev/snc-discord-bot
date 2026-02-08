import discord
from discord import app_commands
from discord.ext import commands
from utils.logger import log

class PatchNotesView(discord.ui.View):
    def __init__(self, patch_notes, index):
        super().__init__(timeout=None)
        self.patch_notes = patch_notes
        self.index = index
    
    @discord.ui.button(label='⮜⮜', style=discord.ButtonStyle.success)
    async def first_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index = 0
        displayedNotes = list(self.patch_notes.keys())[self.index]
        await interaction.response.edit_message(content=f'**{displayedNotes} Patch Notes**\n{self.patch_notes[displayedNotes]}', view=self)
    
    @discord.ui.button(label='⮜', style=discord.ButtonStyle.success)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index = max(0, self.index - 1)
        displayedNotes = list(self.patch_notes.keys())[self.index]
        await interaction.response.edit_message(content=f'**{displayedNotes} Patch Notes**\n{self.patch_notes[displayedNotes]}', view=self)
    
    @discord.ui.button(label='⮞', style=discord.ButtonStyle.success)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index = min(len(self.patch_notes) - 1, self.index + 1)
        displayedNotes = list(self.patch_notes.keys())[self.index]
        await interaction.response.edit_message(content=f'**{displayedNotes} Patch Notes**\n{self.patch_notes[displayedNotes]}', view=self)

    @discord.ui.button(label='⮞⮞', style=discord.ButtonStyle.success)
    async def last_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index = len(self.patch_notes) - 1
        displayedNotes = list(self.patch_notes.keys())[self.index]
        await interaction.response.edit_message(content=f'**{displayedNotes} Patch Notes**\n{self.patch_notes[displayedNotes]}', view=self)

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    patch_notes = {
        '2026-02-07': '- Added the `/update` command to view the current and past patch notes for the bot.\n- Added the `/forward_bug` command to allow testers to automatically forward confirmed bugs to tester-only bug channel.\n- Added `Server Release` option under `Releases` category for bug reports\n- Added ban logs for moderators\n- Added the ability for thread owners to pin messages by reacting to any message in a thread with a pin emoji (📌 or📍)\n- Various bug fixes and improvements.',
        '2026-01-12': '- Added the `/command` command to get a list of commands and their descriptions.\n- Standardized logs to always mention relevant users and channels.\n- Major code refactor; split code into seperate cogs for better organization and readability.\n- Various bug fixes and improvements.',
        '2025-11-02': '- Changed `Discord Server` field to `Extra Links` in `/server_listing` command.',
        '2025-10-30': '- Fixed `/bug` showing server listing modal',
        '2025-10-26': '- Added server listings system\n- Added `/elysium_archive` command',
        '2025-06-02': '- Updated `/server` command with new IP and version info\n- Response message for `/mark_for_review` command made ephemeral',
        '2025-05-18': '- Added `/support` command with info on how to support SNC\n- Updated various log messages',
        '2025-05-07': '- Added attachement support for modmail',
        '2025-03-01': '- Updated `/server` command with new IP\n - Added a response message to `/mark_for_review` command',
        '2025-02-23': '- Added `/server` command to get the IP of the Minecraft server\n- `/mark_for_review` command for staff to manually mark a suggestion for review\n- Logs improvments',
        '2025-02-20': '- Bot released publicly!'
    }

    @app_commands.command(name='update',description='View current and past patch notes for the bot!')
    async def update(self, interaction:discord.Interaction):
        index = 0
        displayedNotes = list(self.patch_notes.keys())[index]
        await interaction.response.send_message(f'**{displayedNotes} Patch Notes**\n{self.patch_notes[displayedNotes]}', view=PatchNotesView(self.patch_notes, index))

    @app_commands.command(name='commands',description='Get a list of commands and their descriptions!')
    async def commands(self, interaction:discord.Interaction):
        await interaction.response.send_message('Here is a list of commands you can use:\n\n`/commands` - Get a list of commands and their descriptions!\n`/update` - View current and past patch notes for the bot!\n`/wiki` - Get the link to the wiki!\n`/villager_guide` - Get the link Fanfo\'s video guide about villagers and reproduction!\n`/spawn_blocks` - Check what blocks titans can spawn on!\n`/sleep` - A friendly reminder that sleep is important!\n`/shifter` - Get the command to give yourself a shifter!\n`/snc2` - Get the link to Shingeki no Craft 2!\n`/snc1` - Get the link to Shingeki no Craft 1!\n`/patreon` - Get help with linking your discord and patreon accounts!\n`/modpack` - Get the link to Fanfo\'s video about the modpack!\n`/map` - Get the link the Shinganshina map used in Fanfo\'s videos!\n`/install` - A guide on how to install the pack!\n`/coral` - Get a link to Fanfo\'s adventure map, Coral!\n`/snc_config` - Get the command to access the config!\n`/chainsaw` - Get a link to Fanfo\'s adventure map, Chainsaw Craft!\n`/server` - Get the IP of the server!\n`/support` - See how you can support SNC!\n`/elysium_archive` - Get links to the world download of previous seasons of Elysium\n`/bug` - Report a bug!\n`/server_listing` - Post a server listing!')
        await log(self.bot, f'LOG: User {interaction.user.mention} ran command `commands` in channel {interaction.channel.mention}')

    @app_commands.command(name='wiki',description='Get the link to the wiki!')
    async def wiki(self, interaction:discord.Interaction):
        await interaction.response.send_message('https://sncraft.fanfus.com/wiki')
        await log(self.bot, f'LOG: User {interaction.user.mention} ran command `wiki` in channel {interaction.channel.mention}')
        
    @app_commands.command(name='villager_guide',description='Get the link Fanfo\'s video guide about villagers and reproduction!')
    async def villager_guide(self, interaction:discord.Interaction):
        await interaction.response.send_message('https://www.youtube.com/watch?v=srcHjwWjUJ0')
        await log(self.bot, f'LOG: User {interaction.user.mention} ran command `villager_guide` in channel {interaction.channel.mention}')

    @app_commands.command(name='spawn_blocks',description='Check what blocks titans can spawn on!')
    async def spawn_blocks(self, interaction:discord.Interaction):
        await interaction.response.send_message('https://cdn.discordapp.com/attachments/953767082703601757/1219415927397814312/image.png?ex=66147314&is=6601fe14&hm=32da2bc67612c32eab8ac253427dc8e6081d5ba64f402b7c0c15f753436b08ce&')
        await log(self.bot, f'LOG: User {interaction.user.mention} ran command `spawn_blocks` in channel {interaction.channel.mention}')

    @app_commands.command(name='sleep',description='A friendly reminder that sleep is important!')
    async def sleep(self, interaction:discord.Interaction):
        await interaction.response.send_message('https://cdn.discordapp.com/attachments/953767082703601757/1057940256529338418/2022-12-29_00-32-51_Trim.mp4?ex=6617a124&is=66052c24&hm=fdcf67c315dce3e89b6b015219cdc339e29dce9ed5d4eb654ed602035545ae04&')
        await log(self.bot, f'LOG: User {interaction.user.mention} ran command `sleep` in channel {interaction.channel.mention}')

    @app_commands.command(name='shifter',description='Get the command to give yourself a shifter!')
    async def shifter(self, interaction:discord.Interaction):
        await interaction.response.send_message('You can use `/function snc:api/get/shifter/[shifter]` to get a shifter, and just replace `[shifter]` with what you want')
        await log(self.bot, f'LOG: User {interaction.user.mention} ran command `shifter` in channel {interaction.channel.mention}')

    @app_commands.command(name='snc2',description='Get the link Shingeki no Craft 2!')
    async def snc2(self, interaction:discord.Interaction):
        await interaction.response.send_message('https://www.planetminecraft.com/data-pack/shingeki-no-craft-2/')
        await log(self.bot, f'LOG: User {interaction.user.mention} ran command `snc2` in channel {interaction.channel.mention}')

    @app_commands.command(name='snc1',description='Get the link to Shingeki no Craft 1!')
    async def snc1(self, interaction:discord.Interaction):
        await interaction.response.send_message('https://www.planetminecraft.com/data-pack/attack-on-titan-datapack-1-16-download/')
        await log(self.bot, f'LOG: User {interaction.user.mention} ran command `snc1` in channel {interaction.channel.mention}')

    @app_commands.command(name='patreon',description='Get help with linking your discord and patreon accounts!')
    async def patreon(self, interaction:discord.Interaction):
        await interaction.response.send_message('If you are missing the Patreon status/roles try the following steps:\n\nGo to https://www.patreon.com/settings/apps/discord and ensure your Discord ID is correct.\nGo to https://www.patreon.com/settings/basics and change your display name, change it to anything and then change it back. This is your patreon display name, not discord.\nAlso make sure you appear as online when making these changes. sometimes appearing offline can stop the linking process.')
        await log(self.bot, f'LOG: User {interaction.user.mention} ran command `patreon` in channel {interaction.channel.mention}')

    @app_commands.command(name='modpack',description='Get the link to Fanfo\'s video about the modpack!')
    async def modpack(self, interaction:discord.Interaction):
        await interaction.response.send_message('https://www.youtube.com/watch?v=bGrnwFEQxZ4')
        await log(self.bot, f'LOG: User {interaction.user.mention} ran command `modpack` in channel {interaction.channel.mention}')

    @app_commands.command(name='map',description='Get the link the Shinganshina map used in Fanfo\'s videos!')
    async def map(self, interaction:discord.Interaction):
        await interaction.response.send_message('https://cdn.discordapp.com/attachments/953780982077616288/1153022566596870274/MapPreston.zip?ex=6612da72&is=66006572&hm=a440c24c26568f4f69d5ec7c98eb0c0583e9620025a1601a9de79445c146de8a&')
        await log(self.bot, f'LOG: User {interaction.user.mention} ran command `map` in channel {interaction.channel.mention}')

    @app_commands.command(name='install',description='A guide on how to install the pack!')
    async def install(self, interaction:discord.Interaction):
        await interaction.response.send_message('If you are using the mod version, it is installed like a normal mod in fabric or forge. If you are using the datapack version, you can follow these guides:\nhttps://www.planetminecraft.com/blog/how-to-download-and-install-minecraft-data-packs/\nhttps://www.planetminecraft.com/blog/how-to-install-minecraft-texture-packs-4615399/')
        await log(self.bot, f'LOG: User {interaction.user.mention} ran command `install` in channel {interaction.channel.mention}')

    @app_commands.command(name='coral',description='Get a link to Fanfo\'s adventure map, Coral!')
    async def coral(self, interaction:discord.Interaction):
        await interaction.response.send_message('https://www.planetminecraft.com/project/coral-5944252/')
        await log(self.bot, f'LOG: User {interaction.user.mention} ran command `coral` in channel {interaction.channel.mention}')

    @app_commands.command(name='snc_config',description='Get the command to access the config!')
    async def snc_config(self, interaction:discord.Interaction):
        await interaction.response.send_message('`/function snc:api/config`')
        await log(self.bot, f'LOG: User {interaction.user.mention} ran command `snc_config` in channel {interaction.channel.mention}')

    @app_commands.command(name='chainsaw',description='Get a link to Fanfo\'s adventure map, Chainsaw Craft!')
    async def chainsaw(self, interaction:discord.Interaction):
        await interaction.response.send_message('https://www.planetminecraft.com/project/chainsaw-craft-chainsaw-man-in-minecraft-vanilla/')
        await log(self.bot, f'LOG: User {interaction.user.mention} ran command `chainsaw` in channel {interaction.channel.mention}')
        
    @app_commands.command(name='server',description='Get the IP of the server!')
    async def server(self, interaction:discord.Interaction):
        await interaction.response.send_message('IP: `snc.sparked.network`\nVersion: `1.21.8`')
        await log(self.bot, f'LOG: User {interaction.user.mention} ran command `server` in channel {interaction.channel.mention}')

    @app_commands.command(name='support',description='See how you can support SNC!')
    async def support(self, interaction:discord.Interaction):
        await interaction.response.send_message('You can support SNC through several different ways, including [Patreon](https://www.patreon.com/join/8356530), [Ko-Fi](https://ko-fi.com/fanfo/tiers), boosting the server, which has the same rewards as buying Maria on Patreon or Ko-Fi, or just simply being here in the community. Never feel pressured to buy something you cannot afford.')
        await log(self.bot, f'LOG: User {interaction.user.mention} ran command `support` in channel {interaction.channel.mention}')
        
    @app_commands.command(name='elysium_archive',description='Get links to the world download of previous seasons of Elysium')
    async def elysium_archive(self, interaction:discord.Interaction):
        await interaction.response.send_message('**Elysium S1 World Download:** <https://mega.nz/file/IdsiwawI#-ftkFRWad8lRG3_hxgnhxZk7yduVEcztZ2NzLiZfgBE>\n**Elysium S2 World Download:** <https://mega.nz/file/xYVnnKiQ#jBNhuyjWoPAeoydYIsa3G6IlerkO49h6ouP34oeu2ag>')
        await log(self.bot, f'LOG: User {interaction.user.mention} ran command `elysium_archive` in channel {interaction.channel.mention}')

class ThreadMessagePinning(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.emoji.name == '📌' or payload.emoji.name == '📍':
            channel = self.bot.get_channel(payload.channel_id)
            if isinstance(channel, discord.Thread):
                # Determine the effective owner
                owner_id = channel.owner_id
                if owner_id == self.bot.user.id:
                    # Thread created by bot, find the first mentioned user in bot's message
                    async for m in channel.history(limit=100, oldest_first=True):
                        if m.author == self.bot.user and m.mentions:
                            owner_id = m.mentions[0].id
                            break
                
                if payload.user_id == owner_id:
                    try:
                        message = await channel.fetch_message(payload.message_id)
                        await message.pin()
                        async for m in channel.history(limit=10):
                            if m.type == discord.MessageType.pins_add:
                                await m.delete()
                                break
                    except Exception:
                        pass
                
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.emoji.name == '📌' or payload.emoji.name == '📍':
            channel = self.bot.get_channel(payload.channel_id)
            if isinstance(channel, discord.Thread):
                # Determine the effective owner
                owner_id = channel.owner_id
                if owner_id == self.bot.user.id:
                    # Thread created by bot, find the first mentioned user in bot's message
                    async for m in channel.history(limit=100, oldest_first=True):
                        if m.author == self.bot.user and m.mentions:
                            owner_id = m.mentions[0].id
                            break
                
                if payload.user_id == owner_id:
                    try:
                        message = await channel.fetch_message(payload.message_id)
                        await message.unpin()
                    except Exception:
                        pass

async def setup(bot):
    await bot.add_cog(Commands(bot))
    await bot.add_cog(ThreadMessagePinning(bot))
