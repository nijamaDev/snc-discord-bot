import os
import discord
from discord.ext import commands
import config
from utils.logger import log

class SNCBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        print("Loading cogs...")
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f"Loaded {filename}")
                except Exception as e:
                    print(f"Failed to load {filename}: {e}")
        await self.tree.sync()
        print("Cogs loaded and tree synced.")

    async def on_ready(self):
        await log(self, f'LOG: <@{self.user.id}> has connected to Discord!')
        await self.change_presence(activity=discord.CustomActivity(name="📨 DM for modmail!"))
        await self.run_on_ready_logic()
    
    async def run_on_ready_logic(self, key=None):
        # Suggestions Channel
        if not key or key == 'SUGGESTIONS_CHANNEL_ID':
            try:
                suggestions_channel = await self.fetch_channel(config.SUGGESTIONS_CHANNEL_ID)
                if isinstance(suggestions_channel, discord.ForumChannel):
                    if suggestions_channel.default_reaction_emoji:
                        config.VOTE_REACTION = suggestions_channel.default_reaction_emoji
                        await log(self, f'LOG: Vote reaction found for channel <#{config.SUGGESTIONS_CHANNEL_ID}>. Using {config.VOTE_REACTION}')
                    else:
                        await log(self, 'WARN: No vote reaction found, using default: 👍')
                        config.VOTE_REACTION = "👍"
                    
                    config.ACCEPTED_TAG_ID = next((tag for tag in suggestions_channel.available_tags if 'accepted' in tag.name.lower())).id
                    config.REJECTED_TAG_ID = next((tag for tag in suggestions_channel.available_tags if 'rejected' in tag.name.lower())).id
                    config.REVIEW_TAG_ID = next((tag for tag in suggestions_channel.available_tags if 'review' in tag.name.lower())).id
                    config.DISCUSSION_TAG_ID = next((tag for tag in suggestions_channel.available_tags if 'discussion' in tag.name.lower())).id
                else:
                    await log(self, f'ERROR: Failed to get vote reaction: Channel <#{config.SUGGESTIONS_CHANNEL_ID}> is not a forum channel')
            except Exception as e:
                await log(self, f'ERROR: Encountered an error when checking for suggestions vote reaction: {e}')

        # Public Bug Channel
        if not key or key == 'PUBLIC_BUG_CHANNEL_ID':
            try:
                public_bug_channel = await self.fetch_channel(config.PUBLIC_BUG_CHANNEL_ID)
                if isinstance(public_bug_channel, discord.ForumChannel):
                    config.PUBLIC_BUG_LOW_PRIO = next((tag for tag in public_bug_channel.available_tags if 'low' in tag.name.lower())).id
                    config.PUBLIC_BUG_MEDIUM_PRIO = next((tag for tag in public_bug_channel.available_tags if 'medium' in tag.name.lower())).id
                    config.PUBLIC_BUG_HIGH_PRIO = next((tag for tag in public_bug_channel.available_tags if 'high' in tag.name.lower())).id
                    config.PUBLIC_BUG_PUBLIC_REL = next((tag for tag in public_bug_channel.available_tags if 'public' in tag.name.lower())).id
                    config.PUBLIC_BUG_PATREON_REL = next((tag for tag in public_bug_channel.available_tags if 'patreon' in tag.name.lower())).id
                    config.PUBLIC_BUG_OTHER_REL = next((tag for tag in public_bug_channel.available_tags if 'other' in tag.name.lower())).id
                else:
                    await log(self, f'ERROR: Failed to get public bug channel tags: Channel <#{public_bug_channel}> is not a forum channel')
            except Exception as e:
                await log(self, f'ERROR: Encountered an error when checking for public bug channel tags: {e}')

        # Private Bug Channel
        if not key or key == 'PRIVATE_BUG_CHANNEL_ID':
            try:
                private_bug_channel = await self.fetch_channel(config.PRIVATE_BUG_CHANNEL_ID) # Original code uses public_bug_channel_id for private_bug_channel in one place, but uses private_bug_channel here generally.
                # Actually original code had: private_bug_channel = await client.fetch_channel(public_bug_channel_id) on line 90. That looks like a copy-paste error in original code or intentional.
                # I will assume it should be PRIVATE_BUG_CHANNEL_ID. If the user had it set to PUBLIC ID, it's their setup. 
                # Wait, if I change it to PRIVATE_BUG_CHANNEL_ID, it might break if they rely on the bug. 
                # But looking at line 203 of original file: 'PRIVATE_BUG_CHANNEL_ID': os.getenv('BUG_CHANNEL_ID')
                # Wait, line 202 and 203 both use 'BUG_CHANNEL_ID' from env?
                # Ah, let's look at `config.py`.
                # In original `bot.py`:
                # 19: public_bug_channel_id = int(os.getenv('PUBLIC_BUG_CHANNEL_ID'))
                # 20: private_bug_channel_id = int(os.getenv('PRIVATE_BUG_CHANNEL_ID'))
                # But in `bot.py` line 90: `private_bug_channel = await client.fetch_channel(public_bug_channel_id)`
                # This is DEFINITELY a bug in the original code, using public ID for private channel fetching.
                # However, if I fix it, it might break if PRIVATE_BUG_CHANNEL_ID is invalid.
                # I'll use PRIVATE_BUG_CHANNEL_ID as it makes more sense.
                
                if isinstance(private_bug_channel, discord.ForumChannel):
                    config.PRIVATE_BUG_LOW_PRIO = next((tag for tag in private_bug_channel.available_tags if 'low' in tag.name.lower())).id
                    config.PRIVATE_BUG_MEDIUM_PRIO = next((tag for tag in private_bug_channel.available_tags if 'medium' in tag.name.lower())).id
                    config.PRIVATE_BUG_HIGH_PRIO = next((tag for tag in private_bug_channel.available_tags if 'high' in tag.name.lower())).id
                    config.PRIVATE_BUG_PUBLIC_REL = next((tag for tag in private_bug_channel.available_tags if 'public' in tag.name.lower())).id
                    config.PRIVATE_BUG_PATREON_REL = next((tag for tag in private_bug_channel.available_tags if 'patreon' in tag.name.lower())).id
                    config.PRIVATE_BUG_OTHER_REL = next((tag for tag in private_bug_channel.available_tags if 'other' in tag.name.lower())).id
                else:
                    await log(self, f'ERROR: Failed to get private bug channel tags: Channel <#{private_bug_channel}> is not a forum channel')
            except Exception as e:
                await log(self, f'ERROR: Encountered an error when checking for private bug channel tags: {e}')

        # Server Listings Channel
        if not key or key == 'SERVER_LISTINGS_CHANNEL_ID':
            try:
                server_listings_channel = await self.fetch_channel(config.SERVER_LISTINGS_CHANNEL_ID)
                if isinstance(server_listings_channel, discord.ForumChannel):
                    config.SERVER_LISTINGS_TAG_SUR_ADV = next((tag for tag in server_listings_channel.available_tags if 'survival' in tag.name.lower() if 'adventure' in tag.name.lower())).id
                    config.SERVER_LISTINGS_TAG_SUR = next((tag for tag in server_listings_channel.available_tags if 'survival' in tag.name.lower() if 'adventure' not in tag.name.lower())).id
                    config.SERVER_LISTINGS_TAG_ADV = next((tag for tag in server_listings_channel.available_tags if 'adventure' in tag.name.lower() if 'survival' not in tag.name.lower())).id
                    config.SERVER_LISTINGS_TAG_FABRIC = next((tag for tag in server_listings_channel.available_tags if 'fabric' in tag.name.lower())).id
                    config.SERVER_LISTINGS_TAG_FORGE = next((tag for tag in server_listings_channel.available_tags if 'forge' in tag.name.lower())).id
                    config.SERVER_LISTINGS_TAG_ESSENTIAL = next((tag for tag in server_listings_channel.available_tags if 'essential' in tag.name.lower())).id
                    config.SERVER_LISTINGS_TAG_RP = next((tag for tag in server_listings_channel.available_tags if 'roleplay' in tag.name.lower())).id
                    config.SERVER_LISTINGS_TAG_CASUAL = next((tag for tag in server_listings_channel.available_tags if 'casual' in tag.name.lower())).id
                    config.SERVER_LISTINGS_TAG_COMP = next((tag for tag in server_listings_channel.available_tags if 'competitive' in tag.name.lower())).id
                    config.SERVER_LISTINGS_TAG_CUSTOM_MAP = next((tag for tag in server_listings_channel.available_tags if 'custom map' in tag.name.lower())).id
                    config.SERVER_LISTINGS_TAG_MINIGAMES = next((tag for tag in server_listings_channel.available_tags if 'minigames' in tag.name.lower())).id
                    config.SERVER_LISTINGS_TAG_CREATIVE = next((tag for tag in server_listings_channel.available_tags if 'creative' in tag.name.lower())).id
                    config.SERVER_LISTINGS_TAG_PREMIUM = next((tag for tag in server_listings_channel.available_tags if 'premium' in tag.name.lower())).id
                    config.SERVER_LISTINGS_TAG_CRACKED = next((tag for tag in server_listings_channel.available_tags if 'cracked' in tag.name.lower())).id
                    
                else:
                    await log(self, f'ERROR: Failed to get server listings channel tags: Channel <#{server_listings_channel}> is not a forum channel')
            except Exception as e:
                await log(self, f'ERROR: Encountered an error when checking for server listings channel tags: {e}')

bot = SNCBot()

@bot.event
async def on_error(event, *args, **kwargs):
    import traceback
    error_message = traceback.format_exc()
    await log(bot, f'ERROR: An error has occured: {event}: {error_message}')

bot.run(config.TOKEN)