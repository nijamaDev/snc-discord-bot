# bot.py
import os
import sys
import time

import discord
from discord import ui, app_commands
from dotenv import load_dotenv
from discord.ext import commands
from discord.ui import View, Button

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
suggestions_channel_id = int(os.getenv('SUGGESTIONS_CHANNEL_ID'))
review_channel_id = int(os.getenv('REVIEW_CHANNEL_ID'))
required_reactions = int(os.getenv('REQUIRED_REACTIONS'))
log_channel_id = int(os.getenv('LOG_CHANNEL_ID'))
modmail_channel_id = int(os.getenv('MODMAIL_CHANNEL_ID'))
public_bug_channel_id = int(os.getenv('PUBLIC_BUG_CHANNEL_ID'))
private_bug_channel_id = int(os.getenv('PRIVATE_BUG_CHANNEL_ID'))
server_listings_channel_id = int(os.getenv('SERVER_LISTINGS_CHANNEL_ID'))

# Define intents
intents = discord.Intents.all()

# Initialize client with intents
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Runs on startup
@client.event
async def on_ready():
    try:
        await tree.sync()
        await log(f'LOG: {client.user} has connected to Discord!')
        await client.change_presence(activity=discord.CustomActivity(name="📨 DM for modmail!"))
        
        try:
            global vote_reaction
            suggestions_channel = await client.fetch_channel(suggestions_channel_id)
            if isinstance(suggestions_channel, discord.ForumChannel):
                if suggestions_channel.default_reaction_emoji:
                    vote_reaction = suggestions_channel.default_reaction_emoji
                    await log(f'LOG: Vote reaction found for channel {suggestions_channel_id}. Using {vote_reaction}')
                else:
                    await log('WARN: No vote reaction found, using default: 👍')
                    vote_reaction = "👍"
                global accepted_tag_id
                global rejected_tag_id
                global review_tag_id
                global discussion_tag_id
                accepted_tag_id = next((tag for tag in suggestions_channel.available_tags if 'accepted' in tag.name.lower())).id
                rejected_tag_id = next((tag for tag in suggestions_channel.available_tags if 'rejected' in tag.name.lower())).id
                review_tag_id = next((tag for tag in suggestions_channel.available_tags if 'review' in tag.name.lower())).id
                discussion_tag_id = next((tag for tag in suggestions_channel.available_tags if 'discussion' in tag.name.lower())).id
            else:
                await log(f'ERROR: Failed to get vote reaction: Channel {suggestions_channel_id} is not a forum channel')
                
        except Exception as e:
            await log(f'ERROR: Encountered an error when checking for suggestions vote reaction: {e}')
            
        try:
            global public_bug_low_prio
            global public_bug_medium_prio
            global public_bug_high_prio
            global public_bug_public_rel
            global public_bug_patreon_rel
            global public_bug_other_rel
            public_bug_channel = await client.fetch_channel(public_bug_channel_id)
            if isinstance(public_bug_channel, discord.ForumChannel):
                public_bug_low_prio = next((tag for tag in public_bug_channel.available_tags if 'low' in tag.name.lower())).id
                public_bug_medium_prio = next((tag for tag in public_bug_channel.available_tags if 'medium' in tag.name.lower())).id
                public_bug_high_prio = next((tag for tag in public_bug_channel.available_tags if 'high' in tag.name.lower())).id
                public_bug_public_rel = next((tag for tag in public_bug_channel.available_tags if 'public' in tag.name.lower())).id
                public_bug_patreon_rel = next((tag for tag in public_bug_channel.available_tags if 'patreon' in tag.name.lower())).id
                public_bug_other_rel = next((tag for tag in public_bug_channel.available_tags if 'other' in tag.name.lower())).id
            else:
                await log(f'ERROR: Failed to get public bug channel tags: Channel {public_bug_channel} is not a forum channel')
                
        except Exception as e:
            await log(f'ERROR: Encountered an error when checking for public bug channel tags: {e}')
            
        try:
            global private_bug_low_prio
            global private_bug_medium_prio
            global private_bug_high_prio
            global private_bug_public_rel
            global private_bug_patreon_rel
            global private_bug_other_rel
            private_bug_channel = await client.fetch_channel(public_bug_channel_id)
            if isinstance(private_bug_channel, discord.ForumChannel):
                private_bug_low_prio = next((tag for tag in private_bug_channel.available_tags if 'low' in tag.name.lower())).id
                private_bug_medium_prio = next((tag for tag in private_bug_channel.available_tags if 'medium' in tag.name.lower())).id
                private_bug_high_prio = next((tag for tag in private_bug_channel.available_tags if 'high' in tag.name.lower())).id
                private_bug_public_rel = next((tag for tag in private_bug_channel.available_tags if 'public' in tag.name.lower())).id
                private_bug_patreon_rel = next((tag for tag in private_bug_channel.available_tags if 'patreon' in tag.name.lower())).id
                private_bug_other_rel = next((tag for tag in private_bug_channel.available_tags if 'other' in tag.name.lower())).id
            else:
                await log(f'ERROR: Failed to get private bug channel tags: Channel {private_bug_channel} is not a forum channel')
                
        except Exception as e:
            await log(f'ERROR: Encountered an error when checking for private bug channel tags: {e}')
            
        try:
            global server_listings_tag_sur_adv
            global server_listings_tag_sur
            global server_listings_tag_adv
            global server_listings_tag_fabric
            global server_listings_tag_forge
            global server_listings_tag_essential
            global server_listings_tag_rp
            global server_listings_tag_casual
            global server_listings_tag_comp
            global server_listings_tag_custom_map
            global server_listings_tag_minigames
            global server_listings_tag_creative
            global server_listings_tag_premium
            global server_listings_tag_cracked
            server_listings_channel = await client.fetch_channel(server_listings_channel_id)
            if isinstance(server_listings_channel, discord.ForumChannel):
                server_listings_tag_sur_adv = next((tag for tag in server_listings_channel.available_tags if 'survival' in tag.name.lower() if 'adventure' in tag.name.lower())).id
                server_listings_tag_sur = next((tag for tag in server_listings_channel.available_tags if 'survival' in tag.name.lower() if 'adventure' not in tag.name.lower())).id
                server_listings_tag_adv = next((tag for tag in server_listings_channel.available_tags if 'adventure' in tag.name.lower() if 'survival' not in tag.name.lower())).id
                server_listings_tag_fabric = next((tag for tag in server_listings_channel.available_tags if 'fabric' in tag.name.lower())).id
                server_listings_tag_forge = next((tag for tag in server_listings_channel.available_tags if 'forge' in tag.name.lower())).id
                server_listings_tag_essential = next((tag for tag in server_listings_channel.available_tags if 'essential' in tag.name.lower())).id
                server_listings_tag_rp = next((tag for tag in server_listings_channel.available_tags if 'roleplay' in tag.name.lower())).id
                server_listings_tag_casual = next((tag for tag in server_listings_channel.available_tags if 'casual' in tag.name.lower())).id
                server_listings_tag_comp = next((tag for tag in server_listings_channel.available_tags if 'competitive' in tag.name.lower())).id
                server_listings_tag_custom_map = next((tag for tag in server_listings_channel.available_tags if 'custom map' in tag.name.lower())).id
                server_listings_tag_minigames = next((tag for tag in server_listings_channel.available_tags if 'minigames' in tag.name.lower())).id
                server_listings_tag_creative = next((tag for tag in server_listings_channel.available_tags if 'creative' in tag.name.lower())).id
                server_listings_tag_premium = next((tag for tag in server_listings_channel.available_tags if 'premium' in tag.name.lower())).id
                server_listings_tag_cracked = next((tag for tag in server_listings_channel.available_tags if 'cracked' in tag.name.lower())).id
                
            else:
                await log(f'ERROR: Failed to get server listings channel tags: Channel {server_listings_channel} is not a forum channel')
                
        except Exception as e:
            await log(f'ERROR: Encountered an error when checking for server listings channel tags: {e}')
            
    except Exception as e:
        await log(f'ERROR: Encountered an error when loading the bot: {e}')

