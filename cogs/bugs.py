import discord
from discord import app_commands
from discord.ext import commands
import time
import config
from utils.logger import log

bug_report_cooldowns = {}

class BugDropdown(discord.ui.Select):
    def __init__(self, placeholder, options, custom_id):
        super().__init__(
            placeholder=placeholder,
            min_values=1,
            max_values=1,
            options=[discord.SelectOption(label=opt) for opt in options],
            custom_id=custom_id
        )

    async def callback(self, interaction: discord.Interaction):
        self.view.selected_options[self.custom_id] = self.values[0]
        await interaction.response.defer()

class BugConfirmButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Confirm", style=discord.ButtonStyle.green)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(BugModal(self.view.selected_options))
        message = await interaction.original_response()
        await message.edit(view=None)

class BugReportView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.selected_options = {}
        
        self.add_item(BugDropdown("Priority", ["Low", "Medium", "High"], "priority"))
        self.add_item(BugDropdown("Release Type", ["Public", "Patreon", "Other"], "release_type"))
        self.add_item(BugConfirmButton())

class BugModal(discord.ui.Modal):
    def __init__(self, selected_options):
        super().__init__(title="Report a bug!")
        self.selected_options = selected_options
        
        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.short,
            label="Title",
            required=True,
            placeholder="What is the title of your bug report?"
        ))
        
        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.long,
            label="Description",
            required=True,
            placeholder="Describe the bug you encountered."
        ))
        
        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.long,
            label="Steps to Reproduce",
            required=True,
            placeholder="Describe the steps to reproduce the bug."
        ))
        
        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.long,
            label="Expected Behavior vs Actual Behavior",
            required=True,
            placeholder="Explain what you expected to happen compared to what actually happened."
        ))
        
        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.long,
            label="Additional Notes",
            required=False,
            placeholder="List any extra details and/or add links to any media you would like to share."
        ))

    async def on_submit(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        current_time = time.time()
        
        await interaction.response.defer(ephemeral=True)
        
        # Use interaction.client instead of global client
        channel = await interaction.client.fetch_channel(config.PUBLIC_BUG_CHANNEL_ID)

        priority_tags = {
            "Low": config.PUBLIC_BUG_LOW_PRIO,
            "Medium": config.PUBLIC_BUG_MEDIUM_PRIO,
            "High": config.PUBLIC_BUG_HIGH_PRIO
        }

        release_tags = {
            "Public": config.PUBLIC_BUG_PUBLIC_REL,
            "Patreon": config.PUBLIC_BUG_PATREON_REL,
            "Other": config.PUBLIC_BUG_OTHER_REL
        }

        applied_tags = [
            discord.Object(id=tag) for tag in [
                priority_tags.get(self.selected_options.get("priority")),
                release_tags.get(self.selected_options.get("release_type"))
            ] if tag is not None
        ]

        if isinstance(channel, discord.ForumChannel):
            await channel.create_thread(
                name=self.children[0].value,
                content=f'# Bug report from {interaction.user.mention}\n\n'
                        f'**Description:**\n {self.children[1].value}\n\n'
                        f'**Steps to Reproduce:**\n{self.children[2].value}\n\n'
                        f'**Expected Behavior vs Actual Behavior:**\n{self.children[3].value}\n\n'
                        f'**Additional Notes:**\n{self.children[4].value}',
                applied_tags=applied_tags
            )
            
            bug_report_cooldowns[user_id] = current_time
            
            await interaction.followup.send("Bug report submitted successfully!", ephemeral=True)
            
        else:
            await log(interaction.client, f'ERROR: User <@{interaction.user.id}> encountered an issue when reporting a bug: Channel {channel} is not a forum channel!')

    async def on_error(self, interaction: discord.Interaction, error):
        await log(interaction.client, f'ERROR: User <@{interaction.user.id}> encountered an issue when reporting a bug: {error}')


class Bug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bug", description="Report a bug!")
    async def bug(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        current_time = time.time()
        
        # Check if user is on cooldown
        if user_id in bug_report_cooldowns:
            last_used = bug_report_cooldowns[user_id]
            cooldown_time = 180  # 3 minutes
            time_left = cooldown_time - (current_time - last_used)

            if time_left > 0:
                await interaction.response.send_message(
                    f"Please wait {int(time_left)} seconds before submitting another bug report.", ephemeral=True
                )
                return

        await log(self.bot, f'LOG: User <@{interaction.user.id}> ran command `bug` in channel <#{interaction.channel.id}>')
        await interaction.response.send_message(
            "Before reporting your bug, please answer the following questions:", ephemeral=True, view=BugReportView()
        )

async def setup(bot):
    await bot.add_cog(Bug(bot))
