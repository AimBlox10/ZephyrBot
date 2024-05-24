import discord
from discord.ext import commands
import os
from flask import Flask
import threading

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

# Specify the role IDs that are not allowed to be kicked or banned
restricted_roles = [123456789012345678, 987654321098765432]  # Replace with actual role IDs

# Function to check if user has allowed roles
def has_allowed_role(ctx):
    return any(role.id in allowed_roles for role in ctx.author.roles)

# Function to log actions
def log_action(action, member, reason):
    with open(HISTORY_FILE, 'a') as f:
        f.write(f'{action}: {member} - {reason}\n')

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Event to confirm bot is ready and set custom status
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game(name="ZephyrBot | !info"))

# Command to kick a user
@bot.command()
@commands.check(has_allowed_role)
async def kick(ctx, member: discord.Member, *, reason='No reason provided'):
    if any(role.id in restricted_roles for role in member.roles):
        await ctx.reply("You cannot kick a member with the specified role.")
        return

    try:
        await member.kick(reason=reason)
        await ctx.reply(f'User {member} has been kicked for: {reason}')
        log_action('Kick', member, reason)
    except discord.Forbidden:
        await ctx.reply("I don't have permission to kick this member.")
    except discord.HTTPException as e:
        await ctx.reply(f'Kick failed: {e}')

# Command to ban a user
@bot.command()
@commands.check(has_allowed_role)
async def ban(ctx, member: discord.Member, *, reason='No reason provided'):
    if any(role.id in restricted_roles for role in member.roles):
        await ctx.reply("You cannot ban a member with the specified role.")
        return

    try:
        await member.ban(reason=reason)
        await ctx.reply(f'User {member} has been banned for: {reason}')
        log_action('Ban', member, reason)
    except discord.Forbidden:
        await ctx.reply("I don't have permission to ban this member.")
    except discord.HTTPException as e:
        await ctx.reply(f'Ban failed: {e}')

# Flask web server to keep the bot running
app = Flask('')

@app.route('/')
def home():
    return "The bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)))

# Function to run the Flask web server in a separate thread
def keep_alive():
    t = threading.Thread(target=run_flask)
    t.start()

# Run the Flask web server and the bot
keep_alive()
bot.run(TOKEN)