## Config
bot_admin = [
    293738089787031552, # Fanfo
    279823686532333570, # Nijama
    690342949556584690, # Bomb
    760834405559304202 # Energy
    ]

@tree.command(name='on_ready',description='Run the on_ready function of the bot!')
async def on_ready_command(interaction:discord.Interaction):
    if interaction.user.id not in bot_admin:
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        await log(f'ERROR: User {interaction.user.mention} attempted to use `on_ready` without permission')
        return
    
    await interaction.response.send_message('Reloading!', ephemeral=True)
    await log(f'LOG: User {interaction.user.mention} reloaded the bot')
    await on_ready()

@tree.command(name='set_config',description='Configure the bot!')
async def set_config(interaction:discord.Interaction, config: str, value: str):
    if interaction.user.id not in bot_admin:
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        await log(f'ERROR: User {interaction.user.mention} attempted to use `set_config` without permission')
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
    
    if config.upper().replace(' ', '_') in configs:
        await update_env_var(config.upper().replace(' ', '_'), value)
        await interaction.response.send_message(f'Config `{config}` has been updated to `{value}`.', ephemeral=True)
        await log(f'LOG: Config `{config}` updated to `{value}` by user {interaction.user.mention}')
    else:
        await interaction.response.send_message(f'Invalid config key: `{config}`. Valid config keys: `{configs}`', ephemeral=True)
        await log(f'ERROR: Invalid config key `{config}` provided by user {interaction.user.mention}')

