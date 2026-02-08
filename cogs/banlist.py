import discord
from discord import app_commands
from discord.ext import commands
import config
from utils.logger import log

class Banlist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        audit_log = None
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            audit_log = entry
            break
        
        if audit_log is None:
            return
        
        banlist_channel = self.bot.get_channel(config.BAN_LOG_CHANNEL_ID)
        embed = discord.Embed(
            title="User Banned",
            description=f"{audit_log.target.mention} has been banned from the server.\nReason: {audit_log.reason}\nBanned by: {audit_log.user.mention}",
            color=discord.Color.red()
        )
        await banlist_channel.send(embed=embed)
        await log(self.bot, f'LOG: User {audit_log.target.mention} has been banned from the server')
        
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        audit_log = None
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.unban):
            audit_log = entry
            break
        
        if audit_log is None:
            return
        
        banlist_channel = self.bot.get_channel(config.BAN_LOG_CHANNEL_ID)
        embed = discord.Embed(
            title="User Unbanned",
            description=f"{audit_log.target.mention} has been unbanned from the server.\nUnbanned by: {audit_log.user.mention}",
            color=discord.Color.green()
        )
        await banlist_channel.send(embed=embed)
        await log(self.bot, f'LOG: User {audit_log.target.mention} has been unbanned from the server')
            
    @app_commands.command(name='minecraft_ban', description='Report a banned user from the Minecraft server!')
    async def minecraft_ban(self, interaction: discord.Interaction, username: str, reason: str = "No reason provided"):
        if config.ADMIN_ROLE_ID not in [role.id for role in interaction.user.roles] and config.MOD_ROLE_ID not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            await log(self.bot, f'ERROR: User {interaction.user.mention} attempted to use `minecraft_ban` without permission')
            return
        
        # Minecraft server ban 
        
        await interaction.response.send_message(f'User {username} has been banned from the Minecraft server for: {reason}', ephemeral=True)
        await log(self.bot, f'LOG: Minecraft user {username} has been banned by {interaction.user.mention} for: {reason}')
        banlist_channel = self.bot.get_channel(config.BAN_LOG_CHANNEL_ID)
        embed = discord.Embed(
            title="Minecraft User Banned",
            description=f"User {username} has been banned from the Minecraft server.\nReason: {reason}\nBanned by: {interaction.user.mention}",
            color=discord.Color.red()
        )
        await banlist_channel.send(embed=embed)
        
    @app_commands.command(name='minecraft_unban', description='Report an unbanned user from the Minecraft server!')
    async def minecraft_unban(self, interaction: discord.Interaction, username: str):
        if config.ADMIN_ROLE_ID not in [role.id for role in interaction.user.roles] and config.MOD_ROLE_ID not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            await log(self.bot, f'ERROR: User {interaction.user.mention} attempted to use `minecraft_unban` without permission')
            return

        # Minecraft server unban

        await interaction.response.send_message(f'User {username} has been unbanned from the Minecraft server.', ephemeral=True)
        await log(self.bot, f'LOG: Minecraft user {username} has been unbanned by {interaction.user.mention}')
        banlist_channel = self.bot.get_channel(config.BAN_LOG_CHANNEL_ID)
        embed = discord.Embed(
            title="Minecraft User Unbanned",
            description=f"User {username} has been unbanned from the Minecraft server.\nUnbanned by: {interaction.user.mention}",
            color=discord.Color.green()
        )
        await banlist_channel.send(embed=embed)
async def setup(bot):
    await bot.add_cog(Banlist(bot))