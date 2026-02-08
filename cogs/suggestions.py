import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View
import config
from utils.logger import log

class SuggestionReviewView(View):
    def __init__(self, bot, original_thread, review_embed, review_tag, accepted_tag, rejected_tag):
        super().__init__(timeout=None)
        self.bot = bot
        self.original_thread = original_thread
        self.review_embed = review_embed
        self.review_tag = review_tag
        self.accepted_tag = accepted_tag
        self.rejected_tag = rejected_tag

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success)
    async def accept_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await self.original_thread.add_tags(self.accepted_tag)
            await self.original_thread.remove_tags(self.review_tag)
            self.review_embed.color = discord.Color.green()
            self.review_embed.title = f"Accepted: {self.original_thread.name}" 
            
            await interaction.message.edit(embed=self.review_embed, view=None)
            await interaction.response.send_message("Suggestion accepted!", ephemeral=True)
            await self.original_thread.send("This suggestion has been accepted!")
            await log(self.bot, f'LOG: Suggestion {self.original_thread.mention} has been accepted')
            
        except Exception as e:
            await interaction.response.send_message("An error occurred. Please check logs for more details.", ephemeral=True)
            await log(self.bot, f'ERROR: Encountered error when accepting a suggestion: {e}')

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.danger)
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await self.original_thread.add_tags(self.rejected_tag)
            await self.original_thread.remove_tags(self.review_tag)
            self.review_embed.color = discord.Color.red()
            self.review_embed.title = f"Rejected: {self.original_thread.name}" 

            await interaction.message.edit(embed=self.review_embed, view=None)
            await interaction.response.send_message("Suggestion rejected!", ephemeral=True)
            await self.original_thread.send("This suggestion has been rejected!")
            await log(self.bot, f'LOG: Suggestion {self.original_thread.mention} has been rejected')
            
        except Exception as e:
            await interaction.response.send_message("An error occurred. Please check logs for more details.", ephemeral=True)
            await log(self.bot, f'ERROR: Encountered error when denying a suggestion: {e}')


class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        try:
            channel = self.bot.get_channel(payload.channel_id)
            
            if isinstance(channel, discord.Thread):
                parent_channel = channel.parent
                if parent_channel.id == config.SUGGESTIONS_CHANNEL_ID:
                    message = await channel.fetch_message(payload.message_id)
                    for reaction in message.reactions: ###
                        if reaction.count >= config.REQUIRED_REACTIONS and reaction.emoji == config.VOTE_REACTION:
                            if not any(tag.id == config.REVIEW_TAG_ID or tag.id == config.ACCEPTED_TAG_ID or tag.id == config.REJECTED_TAG_ID or tag.id == config.DISCUSSION_TAG_ID for tag in channel.applied_tags):
                                review_tag = discord.utils.get(parent_channel.available_tags, id=config.REVIEW_TAG_ID)
                                accepted_tag = discord.utils.get(parent_channel.available_tags, id=config.ACCEPTED_TAG_ID)
                                rejected_tag = discord.utils.get(parent_channel.available_tags, id=config.REJECTED_TAG_ID)
                                if review_tag:
                                    await log(self.bot, f'LOG: Suggestion {channel.mention} marked for review')
                                    await channel.add_tags(review_tag)
                                    await channel.send('This suggestion has been marked for review!')
                                    review_channel = self.bot.get_channel(config.REVIEW_CHANNEL_ID)
                                    embed = discord.Embed(
                                            color = discord.Color.yellow(),
                                            title = channel.name,
                                            description = message.content
                                        )
                                    embed.add_field(
                                        name="Thread Link", 
                                        value=f"[Click here to view the thread]({channel.jump_url})", 
                                        inline=False
                                    )
                                    embed.add_field(name="Suggested By", value=message.author.mention, inline=False)
                                    view = SuggestionReviewView(bot=self.bot, original_thread=channel, review_embed=embed, review_tag=review_tag, accepted_tag=accepted_tag, rejected_tag=rejected_tag)
                                    await review_channel.send(embed=embed, view=view)
                                    
        except Exception as e:
            await log(self.bot, f'ERROR: Encountered error when marking a suggestion for review: {e}')

    @app_commands.command(name='mark_for_review',description='Mark a suggestion for review')
    async def mark_for_review(self, interaction:discord.Interaction):
        if config.ADMIN_ROLE_ID not in [role.id for role in interaction.user.roles] and config.MOD_ROLE_ID not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            await log(self.bot, f'ERROR: User {interaction.user.mention} attempted to use `mark_for_review` without permission')
            return
        try:
            channel = self.bot.get_channel(interaction.channel_id)
            
            if isinstance(channel, discord.Thread):
                parent_channel = channel.parent
                if parent_channel.id == config.SUGGESTIONS_CHANNEL_ID:
                    message = await channel.fetch_message(interaction.channel.id)
                    review_tag = discord.utils.get(parent_channel.available_tags, id=config.REVIEW_TAG_ID)
                    accepted_tag = discord.utils.get(parent_channel.available_tags, id=config.ACCEPTED_TAG_ID)
                    rejected_tag = discord.utils.get(parent_channel.available_tags, id=config.REJECTED_TAG_ID)
                    if review_tag:
                        await log(self.bot, f'LOG: Suggestion {channel.mention} manually marked for review by {interaction.user.mention}')
                        await channel.add_tags(review_tag)
                        await channel.send('This suggestion has been marked for review!')
                        review_channel = self.bot.get_channel(config.REVIEW_CHANNEL_ID)
                        embed = discord.Embed(
                                color = discord.Color.yellow(),
                                title = channel.name,
                                description = message.content
                            )
                        embed.add_field(
                            name="Thread Link", 
                            value=f"[Click here to view the thread]({channel.jump_url})", 
                            inline=False
                        )
                        embed.add_field(name="Suggested By", value=message.author.mention, inline=False)
                        view = SuggestionReviewView(bot=self.bot, original_thread=channel, review_embed=embed, review_tag=review_tag, accepted_tag=accepted_tag, rejected_tag=rejected_tag)
                        await review_channel.send(embed=embed, view=view)
            await interaction.response.send_message("Succesfully marked suggestion for review!",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message("An error occured. Check logs for more details.")
            await log(self.bot, f'ERROR: Encountered error when manually marking a suggestion for review: {e}')

async def setup(bot):
    await bot.add_cog(Suggestions(bot))

