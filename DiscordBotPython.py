import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

SOUND_ALIASES = {
    'dog': r'C:\Users\LENOVO\Music\Sounds\dogbark.wav',
    'car': r'C:\Users\LENOVO\Music\Sounds\carsounds.mp3',
    'surprise': r'C:\Users\LENOVO\Music\Sounds\frog.mp3',
}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

@bot.command(name='play', help='Sends the audio file directly into the text chat.')
@commands.has_permissions(administrator=True)
async def play(ctx, *, query: str):
    query = query.strip('"').strip("'")
    
    if query.lower() in SOUND_ALIASES:
        file_path = SOUND_ALIASES[query.lower()]
    else:
        file_path = query

    if not os.path.exists(file_path):
        await ctx.send(f'❌ File not found at path: `{file_path}`')
        return

    # Uploads and sends the audio file directly into the text channel
    await ctx.send(
        content=f'🎶 Audio requested by {ctx.author.mention}: **{os.path.basename(file_path)}**',
        file=discord.File(file_path)
    )

@play.error
async def play_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('❌ You do not have permission to use this command. Administrator rights are required.')

bot.run('Put your discord bot token here')
