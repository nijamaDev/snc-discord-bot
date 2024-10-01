# bot.py
import os

import discord
from discord import app_commands
from dotenv import load_dotenv
from discord.ext import commands
from discord.ui import View, Button

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Define intents
intents = discord.Intents.all()

# Initialize client with intents
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Runs on startup
@client.event
async def on_ready():
    await tree.sync()
    await log(f'LOG: {client.user} has connected to Discord!')
    
    # Get Vote Reaction
    global vote_reaction
    suggestions_channel = client.get_channel(suggestions_channel_id)
    if isinstance(suggestions_channel, discord.ForumChannel):
        if suggestions_channel.default_reaction_emoji:
            vote_reaction = suggestions_channel.default_reaction_emoji
            await log(f'LOG: Vote reaction found for channel {suggestions_channel_id}')
        else:
            await log('WARN: No vote reaction found, using default')
            vote_reaction = "👍"
    else:
        await log(f'ERROR: Channel {suggestions_channel_id} is not a forum channel')
    
# Define Vars
#Suggestions Manager
suggestions_channel_id = 1290029333032992851
review_channel_id = 1290029369221451927
review_tag_id = 1290046590014197880
accepted_tag_id = 1290451565630591027
rejected_tag_id = 1290451579174129745
required_reactions = 1

# Misc
log_channel_id = 1290466081668071455
    
# Commands
@tree.command(name='wiki',description='Get the link to the wiki!')
async def wiki(interaction:discord.Interaction):
    await interaction.response.send_message('https://sncraft.fanfus.com/wiki')
    await log(f'LOG: {interaction.user} ran command "wiki" in channel {interaction.channel}')
    
@tree.command(name='villager_guide',description='Get the link Fanfo\'s video guide about villagers and reproduction!')
async def villager_guide(interaction:discord.Interaction):
    await interaction.response.send_message('https://www.youtube.com/watch?v=srcHjwWjUJ0')
    await log(f'LOG: {interaction.user} ran command "villager_guide" in channel {interaction.channel}')

@tree.command(name='spawn_blocks',description='Check what blcoks titans can spawn on!')
async def spawn_blocks(interaction:discord.Interaction):
    await interaction.response.send_message('https://cdn.discordapp.com/attachments/953767082703601757/1219415927397814312/image.png?ex=66147314&is=6601fe14&hm=32da2bc67612c32eab8ac253427dc8e6081d5ba64f402b7c0c15f753436b08ce&')
    await log(f'LOG: {interaction.user} ran command "spawn_blocks" in channel {interaction.channel}')

@tree.command(name='sleep',description='A friendly reminder that sleep is important!')
async def sleep(interaction:discord.Interaction):
    await interaction.response.send_message('https://cdn.discordapp.com/attachments/953767082703601757/1057940256529338418/2022-12-29_00-32-51_Trim.mp4?ex=6617a124&is=66052c24&hm=fdcf67c315dce3e89b6b015219cdc339e29dce9ed5d4eb654ed602035545ae04&')
    await log(f'LOG: {interaction.user} ran command "sleep" in channel {interaction.channel}')

@tree.command(name='shifter',description='Get the command to give yourself a shifter!')
async def shifter(interaction:discord.Interaction):
    await interaction.response.send_message('You can use `/function snc:api/get/shifter/[shifter]` to get a shifter, and just replace `[shifter]` with what you want')
    await log(f'LOG: {interaction.user} ran command "shifter" in channel {interaction.channel}')

@tree.command(name='snc2',description='Get the link Shingeki no Craft 2!')
async def snc2(interaction:discord.Interaction):
    await interaction.response.send_message('https://www.planetminecraft.com/data-pack/shingeki-no-craft-2/')
    await log(f'LOG: {interaction.user} ran command "snc2" in channel {interaction.channel}')

@tree.command(name='snc1',description='Get the link to Shingeki no Craft 1!')
async def snc1(interaction:discord.Interaction):
    await interaction.response.send_message('https://www.planetminecraft.com/data-pack/attack-on-titan-datapack-1-16-download/')
    await log(f'LOG: {interaction.user} ran command "snc1" in channel {interaction.channel}')

@tree.command(name='patreon',description='Get help with linking your discord and patreon accounts!')
async def snc1(interaction:discord.Interaction):
    await interaction.response.send_message('If you are missing the Patreon status/roles try the following steps:\n\nGo to https://www.patreon.com/settings/apps/discord and ensure your Discord ID is correct.\nGo to https://www.patreon.com/settings/basics and change your display name, change it to anything and then change it back. This is your patreon display name, not discord.\nAlso make sure you appear as online when making these changes. sometimes appearing offline can stop the linking process.')
    await log(f'LOG: {interaction.user} ran command "patreon" in channel {interaction.channel}')

@tree.command(name='modpack',description='Get the link to Fanfo\'s video about the modpack!')
async def modpack(interaction:discord.Interaction):
    await interaction.response.send_message('https://www.youtube.com/watch?v=bGrnwFEQxZ4')
    await log(f'LOG: {interaction.user} ran command "modpack" in channel {interaction.channel}')