@tree.command(name='get_config',description='View the current configuration of the bot!')
async def get_config(interaction:discord.Interaction):
    if interaction.user.id not in bot_admin:
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        await log(f'ERROR: User {interaction.user.mention} attempted to use `get_config` without permission')
        return

    configs = {
        'SUGGESTIONS_CHANNEL_ID': os.getenv('SUGGESTIONS_CHANNEL_ID'),
        'REVIEW_CHANNEL_ID': os.getenv('REVIEW_CHANNEL_ID'),
        'REQUIRED_REACTIONS': os.getenv('REQUIRED_REACTIONS'),
        'LOG_CHANNEL_ID': os.getenv('LOG_CHANNEL_ID'),
        'PUBLIC_BUG_CHANNEL_ID': os.getenv('BUG_CHANNEL_ID'),
        'PRIVATE_BUG_CHANNEL_ID': os.getenv('BUG_CHANNEL_ID'),
        'MODMAIL_CHANNEL_ID': os.getenv('MODMAIL_CHANNEL_ID'),
        'SERVER_LISTINGS_CHANNEL_ID': os.getenv('SERVER_LISTINGS_CHANNEL_ID')
    }
    
    config_message = "\n".join([f"{key}: {value}" for key, value in configs.items()])
    await interaction.response.send_message(f"**Current Configurations:**\n```\n{config_message}\n```", ephemeral=True)
    await log(f'LOG: User <@{interaction.user.id}> viewed the config')

