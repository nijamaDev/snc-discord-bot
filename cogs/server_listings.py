import discord
from discord import app_commands
from discord.ext import commands
import time
import config
from utils.logger import log

server_listing_cooldowns = {}

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
            style=discord.TextStyle.long,
            label="Extra Links",
            required=False,
            placeholder="Image link, discord server, etc"
        ))
        
    async def on_submit(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        current_time = time.time()
        
        await interaction.response.defer(ephemeral=True)
        
        channel = await interaction.client.fetch_channel(config.SERVER_LISTINGS_CHANNEL_ID)

        server_type_tags = {
            "Survival + Adventure": config.SERVER_LISTINGS_TAG_SUR_ADV,
            "Survival": config.SERVER_LISTINGS_TAG_SUR,
            "Creative": config.SERVER_LISTINGS_TAG_CREATIVE,
            "Adventure": config.SERVER_LISTINGS_TAG_ADV,
            "Roleplay": config.SERVER_LISTINGS_TAG_RP,
            "Minigames": config.SERVER_LISTINGS_TAG_MINIGAMES
        }

        competitive_tags = {
            "Casual": config.SERVER_LISTINGS_TAG_CASUAL,
            "Competitive": config.SERVER_LISTINGS_TAG_COMP
        }
        
        online_tags = {
            "Premium": config.SERVER_LISTINGS_TAG_PREMIUM,
            "Cracked": config.SERVER_LISTINGS_TAG_CRACKED
        }

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
                        f'**Region:**\n{self.selected_options.get("server_location")}\n\n'
                        f'**Extra Links:**\n{self.children[4].value}',
                applied_tags=applied_tags
            )
            
            server_listing_cooldowns[user_id] = current_time
            
            await interaction.followup.send("Server listing posted successfully!", ephemeral=True)
            
        else:
            await log(interaction.client, f'ERROR: User <@{interaction.user.id}> encountered an issue when posting a server listing: Channel {channel} is not a forum channel!')

    async def on_error(self, interaction: discord.Interaction, error):
        await log(interaction.client, f'ERROR: User <@{interaction.user.id}> encountered an issue when posting a server listing: {error}')


class ServerListing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="server_listing", description="Post a server listing!")
    async def server_listing(self, interaction: discord.Interaction):
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

        await log(self.bot, f'LOG: User <@{interaction.user.id}> ran command `server_listing` in channel <#{interaction.channel.id}>')
        await interaction.response.send_message(
            "Before posting your server listing, please answer the following questions:", ephemeral=True, view=ServerListingView()
        )

async def setup(bot):
    await bot.add_cog(ServerListing(bot))
