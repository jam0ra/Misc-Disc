import discord
from dotenv import load_dotenv
load_dotenv()
import os
from random import choice
from discord.ext import commands, tasks
from itertools import cycle

# @TODO: Add exception handling.
# @TODO: Create cogs based on roles

# Sets command pre-fix ie: !ping
client = commands.Bot(command_prefix='!')
status = cycle(["for commands", "for instructions", "for pings"])

# Event
@client.event
# Runs once bot is ready
async def on_ready():
    change_status.start()
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=next(status)))
    print("Bot is ready!")

@client.event
async def on_member_join(member):
    print(f"Welcome, {member}.")

@client.event
async def on_member_remove(member):
    print(f"{member} has been removed.")

@client.event
async def on_command_error(context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        pass
    elif isinstance(error, commands.CommandNotFound):
        pass
    await context.send(error)

@tasks.loop(seconds=600)
async def change_status():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=next(status)))

@client.command()
async def ping(context):
    await context.send(f"Pong!")

@client.command()
async def latency(context):
    await context.send(f"Bot latency is {round(client.latency * 1000)} ms")

@client.command()
async def tree(context, type, size, symbol, whitespace=" "):
    size = int(size)
    output = ""
    if not (0 < size <= 21):
        await context.send("Size must > 0.") if size <= 0 else await context.send("Size must be < 22.")
        return
    if (type.lower() in ("left", "right-skewed")):
        spaces = size
        for i in range(size):
            output += (symbol * (i + 1) + (whitespace * spaces)) + "\n"
            spaces -= 1
    elif (type.lower() in ("right", "left-skewed")):
        spaces = size
        for i in range(size):
            output += ((whitespace * spaces) + (symbol * (i + 1))) + "\n"
            spaces -= 1
    elif (type.lower() in ("normal", "even")):
        spaces = size - 1
        for i in range(size):
            output += ((whitespace * spaces) + (symbol * (1 + i * 2)) + (whitespace * spaces)) + "\n"
            spaces -= 1

    await context.send(f"""```{output}```""")

@client.command(aliases=["8ball", "wisdom","eightball"])
async def _8ball(context, *, question):
    responses = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes – definitely', 'You may rely on it', 'As I see it, yes', 'Most likely', 'Outlook good', 'Yes Signs point to yes', 'Reply hazy', 'try again', 'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again', 'Dont count on it', 'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful']
    await context.send(f"Question: {question}\nAnswer: {choice(responses)}")

@client.command()
async def clear(context, amount):
    if amount > 0:
        await context.channel.purge(limit=amount)
    else:
        await context.send(f"Amount must be greater than zero. You said: {amount}")

@client.command(aliases=["remove"])
@commands.has_permissions(kick_members=True)
async def kick(context, member : discord.Member, *, reason=None):
    if not member:
        await context.send(f'{member} not found.')
        return
    await member.kick(reason = reason)
    await context.send(f'{member.display_name} was kicked from the server.')

@client.command(aliases=["banhammer", "begone"])
@commands.has_permissions(ban_members=True)
async def ban(context, member : discord.Member, *, reason=None):
    if not member:
        await context.send(f'{member} not found.')
        return
    await member.ban(reason=reason)
    await context.send(f'{member.display_name} was banned from the server.')

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(context, *, member):
    banned_users = await context.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await context.guild.unban(user)
            await context.send(f'{user.mention} was unbanned from the server.')
            break

@clear.error
async def clear_error(context, error):
    await context.send("Please specify the amount of messages to delete.")

######################## Cog Commands ############################

@client.command()
async def load(context, extension):
    client.load_extension(f"Cogs.{extension}")
    await context.send(f"{extension} was loaded.")

@client.command()
async def unload(context, extension):
    client.unload_extension(f"Cogs.{extension}")
    await context.send(f"{extension} was unloaded.")

@client.command(aliases=["update"])
async def reload(context, extension):
    client.unload_extension(f"Cogs.{extension}")
    await context.send(f"{extension} was unloaded.")
    client.load_extension(f"Cogs.{extension}")
    await context.send(f"{extension} was loaded.")

# loads cogs
for filename in os.listdir('./Cogs'):
    if filename.endswith(".py"):
        client.load_extension(f"Cogs.{filename[:-3]}")

# Runs client, token pulled from discord.com/developers
token = os.environ.get("token")
client.run(token)