async def update_env_var(key, value):
    # Read current .env file content
    with open('.env', 'r') as file:
        lines = file.readlines()

    # Check if the key exists
    found = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            found = True
            break

    # If the key doesn't exist, add it
    if not found:
        lines.append(f"{key}={value}\n")

    # Write the updated content back to the .env file
    with open('.env', 'w') as file:
        file.writelines(lines)

    # Update the vars in the bot's memory
    globals()[key.lower()] = value
    
    if key == 'SUGGESTIONS_CHANNEL_ID':
        global vote_reaction
        suggestions_channel = await client.fetch_channel(suggestions_channel_id)
        if isinstance(suggestions_channel, discord.ForumChannel):
            if suggestions_channel.default_reaction_emoji:
                vote_reaction = suggestions_channel.default_reaction_emoji
                await log(f'LOG: Vote reaction found for channel {suggestions_channel_id}. Using {vote_reaction}')
            else:
                await log('WARN: No vote reaction found, using default: 👍')
                vote_reaction = "👍"
            global accepted_tag_id
            global rejected_tag_id
            global review_tag_id
            global discussion_tag_id
            accepted_tag_id = next((tag for tag in suggestions_channel.available_tags if 'accepted' in tag.name.lower())).id
            rejected_tag_id = next((tag for tag in suggestions_channel.available_tags if 'rejected' in tag.name.lower())).id
            review_tag_id = next((tag for tag in suggestions_channel.available_tags if 'review' in tag.name.lower())).id
            discussion_tag_id = next((tag for tag in suggestions_channel.available_tags if 'discussion' in tag.name.lower())).id
        else:
            await log(f'ERROR: Failed to get vote reaction: Channel {suggestions_channel} is not a forum channel')

    if key == 'PUBLIC_BUG_CHANNEL_ID':
        global public_bug_low_prio
        global public_bug_medium_prio
        global public_bug_high_prio
        global public_bug_public_rel
        global public_bug_patreon_rel
        global public_bug_other_rel
        bug_channel = await client.fetch_channel(public_bug_channel_id)
        if isinstance(bug_channel, discord.ForumChannel):
            public_bug_low_prio = next((tag for tag in bug_channel.available_tags if 'low' in tag.name.lower())).id
            public_bug_medium_prio = next((tag for tag in bug_channel.available_tags if 'medium' in tag.name.lower())).id
            public_bug_high_prio = next((tag for tag in bug_channel.available_tags if 'high' in tag.name.lower())).id
            public_bug_public_rel = next((tag for tag in bug_channel.available_tags if 'public' in tag.name.lower())).id
            public_bug_patreon_rel = next((tag for tag in bug_channel.available_tags if 'patreon' in tag.name.lower())).id
            public_bug_other_rel = next((tag for tag in bug_channel.available_tags if 'other' in tag.name.lower())).id
        else:
            await log(f'ERROR: Failed to get public bug channel tags: Channel {bug_channel} is not a forum channel')
            
    if key == 'PRIVATE_BUG_CHANNEL_ID':
        global private_bug_low_prio
        global private_bug_medium_prio
        global private_bug_high_prio
        global private_bug_public_rel
        global private_bug_patreon_rel
        global private_bug_other_rel
        bug_channel = await client.fetch_channel(public_bug_channel_id)
        if isinstance(bug_channel, discord.ForumChannel):
            private_bug_low_prio = next((tag for tag in bug_channel.available_tags if 'low' in tag.name.lower())).id
            private_bug_medium_prio = next((tag for tag in bug_channel.available_tags if 'medium' in tag.name.lower())).id
            private_bug_high_prio = next((tag for tag in bug_channel.available_tags if 'high' in tag.name.lower())).id
            private_bug_public_rel = next((tag for tag in bug_channel.available_tags if 'public' in tag.name.lower())).id
            private_bug_patreon_rel = next((tag for tag in bug_channel.available_tags if 'patreon' in tag.name.lower())).id
            private_bug_other_rel = next((tag for tag in bug_channel.available_tags if 'other' in tag.name.lower())).id
        else:
            await log(f'ERROR: Failed to get private bug channel tags: Channel {bug_channel} is not a forum channel')
            
    if key == 'SERVER_LISTINGS_CHANNEL_ID':
        global server_listings_tag_sur_adv
        global server_listings_tag_sur
        global server_listings_tag_adv
        global server_listings_tag_fabric
        global server_listings_tag_forge
        global server_listings_tag_essential
        global server_listings_tag_rp
        global server_listings_tag_casual
        global server_listings_tag_comp
        global server_listings_tag_custom_map
        global server_listings_tag_minigames
        global server_listings_tag_creative
        global server_listings_tag_premium
        global server_listings_tag_cracked
        server_listings_channel = await client.fetch_channel(server_listings_channel_id)
        if isinstance(server_listings_channel, discord.ForumChannel):
            server_listings_tag_sur_adv = next((tag for tag in server_listings_channel.available_tags if 'survival' in tag.name.lower() if 'adventure' in tag.name.lower())).id
            server_listings_tag_sur = next((tag for tag in server_listings_channel.available_tags if 'survival' in tag.name.lower() if 'adventure' not in tag.name.lower())).id
            server_listings_tag_adv = next((tag for tag in server_listings_channel.available_tags if 'adventure' in tag.name.lower() if 'survival' not in tag.name.lower())).id
            server_listings_tag_fabric = next((tag for tag in server_listings_channel.available_tags if 'fabric' in tag.name.lower())).id
            server_listings_tag_forge = next((tag for tag in server_listings_channel.available_tags if 'forge' in tag.name.lower())).id
            server_listings_tag_essential = next((tag for tag in server_listings_channel.available_tags if 'essential' in tag.name.lower())).id
            server_listings_tag_rp = next((tag for tag in server_listings_channel.available_tags if 'roleplay' in tag.name.lower())).id
            server_listings_tag_casual = next((tag for tag in server_listings_channel.available_tags if 'casual' in tag.name.lower())).id
            server_listings_tag_comp = next((tag for tag in server_listings_channel.available_tags if 'competitive' in tag.name.lower())).id
            server_listings_tag_custom_map = next((tag for tag in server_listings_channel.available_tags if 'custom map' in tag.name.lower())).id
            server_listings_tag_minigames = next((tag for tag in server_listings_channel.available_tags if 'minigames' in tag.name.lower())).id
            server_listings_tag_creative = next((tag for tag in server_listings_channel.available_tags if 'creative' in tag.name.lower())).id
            server_listings_tag_premium = next((tag for tag in server_listings_channel.available_tags if 'premium' in tag.name.lower())).id
            server_listings_tag_cracked = next((tag for tag in server_listings_channel.available_tags if 'cracked' in tag.name.lower())).id
            
        else:
            await log(f'ERROR: Failed to get private bug channel tags: Channel {bug_channel} is not a forum channel')
    

## Bug Reporter
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
        
        channel = await client.fetch_channel(public_bug_channel_id)

        priority_tags = {
            "Low": public_bug_low_prio,
            "Medium": public_bug_medium_prio,
            "High": public_bug_high_prio
        }

        release_tags = {
            "Public": public_bug_public_rel,
            "Patreon": public_bug_patreon_rel,
            "Other": public_bug_other_rel
        }

        applied_tags = [
            priority_tags.get(self.selected_options.get("priority")),
            release_tags.get(self.selected_options.get("release_type"))
        ]

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
            await log(f'ERROR: User <@{interaction.user.id}> encountered an issue when reporting a bug: Channel {channel} is not a forum channel!')

    async def on_error(self, interaction: discord.Interaction, error):
        await log(f'ERROR: User <@{interaction.user.id}> encountered an issue when reporting a bug: {error}')


@tree.command(name="bug", description="Report a bug!")
async def bug(interaction: discord.Interaction):
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

    await log(f'LOG: User <@{interaction.user.id}> ran command "bug" in channel {interaction.channel}')
    await interaction.response.send_message(
        "Before reporting your bug, please answer the following questions:", ephemeral=True, view=BugReportView()
    )

bug_report_cooldowns = {}