@tree.command(name='map',description='Get the link the Shinganshina map used in Fanfo\'s videos!')
async def map(interaction:discord.Interaction):
    await interaction.response.send_message('https://cdn.discordapp.com/attachments/953780982077616288/1153022566596870274/MapPreston.zip?ex=6612da72&is=66006572&hm=a440c24c26568f4f69d5ec7c98eb0c0583e9620025a1601a9de79445c146de8a&')
    await log(f'LOG: {interaction.user} ran command "map" in channel {interaction.channel}')

@tree.command(name='install',description='A guide on how to install the pack!')
async def install(interaction:discord.Interaction):
    await interaction.response.send_message('If you are using the mod version, it is installed like a normal mod in fabric or forge. If you are using the datapack version, you can follow these guides:\nhttps://www.planetminecraft.com/blog/how-to-download-and-install-minecraft-data-packs/\nhttps://www.planetminecraft.com/blog/how-to-install-minecraft-texture-packs-4615399/')
    await log(f'LOG: {interaction.user} ran command "install" in channel {interaction.channel}')

@tree.command(name='coral',description='Get a link to Fanfo\'s adventure map, Coral!')
async def coral(interaction:discord.Interaction):
    await interaction.response.send_message('https://www.planetminecraft.com/project/coral-5944252/')
    await log(f'LOG: {interaction.user} ran command "coral" in channel {interaction.channel}')

@tree.command(name='config',description='Get the command to access the wiki!')
async def config(interaction:discord.Interaction):
    await interaction.response.send_message('`/function snc:api/config`')
    await log(f'LOG: {interaction.user} ran command "config" in channel {interaction.channel}')

@tree.command(name='chainsaw',description='Get a link to Fanfo\'s adventure map, Chainsaw Craft!')
async def chainsaw(interaction:discord.Interaction):
    await interaction.response.send_message('https://www.planetminecraft.com/project/chainsaw-craft-chainsaw-man-in-minecraft-vanilla/')
    await log(f'LOG: {interaction.user} ran command "chainsaw" in channel {interaction.channel}')



# Suggestions Manager
@client.event
async def on_raw_reaction_add(payload):
    channel = client.get_channel(payload.channel_id)
    
    if isinstance(channel, discord.Thread):
        parent_channel = channel.parent
        if parent_channel.id == suggestions_channel_id:
             message = await channel.fetch_message(payload.message_id)
             for reaction in message.reactions:
                 if reaction.count >= required_reactions and reaction.emoji == vote_reaction:
                    if not any(tag.id == review_tag_id or tag.id == accepted_tag_id or tag.id == rejected_tag_id for tag in channel.applied_tags):
                        review_tag_object = discord.utils.get(parent_channel.available_tags, id=review_tag_id)
                        accepted_tag_object = discord.utils.get(parent_channel.available_tags, id=accepted_tag_id)
                        rejected_tag_object = discord.utils.get(parent_channel.available_tags, id=rejected_tag_id)
                        if review_tag_object:
                            await log(f'LOG: Suggestion "{channel}" marked for review')
                            await channel.add_tags(review_tag_object)
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
                            view = SuggestionReviewView(original_thread=channel, review_embed=embed, review_tag=review_tag_object, accepted_tag=accepted_tag_object, rejected_tag=rejected_tag_object)
                            await review_channel.send(embed=embed, view=view)
                            
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
        # Remove 'Under Review' tag, add 'Accepted' tag
        await self.original_thread.add_tags(self.accepted_tag)
        await self.original_thread.remove_tags(self.review_tag)
        self.review_embed.color = discord.Color.green()
        self.review_embed.title = f"Accepted: {self.original_thread.name}" 

        await interaction.message.edit(embed=self.review_embed, view=None)
        await interaction.response.send_message("Suggestion accepted!", ephemeral=True)
        await self.original_thread.send("This suggestion has been accepted!")
        await log(f'LOG: Suggestion "{self.original_thread.name}" has been accepted')

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.danger)
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Remove 'Under Review' tag, add 'Rejected' tag
        await self.original_thread.add_tags(self.rejected_tag)
        await self.original_thread.remove_tags(self.review_tag)
        self.review_embed.color = discord.Color.red()
        self.review_embed.title = f"Rejected: {self.original_thread.name}" 

        await interaction.message.edit(embed=self.review_embed, view=None)
        await interaction.response.send_message("Suggestion rejected!", ephemeral=True)
        await self.original_thread.send("This suggestion has been rejected!")
        await log(f'LOG: Suggestion "{self.original_thread.name}" has been rejected')
        
# Logs
async def log(message):
    print(message)
    log_channel = client.get_channel(log_channel_id)
    await log_channel.send(message.replace("LOG:","**LOG:**").replace("WARN:","**WARN:**").replace("ERROR:","**ERROR:**"))

# Modmail


# Moderation


client.run(TOKEN)