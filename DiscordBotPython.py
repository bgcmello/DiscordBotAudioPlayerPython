import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

SOUND_ALIASES = {
    'airhorn': 'C:/Users/YourName/Music/airhorn.mp3', # This can be any path that you make it be.
    'intro': 'C:/Users/YourName/Music/intro.wav', # It can support multiple file types
    'victory': 'C:/Users/YourName/Music/victory.ogg',
}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

@bot.command(name='play', help='Plays sound via variable or file path.')
@commands.has_permissions(administrator=True)
async def play(ctx, *, query: str):
    query = query.strip('"').strip("'")

    if query.lower() in SOUND_ALIASES:
        file_path = SOUND_ALIASES[query.lower()]
    else:
        file_path = query

    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send('❌ You must be connected to a voice channel to use this command!')
        return

    voice_channel = ctx.author.voice.channel

    if not os.path.exists(file_path):
        await ctx.send(f'❌ File not found at path: `{file_path}`')
        return

    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(voice_channel)
    else:
        try:
            await voice_channel.connect()
        except Exception as e:
            await ctx.send(f'❌ Failed to connect to voice channel: {e}')
            return

    voice_client = ctx.voice_client

    # Automatically stops the current track if another one is requested
    if voice_client.is_playing():
        voice_client.stop()

    def after_playing(error):
        if error:
            print(f'Player error encountered: {error}')

    try:
        audio_source = discord.FFmpegPCMAudio(file_path)
    except Exception as e:
        await ctx.send(f'❌ Error loading audio file. Ensure FFmpeg is installed! Error: {e}')
        return

    voice_client.play(audio_source, after=after_playing)
    await ctx.send(f'🎶 Now playing: **{os.path.basename(file_path)}**')

@play.error
async def play_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('❌ You do not have permission to use this command. Administrator rights are required.')

# Command to stop audio playback manually without leaving the voice channel
@bot.command(name='stop', help='Stops the current audio playback')
@commands.has_permissions(administrator=True)
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send('⏹️ Audio playback stopped.')
    else:
        await ctx.send('❌ No audio is currently playing.')

@stop.error
async def stop_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('❌ You do not have permission to use this command. Administrator rights are required.')

@bot.command(name='leave', help='Disconnects the bot from the voice channel')
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send('🔌 Disconnected from the voice channel.')
    else:
        await ctx.send('❌ I am not connected to any voice channel.')

bot.run('YOUR_BOT_TOKEN_HERE')