# @tree.command(name='verify_bug', description="Verify a bug report!")
# async def verify_bug(interaction: discord.Interaction):
#     pass

## Server Listings
class ServerListingDropdown(discord.ui.Select):
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

class ServerListingsConfirmButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Confirm", style=discord.ButtonStyle.green)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ServerListingModal(self.view.selected_options))
        message = await interaction.original_response()
        await message.edit(view=None)

class ServerListingView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.selected_options = {}
        
        self.add_item(ServerListingDropdown("Premium or Cracked", ["Premium", "Cracked"], "online"))
        self.add_item(ServerListingDropdown("Server Location", ["North America", "Central America", "South America", "Western Europe", "Eastern Europe", "Northern Europe", "Southern Europe", "Central Europe", "Oceania", "West Asia", "East Asia", "South Asia", "South East Asia", "Central Asia", "North Asia", "North Africa", "East Africa", "West Africa", "Central Africa", "South Africa"], "server_location"))
        self.add_item(ServerListingDropdown("Server Type", ["Survival + Adventure", "Survival", "Creative", "Adventure", "Roleplay", "Minigames"], "server_type"))
        self.add_item(ServerListingDropdown("Casual or Competitive", ["Casual", "Competitive"], "competitive"))
        self.add_item(ServerListingsConfirmButton())

