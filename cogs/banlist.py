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
            description=f"{audit_log.target.mention} - {audit_log.target.display_name} has been banned from the server.\nReason: {audit_log.reason}\nBanned by: {audit_log.user.mention}",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=audit_log.target.display_avatar.url)
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
            description=f"{audit_log.target.mention} - {audit_log.target.display_name} has been unbanned from the server.\nUnbanned by: {audit_log.user.mention}",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=audit_log.target.display_avatar.url)
        await banlist_channel.send(embed=embed)
        await log(self.bot, f'LOG: User {audit_log.target.mention} has been unbanned from the server')
            
async def setup(bot):
    await bot.add_cog(Banlist(bot))