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
        self.add_item(BugDropdown("Release Type", ["Public", "Patreon", "Server", "Other"], "release_type"))
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
            "Server": config.PUBLIC_BUG_SERVER_REL,
            "Other": config.PUBLIC_BUG_OTHER_REL
        }

        applied_tags = [
            discord.Object(id=tag) for tag in [
                priority_tags.get(self.selected_options.get("priority")),
                release_tags.get(self.selected_options.get("release_type")),
                config.PUBLIC_BUG_UNCONFIRMED
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

        await log(self.bot, f'LOG: User <@{interaction.user.id}> ran command `bug` in channel {interaction.channel.mention}')
        await interaction.response.send_message(
            "Before reporting your bug, please answer the following questions:", ephemeral=True, view=BugReportView()
        )
    
    @app_commands.command(name="forward_bug", description="Forward a bug report to the private bug channel!")
    async def forward_bug(self, interaction: discord.Interaction):
        if config.TESTER_ROLE_ID not in [role.id for role in interaction.user.roles] and config.ADMIN_ROLE_ID not in [role.id for role in interaction.user.roles] and config.MOD_ROLE_ID not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            await log(self.bot, f'ERROR: User {interaction.user.mention} attempted to use `forward_bug` without permission')
            return
        channel = self.bot.get_channel(interaction.channel_id)
        if channel is None or not isinstance(channel, discord.Thread):
            await interaction.response.send_message("This command can only be used in a thread channel.", ephemeral=True)
            return
        parent_channel = channel.parent
        if parent_channel.id != config.PUBLIC_BUG_CHANNEL_ID:
            await interaction.response.send_message("This command can only be used in a public bug report thread.", ephemeral=True)
            return
        
        private_bug_channel = self.bot.get_channel(config.PRIVATE_BUG_CHANNEL_ID)
        if private_bug_channel is None or not isinstance(private_bug_channel, discord.ForumChannel):
            await interaction.response.send_message("Private bug channel is not properly configured.", ephemeral=True)
            await log(self.bot, f'ERROR: Private bug channel {config.PRIVATE_BUG_CHANNEL_ID} is not a forum channel')
            return
        
        channel_tags = [tag.id for tag in channel.applied_tags]
        if config.PUBLIC_BUG_CONFIRMED in channel_tags:
            await interaction.response.send_message("This bug report has already been forwarded.", ephemeral=True)
            return
        
        try:
            message = await channel.fetch_message(interaction.channel.id)
            public_tags = [tag for tag in channel.applied_tags if tag.id != config.PUBLIC_BUG_UNCONFIRMED]
            private_tag_map = {t.name: t.id for t in private_bug_channel.available_tags}
            private_applied_tag_ids = [private_tag_map[name] for name in (t.name for t in public_tags) if name in private_tag_map]

            new_thread = await private_bug_channel.create_thread(
                name=channel.name,
                content=message.content,
                applied_tags=[discord.Object(id=tag_id) for tag_id in private_applied_tag_ids]
            )

            public_applied_tag_ids = [tag.id for tag in public_tags] + [config.PUBLIC_BUG_CONFIRMED]
            await channel.edit(applied_tags=[discord.Object(id=tag_id) for tag_id in public_applied_tag_ids])
            await log(self.bot, f'LOG: Bug report {channel.mention} forwarded to private bug channel by {interaction.user.mention}')
            await interaction.response.send_message(f"Bug report has been forwarded to the private bug channel: {new_thread.thread.mention}", ephemeral=True)
            await new_thread.thread.send(f"{channel.mention} forwarded by {interaction.user.mention}")
            await channel.send(f"Your bug report has been reviewed and verified by {interaction.user.mention}.")
            
        except Exception as e:
            await interaction.response.send_message("An error occurred while forwarding the bug report. Please check logs for more details.", ephemeral=True)
            await log(self.bot, f'ERROR: Failed to forward bug report {channel.mention}: {e}')

async def setup(bot):
    await bot.add_cog(Bug(bot))
