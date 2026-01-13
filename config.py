import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
SUGGESTIONS_CHANNEL_ID = int(os.getenv('SUGGESTIONS_CHANNEL_ID'))
REVIEW_CHANNEL_ID = int(os.getenv('REVIEW_CHANNEL_ID'))
REQUIRED_REACTIONS = int(os.getenv('REQUIRED_REACTIONS'))
LOG_CHANNEL_ID = int(os.getenv('LOG_CHANNEL_ID'))
MODMAIL_CHANNEL_ID = int(os.getenv('MODMAIL_CHANNEL_ID'))
PUBLIC_BUG_CHANNEL_ID = int(os.getenv('PUBLIC_BUG_CHANNEL_ID'))
PRIVATE_BUG_CHANNEL_ID = int(os.getenv('PRIVATE_BUG_CHANNEL_ID'))
SERVER_LISTINGS_CHANNEL_ID = int(os.getenv('SERVER_LISTINGS_CHANNEL_ID'))

BOT_ADMIN = [
    293738089787031552, # Fanfo
    279823686532333570, # Nijama
    690342949556584690, # Bomb
    760834405559304202 # Energy
]

# Runtime variables
VOTE_REACTION = "👍"
ACCEPTED_TAG_ID = 0
REJECTED_TAG_ID = 0
REVIEW_TAG_ID = 0
DISCUSSION_TAG_ID = 0

PUBLIC_BUG_LOW_PRIO = 0
PUBLIC_BUG_MEDIUM_PRIO = 0
PUBLIC_BUG_HIGH_PRIO = 0
PUBLIC_BUG_PUBLIC_REL = 0
PUBLIC_BUG_PATREON_REL = 0
PUBLIC_BUG_OTHER_REL = 0

PRIVATE_BUG_LOW_PRIO = 0
PRIVATE_BUG_MEDIUM_PRIO = 0
PRIVATE_BUG_HIGH_PRIO = 0
PRIVATE_BUG_PUBLIC_REL = 0
PRIVATE_BUG_PATREON_REL = 0
PRIVATE_BUG_OTHER_REL = 0

SERVER_LISTINGS_TAG_SUR_ADV = 0
SERVER_LISTINGS_TAG_SUR = 0
SERVER_LISTINGS_TAG_ADV = 0
SERVER_LISTINGS_TAG_FABRIC = 0
SERVER_LISTINGS_TAG_FORGE = 0
SERVER_LISTINGS_TAG_ESSENTIAL = 0
SERVER_LISTINGS_TAG_RP = 0
SERVER_LISTINGS_TAG_CASUAL = 0
SERVER_LISTINGS_TAG_COMP = 0
SERVER_LISTINGS_TAG_CUSTOM_MAP = 0
SERVER_LISTINGS_TAG_MINIGAMES = 0
SERVER_LISTINGS_TAG_CREATIVE = 0
SERVER_LISTINGS_TAG_PREMIUM = 0
SERVER_LISTINGS_TAG_CRACKED = 0

def update_runtime_var(key, value):
    globals()[key] = value

async def update_env_var(key, value):
    # Read current .env file content
    try:
        with open('.env', 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

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

    # Update the vars in the memory
    globals()[key] = value
    if key.endswith('_ID') or key == 'REQUIRED_REACTIONS':
         globals()[key] = int(value)