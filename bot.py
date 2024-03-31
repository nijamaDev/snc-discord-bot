# bot.py
import os

import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Define intents
intents = discord.Intents.default()
intents.messages = True  # Assuming you want the bot to read messages
intents.message_content = True

# Initialize client with intents
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Runs on startup
@client.event
async def on_ready():
    await tree.sync()
    print(f'{client.user} has connected to Discord!')
    
# Commands
@tree.command(name='wiki',description='Get the link to the wiki!')
async def wiki(interaction:discord.Interaction):
    await interaction.response.send_message('https://sncraft.fanfus.com/wiki')
    
@tree.command(name='villager_guide',description='Get the link Fanfo\'s video guide about villagers and reproduction!')
async def villager_guide(interaction:discord.Interaction):
    await interaction.response.send_message('https://www.youtube.com/watch?v=srcHjwWjUJ0')
    
@tree.command(name='spawn_blocks',description='Check what blcoks titans can spawn on!')
async def spawn_blocks(interaction:discord.Interaction):
    await interaction.response.send_message('https://cdn.discordapp.com/attachments/953767082703601757/1219415927397814312/image.png?ex=66147314&is=6601fe14&hm=32da2bc67612c32eab8ac253427dc8e6081d5ba64f402b7c0c15f753436b08ce&')
    
@tree.command(name='sleep',description='A friendly reminder that sleep is important!')
async def sleep(interaction:discord.Interaction):
    await interaction.response.send_message('https://cdn.discordapp.com/attachments/953767082703601757/1057940256529338418/2022-12-29_00-32-51_Trim.mp4?ex=6617a124&is=66052c24&hm=fdcf67c315dce3e89b6b015219cdc339e29dce9ed5d4eb654ed602035545ae04&')

@tree.command(name='shifter',description='Get the command to give yourself a shifter!')
async def shifter(interaction:discord.Interaction):
    await interaction.response.send_message('You can use `/function snc:api/get/shifter/[shifter]` to get a shifter, and just replace `[shifter]` with what you want')
    
@tree.command(name='snc2',description='Get the link Shingeki no Craft 2!')
async def snc2(interaction:discord.Interaction):
    await interaction.response.send_message('https://www.planetminecraft.com/data-pack/shingeki-no-craft-2/')
    
@tree.command(name='snc1',description='Get the link to Shingeki no Craft 1!')
async def snc1(interaction:discord.Interaction):
    await interaction.response.send_message('https://www.planetminecraft.com/data-pack/attack-on-titan-datapack-1-16-download/')
    
@tree.command(name='modpack',description='Get the link to Fanfo\'s video about the modpack!')
async def modpack(interaction:discord.Interaction):
    await interaction.response.send_message('https://www.youtube.com/watch?v=bGrnwFEQxZ4')
    
@tree.command(name='map',description='Get the link the Shinganshina map used in Fanfo\'s videos!')
async def map(interaction:discord.Interaction):
    await interaction.response.send_message('https://cdn.discordapp.com/attachments/953780982077616288/1153022566596870274/MapPreston.zip?ex=6612da72&is=66006572&hm=a440c24c26568f4f69d5ec7c98eb0c0583e9620025a1601a9de79445c146de8a&')
    
@tree.command(name='install',description='A guide on how to install the pack!')
async def install(interaction:discord.Interaction):
    await interaction.response.send_message('If you are using the mod version, it is installed like a normal mod in fabric or forge. If you are using the datapack version, you can follow these guides:\nhttps://www.planetminecraft.com/blog/how-to-download-and-install-minecraft-data-packs/\nhttps://www.planetminecraft.com/blog/how-to-install-minecraft-texture-packs-4615399/')
    
@tree.command(name='coral',description='Get a link to Fanfo\'s adventure map, Coral!')
async def coral(interaction:discord.Interaction):
    await interaction.response.send_message('https://www.planetminecraft.com/project/coral-5944252/')
    
@tree.command(name='config',description='Get the command to access the wiki!')
async def config(interaction:discord.Interaction):
    await interaction.response.send_message('`/function snc:api/config`')
    
@tree.command(name='chainsaw',description='Get a link to Fanfo\'s adventure map, Chainsaw Craft!')
async def chainsaw(interaction:discord.Interaction):
    await interaction.response.send_message('https://www.planetminecraft.com/project/chainsaw-craft-chainsaw-man-in-minecraft-vanilla/')
    

client.run(TOKEN)