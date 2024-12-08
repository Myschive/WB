import discord
from discord.ext import tasks, commands
import random
import asyncio
from time import sleep
import math
import random
# Your bot token and target settings
TOKEN = "tok"
GUILD_ID = 1248746492475473970  # Replace with your guild ID
VOICE_CHANNEL_ID = 1262063525220847688  # Replace with the target voice channel ID
SOUND_FILE = "file/path"  # Path to your sound file

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    # Start the sound-playing loop in the background
    bot.loop.create_task(sound_loop())
ttt = random.randint(500,2500)
async def sound_loop():
    """A loop that plays a sound in the VC every hour when users are present."""
    while True:
        hh = 0

        print(ttt)
        hh += 1
        await asyncio.sleep(ttt)  # Wait for an hour

        guild = bot.get_guild(GUILD_ID)
        if guild is None:
            print(f"Guild with ID {GUILD_ID} not found. Ensure the bot is in the server.")
            continue  # Skip the rest of the loop

        channel = guild.get_channel(VOICE_CHANNEL_ID)
        if channel is None or not isinstance(channel, discord.VoiceChannel):
            print(f"Voice channel with ID {VOICE_CHANNEL_ID} not found.")
            continue

        # Check if there's at least one non-bot member in the voice channel
        members_in_vc = [member for member in channel.members if not member.bot]
        if not members_in_vc:
            print("No users in the voice channel.")
            continue
        l = 0
        vc = None  # Initialize to ensure it exists in the `finally` block
        for memeber in members_in_vc:
            l += 1
            if l >= 1:
                print(l)
                try:
                    # Join the voice channel
                    vc = await channel.connect()
                    # Wait for a random delay (1–10 seconds)
                    delay = random.randint(1, 10)
                    await asyncio.sleep(delay)
                    # Play the sound file
                    await asyncio.sleep(random.randint(1,25))
                    vc.play(discord.FFmpegPCMAudio(SOUND_FILE), after=lambda e: print("Playback done."))
                    while vc.is_playing():
                        await asyncio.sleep(1)  # Wait until playback finishes
                except Exception as e:
                    print(f"Error during playback: {e}")
                finally:
                    # Ensure the bot disconnects after playing
                    if vc:
                        await vc.disconnect()


# Run the bot
bot.run(TOKEN)