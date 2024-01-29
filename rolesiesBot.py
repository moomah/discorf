import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random
import emoji
import asyncio
# Loading environment variables .env
load_dotenv()

# Access the bot token

discord_bot_token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.errors.HTTPException):
        print(f"Discord HTTPException: {error.text}")
    else:
        print(f"An error occurred: {type(error).__name__} - {error}")

# Custom emoji unicode to change roles in discord server
@bot.event
async def on_reaction_add(reaction, user):
    #Check if the reaction is added to the correct message and by a non-bot user
    if reaction.message.content == "React to this message to assign multiple roles!" and not user.bot:
        #Define the role names associated with each reaction and their corresponding Discord custom emoji syntax
        reaction_roles = {
            '<:CoX:1201538577528537219>': 'CoX',
            '<:ToB:1201538593810821220>': 'ToB',
            '<:ToA:1201538606855098498>': 'ToA',
            '<:nightmare:1201538519865249903>': 'nightmare',
            '<:gwd:1201538553906212884>': 'gwd',
            '<:nex:1201538536936062996>': 'nex'
        }

        #Get the role associated with the reaction
        role_name = reaction_roles.get(str(reaction.emoji))
        if role_name:
            role = discord.utils.get(user.guild.roles, name=role_name)
            if role:
                # Add the role to the user
                await asyncio.sleep(2)
                await user.add_roles(role)


# Command to send a message with reactions for role assignments
@bot.command(name='reactionmessage')
async def reaction_message(ctx, channel: discord.TextChannel = None):
    # Discord custom emoji syntax for the custom emojis
    custom_emoji_syntax = [':CoX:1201538577528537219', ':ToB:1201538593810821220', ':ToA:1201538606855098498', ':nightmare:1201538519865249903', ':gwd:1201538553906212884', ':nex:1201538536936062996']

    try:
        #Send a message with reactions to the specified channel or the current channel if not specified
        message_channel = channel if channel else ctx.channel
        message = await message_channel.send("React to this message to assign multiple roles!")
        for emoji_syntax in custom_emoji_syntax:
            #Converting Discord custom emoji syntax to Unicode
            unicode_representation = emoji.emojize(emoji_syntax)
            await message.add_reaction(unicode_representation)

        await ctx.send(f"Message with reactions sent to {message_channel.mention}. React to assign multiple roles.")
    except discord.Forbidden:
        await ctx.send("I don't have the permission to send messages or add reactions.")

@bot.event
async def on_reaction_remove(reaction, user):
    #Check if the reaction is removed from the correct message
    if reaction.message.content == "React to this message to assign multiple roles!" and not user.bot:
        #Define the role names associated with each reaction and their corresponding ID
        reaction_roles = {
            1201538577528537219: 'CoX',  # id for :CoX:
            1201538593810821220: 'ToB',  # id for :ToB:
            1201538606855098498: 'ToA',  # id for :ToA:
            1201538519865249903: 'nightmare',  # id for :nightmare:
            1201538553906212884: 'gwd',  # id for :gwd:
            1201538536936062996: 'nex'  # id for :nex:
        }

        # Get the role associated with the reaction
        role_name = reaction_roles.get(reaction.emoji.id)
        if role_name:
            role = discord.utils.get(user.guild.roles, name=role_name)
            if role:
                # Remove the role from the user
                await asyncio.sleep(2)
                await user.remove_roles(role)


#Responding to users when they mention rolesios-mcbotty
        
        #List of responses
responses = [
    "How you diddly do {username}!",
    "YEEEHAAWWW {username}!",
    "Hello {username}! Have you chose any roles yet? If not that makes me sad because that's why I am here :(",
    "Howdy partner {username}!",
    "Yabadabadoo {username}!"
]

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    # debugging message
    print(f"Received message: {message.content}")
    # Ignore messages from bot itself to prevent infinite loops (though would be fun)
    if message.author == bot.user:
        return

    #Checking if the bots name is in the message
    if bot.user.name.lower() in message.content.lower():
        #Randomly select a response
        response = random.choice(responses)
        #Format the response with the user's mention
        response = response.format(username=message.author.mention)

        #debugging response
        print(f"Sending response: {response}")
        await message.channel.send(response)

        #Check if the word "rat" is mentioned in the message content
    #if 'rat' in message.content.lower():
        # Respond to the mention of "rat"
        #await message.channel.send("There is only one rat in here, and you know who it is!")

    # You can add more conditions and responses based on your requirements

    # Process commands
    await bot.process_commands(message)

# Using bot token
bot.run(discord_bot_token)