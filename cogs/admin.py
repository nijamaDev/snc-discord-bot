import discord
from discord import app_commands
from discord.ext import commands
import config
from utils.logger import log

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='on_ready', description='Run the on_ready function of the bot!')
    async def on_ready_command(self, interaction: discord.Interaction):
        if interaction.user.id not in config.BOT_ADMIN:
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            await log(self.bot, f'ERROR: User {interaction.user.mention} attempted to use `on_ready` without permission')
            return
        
        await interaction.response.send_message('Reloading!', ephemeral=True)
        await log(self.bot, f'LOG: User {interaction.user.mention} reloaded the bot')
        await self.bot.run_on_ready_logic()

    @app_commands.command(name='set_config', description='Configure the bot!')
    async def set_config(self, interaction: discord.Interaction, config_key: str, value: str):
        if interaction.user.id not in config.BOT_ADMIN:
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            await log(self.bot, f'ERROR: User {interaction.user.mention} attempted to use `set_config` without permission')
            return
        
        configs = [
            'SUGGESTIONS_CHANNEL_ID',
            'REVIEW_CHANNEL_ID',
            'REQUIRED_REACTIONS',
            'LOG_CHANNEL_ID',
            'PUBLIC_BUG_CHANNEL_ID',
            'PRIVATE_BUG_CHANNEL_ID',
            'MODMAIL_CHANNEL_ID',
            'SERVER_LISTINGS_CHANNEL_ID'
        ]
        
        config_key = config_key.upper().replace(' ', '_')
        if config_key in configs:
            await config.update_env_var(config_key, value)
            # Re-run logic associated with config changes
            await self.bot.run_on_ready_logic(key=config_key)
            
            await interaction.response.send_message(f'Config `{config_key}` has been updated to `{value}`.', ephemeral=True)
            await log(self.bot, f'LOG: Config `{config_key}` updated to `{value}` by user {interaction.user.mention}')
        else:
            await interaction.response.send_message(f'Invalid config key: `{config_key}`. Valid config keys: `{configs}`', ephemeral=True)
            await log(self.bot, f'ERROR: Invalid config key `{config_key}` provided by user {interaction.user.mention}')

    @app_commands.command(name='get_config', description='View the current configuration of the bot!')
    async def get_config(self, interaction: discord.Interaction):
        if interaction.user.id not in config.BOT_ADMIN:
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            await log(self.bot, f'ERROR: User {interaction.user.mention} attempted to use `get_config` without permission')
            return

        configs = {
            'SUGGESTIONS_CHANNEL_ID': config.SUGGESTIONS_CHANNEL_ID,
            'REVIEW_CHANNEL_ID': config.REVIEW_CHANNEL_ID,
            'REQUIRED_REACTIONS': config.REQUIRED_REACTIONS,
            'LOG_CHANNEL_ID': config.LOG_CHANNEL_ID,
            'PUBLIC_BUG_CHANNEL_ID': config.PUBLIC_BUG_CHANNEL_ID,
            'PRIVATE_BUG_CHANNEL_ID': config.PRIVATE_BUG_CHANNEL_ID,
            'MODMAIL_CHANNEL_ID': config.MODMAIL_CHANNEL_ID,
            'SERVER_LISTINGS_CHANNEL_ID': config.SERVER_LISTINGS_CHANNEL_ID
        }
        
        config_message = "\n".join([f"{key}: {value}" for key, value in configs.items()])
        await interaction.response.send_message(f"**Current Configurations:**\n```\n{config_message}\n```", ephemeral=True)
        await log(self.bot, f'LOG: User <@{interaction.user.id}> viewed the config')

async def setup(bot):
    await bot.add_cog(Admin(bot))
