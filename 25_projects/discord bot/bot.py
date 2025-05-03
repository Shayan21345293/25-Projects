import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guild_messages = True

bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')


@bot.command()
async def hello(ctx):
    await ctx.send("Hello, I am alive! 🤖")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! 🏓 Latency: {round(bot.latency * 1000)}ms")

@bot.command()
async def echo(ctx, *, message):
    await ctx.send(message)

@bot.command()
async def help_me(ctx):
    help_text = """
🤖 **Available Commands**

Fun:
`/joke` - Get a random joke
`/coin` - Flip a coin
`/roll [number]` - Roll a dice

Utility:
`/serverinfo` - Get server information
`/userinfo [member]` - Get user information
`/avatar [member]` - Get user's avatar
`/ping` - Check bot latency
`/echo [message]` - Repeat your message

Moderation:
`/kick [member] [reason]` - Kick a member
`/ban [member] [reason]` - Ban a member
`/clear [amount]` - Clear messages

Chat:
`/chat [message]` - Chat with the bot
`/hello` - Get a greeting
"""
    await ctx.send(help_text)

# Fun Commands
@bot.command()
async def joke(ctx):
    """Tell a random joke"""
    jokes = [
        "Why don't programmers like nature? It has too many bugs!",
        "What do you call a bear with no teeth? A gummy bear!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "What do you call a fake noodle? An impasta!"
    ]
    await ctx.send(random.choice(jokes))

@bot.command()
async def coin(ctx):
    """Flip a coin"""
    result = random.choice(['Heads', 'Tails'])
    await ctx.send(f"🪙 The coin landed on: **{result}**!")

@bot.command()
async def roll(ctx, number: int = 6):
    """Roll a dice (default is 6-sided)"""
    result = random.randint(1, number)
    await ctx.send(f"🎲 You rolled a **{result}**!")

# Utility Commands
@bot.command()
async def serverinfo(ctx):
    """Get information about the server"""
    server = ctx.guild
    await ctx.send(f"""
📊 **Server Information**
Name: {server.name}
Members: {server.member_count}
Created: {server.created_at.strftime('%B %d, %Y')}
Owner: {server.owner}
""")

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    """Get information about a user"""
    member = member or ctx.author
    await ctx.send(f"""
👤 **User Information**
Name: {member.name}
Joined: {member.joined_at.strftime('%B %d, %Y')}
Role: {member.top_role}
Status: {member.status}
""")

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    """Get user's avatar"""
    member = member or ctx.author
    await ctx.send(member.avatar.url)

# Moderation Commands
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    """Kick a member"""
    await member.kick(reason=reason)
    await ctx.send(f"Kicked {member.name} for reason: {reason}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    """Ban a member"""
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.name} for reason: {reason}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    """Clear specified number of messages"""
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"Cleared {amount} messages!", delete_after=5)

# Chat Command
@bot.command()
async def chat(ctx, *, message):
    """Chat with the bot"""
    responses = {
        "how are you": "I'm doing great! How about you?",
        "what's up": "Just hanging out in the server, ready to chat!",
        "hello": "Hey there! Nice to chat with you!",
        "bye": "Goodbye! Talk to you later!",
        "good morning": "Good morning! Hope you have a great day!",
        "good night": "Good night! Sweet dreams!",
        "tell me a joke": "Why don't programmers like nature? It has too many bugs! 😄",
        "favorite color": "I love all colors of the rainbow! 🌈",
        "thank you": "You're welcome! Always happy to help! 😊",
        "who are you": "I'm a friendly Discord bot here to help and chat! 🤖",
    }
    
    message = message.lower()
    for key in responses:
        if key in message:
            await ctx.send(responses[key])
            return
    
    await ctx.send("I'm not sure how to respond to that. Try asking me how I am!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content.lower()
    
    if bot.user.mentioned_in(message):
        await message.channel.send("Hey! You can chat with me using the `/chat` command!")
    
    await bot.process_commands(message)

bot.run(TOKEN)