class ServerListingModal(discord.ui.Modal):
    def __init__(self, selected_options):
        super().__init__(title="Post a Server Listing!")
        self.selected_options = selected_options
        
        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.short,
            label="Title",
            required=True,
            placeholder="What is the title of your server?"
        ))
        
        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.long,
            label="Description",
            required=True,
            placeholder="Give a description of your server. Provide all relevant information."
        ))
        
        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.short,
            label="IP Address",
            required=True,
            placeholder="Provide the IP address for your Minecraft server"
        ))
        
        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.short,
            label="Minecraft Version",
            required=True,
            placeholder="Provide the version of Minecraft your server uses."
        ))
        
        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.short,
            label="Discord Server (Not Required)",
            required=False,
            placeholder="Provide the link to a discord server associated with your server."
        ))
        
    async def on_submit(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        current_time = time.time()
        
        await interaction.response.defer(ephemeral=True)
        
        channel = await client.fetch_channel(server_listings_channel_id)

        server_type_tags = {
            "Survival + Adventure": server_listings_tag_sur_adv,
            "Survival": server_listings_tag_sur,
            "Creative": server_listings_tag_creative,
            "Adventure": server_listings_tag_adv,
            "Roleplay": server_listings_tag_rp,
            "Minigames": server_listings_tag_minigames
        }

        competitive_tags = {
            "Casual": server_listings_tag_casual,
            "Competitive": server_listings_tag_comp
        }
        
        online_tags = {
            "Premium": server_listings_tag_premium,
            "Cracked": server_listings_tag_cracked
        }

        applied_tags = [
            server_type_tags.get(self.selected_options.get("server_type")),
            competitive_tags.get(self.selected_options.get("competitive")),
            online_tags.get(self.selected_options.get("online"))
        ]

        applied_tags = [
            discord.Object(id=tag) for tag in [
                server_type_tags.get(self.selected_options.get("server_type")),
                competitive_tags.get(self.selected_options.get("competitive")),
                online_tags.get(self.selected_options.get("online"))
            ] if tag is not None
        ]

        if isinstance(channel, discord.ForumChannel):
            await channel.create_thread(
                name=self.children[0].value,
                content=f'# Server Listing from {interaction.user.mention}\n\n'
                        f'**Description:**\n {self.children[1].value}\n\n'
                        f'**IP Address:**\n{self.children[2].value}\n\n'
                        f'**Minecraft Version:**\n{self.children[3].value}\n\n'
                        f'**Discord Server:**\n{self.children[4].value}\n\n'
                        f'**Region:**\n{self.selected_options.get("server_location")}',
                applied_tags=applied_tags
            )
            
            server_listing_cooldowns[user_id] = current_time
            
            await interaction.followup.send("Server listing posted successfully!", ephemeral=True)
            
        else:
            await log(f'ERROR: User <@{interaction.user.id}> encountered an issue when posting a server listing: Channel {channel} is not a forum channel!')

    async def on_error(self, interaction: discord.Interaction, error):
        await log(f'ERROR: User <@{interaction.user.id}> encountered an issue when posting a server listing: {error}')


@tree.command(name="server_listing", description="Post a server listing!")
async def server_listing(interaction: discord.Interaction):
    user_id = interaction.user.id
    current_time = time.time()
    
    # Check if user is on cooldown
    if user_id in server_listing_cooldowns:
        last_used = server_listing_cooldowns[user_id]
        cooldown_time = 21600  # 6 hours
        time_left = cooldown_time - (current_time - last_used)

        if time_left > 0:
            await interaction.response.send_message(
                f"Please wait {int(time_left)} seconds before posting another server listing.", ephemeral=True
            )
            return

    await log(f'LOG: User <@{interaction.user.id}> ran command "server_listing" in channel {interaction.channel}')
    await interaction.response.send_message(
        "Before posting your server listing, please answer the following questions:", ephemeral=True, view=ServerListingView()
    )

server_listing_cooldowns = {}

## Help Commands
@tree.command(name='wiki',description='Get the link to the wiki!')
async def wiki(interaction:discord.Interaction):
    await interaction.response.send_message('https://sncraft.fanfus.com/wiki')
    await log(f'LOG: User {interaction.user.mention} ran command `wiki` in channel <#{interaction.channel_id}>')
    
@tree.command(name='villager_guide',description='Get the link Fanfo\'s video guide about villagers and reproduction!')
async def villager_guide(interaction:discord.Interaction):
    await interaction.response.send_message('https://www.youtube.com/watch?v=srcHjwWjUJ0')
    await log(f'LOG: User {interaction.user.mention} ran command `villager_guide` in channel <#{interaction.channel_id}>')

@tree.command(name='spawn_blocks',description='Check what blocks titans can spawn on!')
async def spawn_blocks(interaction:discord.Interaction):
    await interaction.response.send_message('https://cdn.discordapp.com/attachments/953767082703601757/1219415927397814312/image.png?ex=66147314&is=6601fe14&hm=32da2bc67612c32eab8ac253427dc8e6081d5ba64f402b7c0c15f753436b08ce&')
    await log(f'LOG: User {interaction.user.mention} ran command `spawn_blocks` in channel <#{interaction.channel_id}>')

@tree.command(name='sleep',description='A friendly reminder that sleep is important!')
async def sleep(interaction:discord.Interaction):
    await interaction.response.send_message('https://cdn.discordapp.com/attachments/953767082703601757/1057940256529338418/2022-12-29_00-32-51_Trim.mp4?ex=6617a124&is=66052c24&hm=fdcf67c315dce3e89b6b015219cdc339e29dce9ed5d4eb654ed602035545ae04&')
    await log(f'LOG: User {interaction.user.mention} ran command `sleep` in channel <#{interaction.channel_id}>')

@tree.command(name='shifter',description='Get the command to give yourself a shifter!')
async def shifter(interaction:discord.Interaction):
    await interaction.response.send_message('You can use `/function snc:api/get/shifter/[shifter]` to get a shifter, and just replace `[shifter]` with what you want')
    await log(f'LOG: User {interaction.user.mention} ran command `shifter` in channel <#{interaction.channel_id}>')

@tree.command(name='snc2',description='Get the link Shingeki no Craft 2!')
async def snc2(interaction:discord.Interaction):
    await interaction.response.send_message('https://www.planetminecraft.com/data-pack/shingeki-no-craft-2/')
    await log(f'LOG: User {interaction.user.mention} ran command `snc2` in channel <#{interaction.channel_id}>')

@tree.command(name='snc1',description='Get the link to Shingeki no Craft 1!')
async def snc1(interaction:discord.Interaction):
    await interaction.response.send_message('https://www.planetminecraft.com/data-pack/attack-on-titan-datapack-1-16-download/')
    await log(f'LOG: User {interaction.user.mention} ran command `snc1` in channel <#{interaction.channel_id}>')

@tree.command(name='patreon',description='Get help with linking your discord and patreon accounts!')
async def snc1(interaction:discord.Interaction):
    await interaction.response.send_message('If you are missing the Patreon status/roles try the following steps:\n\nGo to https://www.patreon.com/settings/apps/discord and ensure your Discord ID is correct.\nGo to https://www.patreon.com/settings/basics and change your display name, change it to anything and then change it back. This is your patreon display name, not discord.\nAlso make sure you appear as online when making these changes. sometimes appearing offline can stop the linking process.')
    await log(f'LOG: User {interaction.user.mention} ran command `patreon` in channel <#{interaction.channel_id}>')

@tree.command(name='modpack',description='Get the link to Fanfo\'s video about the modpack!')
async def modpack(interaction:discord.Interaction):
    await interaction.response.send_message('https://www.youtube.com/watch?v=bGrnwFEQxZ4')
    await log(f'LOG: User {interaction.user.mention} ran command `modpack` in channel <#{interaction.channel_id}>')

@tree.command(name='map',description='Get the link the Shinganshina map used in Fanfo\'s videos!')
async def map(interaction:discord.Interaction):
    await interaction.response.send_message('https://cdn.discordapp.com/attachments/953780982077616288/1153022566596870274/MapPreston.zip?ex=6612da72&is=66006572&hm=a440c24c26568f4f69d5ec7c98eb0c0583e9620025a1601a9de79445c146de8a&')
    await log(f'LOG: User {interaction.user.mention} ran command `map` in channel <#{interaction.channel_id}>')

@tree.command(name='install',description='A guide on how to install the pack!')
async def install(interaction:discord.Interaction):
    await interaction.response.send_message('If you are using the mod version, it is installed like a normal mod in fabric or forge. If you are using the datapack version, you can follow these guides:\nhttps://www.planetminecraft.com/blog/how-to-download-and-install-minecraft-data-packs/\nhttps://www.planetminecraft.com/blog/how-to-install-minecraft-texture-packs-4615399/')
    await log(f'LOG: User {interaction.user.mention} ran command `install` in channel <#{interaction.channel_id}>')

@tree.command(name='coral',description='Get a link to Fanfo\'s adventure map, Coral!')
async def coral(interaction:discord.Interaction):
    await interaction.response.send_message('https://www.planetminecraft.com/project/coral-5944252/')
    await log(f'LOG: User {interaction.user.mention} ran command `coral` in channel <#{interaction.channel_id}>')

@tree.command(name='snc_config',description='Get the command to access the config!')
async def snc_config(interaction:discord.Interaction):
    await interaction.response.send_message('`/function snc:api/config`')
    await log(f'LOG: User {interaction.user.mention} ran command `snc_config` in channel <#{interaction.channel_id}>')

@tree.command(name='chainsaw',description='Get a link to Fanfo\'s adventure map, Chainsaw Craft!')
async def chainsaw(interaction:discord.Interaction):
    await interaction.response.send_message('https://www.planetminecraft.com/project/chainsaw-craft-chainsaw-man-in-minecraft-vanilla/')
    await log(f'LOG: User {interaction.user.mention} ran command `chainsaw` in channel <#{interaction.channel_id}>')
    
@tree.command(name='server',description='Get the IP of the server!')
async def server(interaction:discord.Interaction):
    await interaction.response.send_message('IP: `snc.sparked.network`\nVersion: `1.21.8`')
    await log(f'LOG: User {interaction.user.mention} ran command `server` in channel <#{interaction.channel_id}>')

@tree.command(name='support',description='See how you can support SNC!')
async def support(interaction:discord.Interaction):
    await interaction.response.send_message('You can support SNC through several different ways, including [Patreon](https://www.patreon.com/join/8356530), [Ko-Fi](https://ko-fi.com/fanfo/tiers), boosting the server, which has the same rewards as buying Maria on Patreon or Ko-Fi, or just simply being here in the community. Never feel pressured to buy something you cannot afford.')
    await log(f'LOG: User {interaction.user.mention} ran command `support` in channel <#{interaction.channel_id}>')
    
@tree.command(name='elysium_archive',description='Get links to the world download of previous seasons of Elysium')
async def elysium_archive(interaction:discord.Interaction):
    await interaction.response.send_message('**Elysium S1 World Download:** <https://mega.nz/file/IdsiwawI#-ftkFRWad8lRG3_hxgnhxZk7yduVEcztZ2NzLiZfgBE>\n**Elysium S2 World Download:** <https://mega.nz/file/xYVnnKiQ#jBNhuyjWoPAeoydYIsa3G6IlerkO49h6ouP34oeu2ag>')
    await log(f'LOG: User {interaction.user.mention} ran command `elysium_archive` in channel <#{interaction.channel_id}>')


# Suggestions Manager
@client.event
async def on_raw_reaction_add(payload):
    try:
        channel = client.get_channel(payload.channel_id)
        
        if isinstance(channel, discord.Thread):
            parent_channel = channel.parent
            if parent_channel.id == suggestions_channel_id:
                message = await channel.fetch_message(payload.message_id)
                for reaction in message.reactions:
                    if reaction.count >= required_reactions and reaction.emoji == vote_reaction:
                        if not any(tag.id == review_tag_id or tag.id == accepted_tag_id or tag.id == rejected_tag_id or tag.id == discussion_tag_id for tag in channel.applied_tags):
                            review_tag = discord.utils.get(parent_channel.available_tags, id=review_tag_id)
                            accepted_tag = discord.utils.get(parent_channel.available_tags, id=accepted_tag_id)
                            rejected_tag = discord.utils.get(parent_channel.available_tags, id=rejected_tag_id)
                            if review_tag:
                                await log(f'LOG: Suggestion "{channel}" marked for review')
                                await channel.add_tags(review_tag)
                                await channel.send('This suggestion has been marked for review!')
                                review_channel = client.get_channel(review_channel_id)
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
                                view = SuggestionReviewView(original_thread=channel, review_embed=embed, review_tag=review_tag, accepted_tag=accepted_tag, rejected_tag=rejected_tag)
                                await review_channel.send(embed=embed, view=view)
                                
    except Exception as e:
        await log(f'ERROR: Encountered error when marking a suggestion for review: {e}')
                            
class SuggestionReviewView(View):
    def __init__(self, original_thread, review_embed, review_tag, accepted_tag, rejected_tag):
        super().__init__(timeout=None)
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
            await log(f'LOG: Suggestion "{self.original_thread.name}" has been accepted')
            
        except Exception as e:
            await interaction.response.send_message("An error occurred. Please check logs for more details.", ephemeral=True)
            await log(f'ERROR: Encountered error when accepting a suggestion: {e}')

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
            await log(f'LOG: Suggestion "{self.original_thread.name}" has been rejected')
            
        except Exception as e:
            await interaction.response.send_message("An error occurred. Please check logs for more details.", ephemeral=True)
            await log(f'ERROR: Encountered error when denying a suggestion: {e}')

@tree.command(name='mark_for_review',description='Mark a suggestion for review')
async def mark_for_review(interaction:discord):
    if interaction.user.id not in bot_admin:
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        await log(f'ERROR: User {interaction.user.mention} attempted to use `mark_for_review` without permission')
        return
    try:
        channel = client.get_channel(interaction.channel_id)
        
        if isinstance(channel, discord.Thread):
            parent_channel = channel.parent
            if parent_channel.id == suggestions_channel_id:
                message = await channel.fetch_message(interaction.channel.id)
                review_tag = discord.utils.get(parent_channel.available_tags, id=review_tag_id)
                accepted_tag = discord.utils.get(parent_channel.available_tags, id=accepted_tag_id)
                rejected_tag = discord.utils.get(parent_channel.available_tags, id=rejected_tag_id)
                if review_tag:
                    await log(f'LOG: Suggestion "{channel}" manually marked for review by {interaction.user.mention}')
                    await channel.add_tags(review_tag)
                    await channel.send('This suggestion has been marked for review!')
                    review_channel = client.get_channel(review_channel_id)
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
                    view = SuggestionReviewView(original_thread=channel, review_embed=embed, review_tag=review_tag, accepted_tag=accepted_tag, rejected_tag=rejected_tag)
                    await review_channel.send(embed=embed, view=view)
        await interaction.response.send_message("Succesfully marked suggestion for review!",ephemeral=True)
    except Exception as e:
        await interaction.response.send_message("An error occured. Check logs for more details.")
        await log(f'ERROR: Encountered error when manually marking a suggestion for review: {e}')
    
# Thread Pinning


# Modmail
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    modmail_channel = client.get_channel(modmail_channel_id)
    
    if isinstance(message.channel, discord.DMChannel):
        threads = list(modmail_channel.threads) + [thread async for thread in modmail_channel.archived_threads(limit=None)]
        open_threads = {thread.name: thread for thread in threads}
        user_thread_name = f"{message.author.id} - {message.author}"
        await log(f'LOG: Modmail recieved from user <@{message.author.id}>')

        if user_thread_name in open_threads:
            modmail_thread = open_threads[user_thread_name]
        else:
            create_thread = await modmail_channel.create_thread(
                name = user_thread_name,
                content = f"Modmail from {message.author.mention}",
                auto_archive_duration=10080 # 7 days
            )
            modmail_thread = create_thread.thread
            await log(f'LOG: Creating modmail thread for user <@{message.author.id}>')
        
        content = f"**[MODMAIL] {message.author.mention}:** {message.content}"
        files = []
        if message.attachments:
            for attachment in message.attachments:
                file = await attachment.to_file()
                files.append(file)
        await modmail_thread.send(content=content, files=files)
        await message.add_reaction("📨")
        
    
    if isinstance(message.channel, discord.Thread) and message.channel.parent_id == modmail_channel.id:
        user = await client.fetch_user(int(message.channel.name.split(" - ")[0]))
        content = f"**[MODMAIL] {message.author.mention}:** {message.content}"
        files = []
        if message.attachments:
            for attachment in message.attachments:
                file = await attachment.to_file()
                files.append(file)
        await user.send(content=content, files=files)
        await message.add_reaction("📨")
    

@client.event
async def on_message_edit(before, after):
    if before.author == client.user:
        return
    
    if isinstance(before.channel, discord.DMChannel):
        modmail_channel = client.get_channel(modmail_channel_id)
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

@client.event
async def on_message_delete(message):
    if message.author == client.user:
        return
    
    if isinstance(message.channel, discord.DMChannel):
        modmail_channel = client.get_channel(modmail_channel_id)
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


# Moderation



# Logs
@client.event
async def on_error(event, *args, **kwargs):
    import traceback
    error_message = traceback.format_exc()
    await log(f'ERROR: An error has occured: {event}: {error_message}')

async def log(message):
    print(message)
    log_channel = client.get_channel(log_channel_id)
    await log_channel.send(message.replace("LOG:","**LOG:**").replace("WARN:","**WARN:**").replace("ERROR:","**ERROR:**"))


client.run(TOKEN)