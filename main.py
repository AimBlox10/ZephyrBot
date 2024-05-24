import discord
from discord.ext import commands
import os

# Bot token
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# File to store kick and ban history
HISTORY_FILE = 'history.txt'

# Intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True 
intents.message_content = True

# Specify the role IDs that are allowed to use the commands
allowed_roles = [1243285427817943212, 1243300734011834499]

# Function to check if user has allowed roles
def has_allowed_role(ctx):
    return any(role.id in allowed_roles for role in ctx.author.roles)

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Event to confirm bot is ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Updated Command to kick a user
@bot.command()
@commands.check(has_allowed_role)
async def kick(ctx, member: discord.Member, *, reason='No reason provided'):
    try:
        await member.send(f'You have been kicked from {ctx.guild.name} for the following reason: {reason}')
    except discord.Forbidden:
        await ctx.reply(f'Could not send DM to {member.mention}. Proceeding with kick.')

    await member.kick(reason=reason)
    await ctx.reply(f'{member.mention} has been kicked for : {reason}')

    # Save kick history to file with the correct format
    with open(HISTORY_FILE, 'a') as file:
        file.write(f'KICK: {member.id} - {member.name} - {reason}\n')

# Command to ban a user
@bot.command()
@commands.check(has_allowed_role)
async def ban(ctx, member: discord.Member, *, reason='No reason provided'):
    try:
        await member.send(f'You have been banned from {ctx.guild.name} for the following reason: {reason}')
    except discord.Forbidden:
        await ctx.reply(f'Could not send DM to {member.mention}. Proceeding with ban.')

    await member.ban(reason=reason)
    await ctx.reply(f'{member.mention} has been banned for : {reason}')
    # Save ban history to file
    with open(HISTORY_FILE, 'a') as file:
        file.write(f'BAN: {member.id} - {member.name} - {reason}\n')

# Command to show kick and ban history
@bot.command()
@commands.check(has_allowed_role)
async def history(ctx):
    try:
        with open(HISTORY_FILE, 'r') as file:
            history_content = file.read()

        if not history_content:
            await ctx.reply("No history found.")
            return

        await ctx.reply(f"**Kick and Ban History:**\n```{history_content}```")
    except FileNotFoundError:
        await ctx.reply("No history found.")
    except Exception as e:
        await ctx.reply(f"An error occurred: {e}")

# Command to display bot info
@bot.command()
async def info(ctx):
    embed = discord.Embed(title="About me", description="`This Bot can kick, ban and view kick & ban history`", color=0x7289DA)
    embed.add_field(name="Creator", value="`OrangeMario`", inline=False)
    embed.add_field(name="Commands", value="`!kick (username) (reason)` `!ban (username) (reason)` `!history` `!info`", inline=False)
    await ctx.reply(embed=embed) 

bot.run(TOKEN)
keep_alive() 
