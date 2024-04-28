import discord
from discord.ext import commands
import requests
import matplotlib.pyplot as plt
import config

# Initialize the Discord bot
intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)

# Last.fm API details
LASTFM_API_KEY = config.lastFMKey
LASTFM_API_URL = 'https://ws.audioscrobbler.com/2.0/'

# Function to fetch top tracks from Last.fm API
def get_top_tracks(username):
    print("entrando")
    params = {
        'method': 'user.gettoptracks',
        'user': username,
        'api_key': LASTFM_API_KEY,
        'format': 'json',
        'limit': 10  # Change this to get more tracks if needed
    }
    print("requesting response")
    response = requests.get(LASTFM_API_URL, params=params)
    data = response.json()
    print("generated response", data)
    return [track['name'] for track in data['toptracks']['track']]

# Function to generate a bar chart
def generate_chart(tracks):
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(tracks)), [1]*len(tracks))  # Just plotting bars, actual data can be added
    plt.xticks(range(len(tracks)), tracks, rotation=45)
    plt.xlabel('Tracks')
    plt.ylabel('Play Count')
    plt.title('Top Tracks')
    plt.tight_layout()
    plt.savefig('chart.png')  # Save the chart as a file
    plt.close()

# Command to generate chart
@bot.command()
async def toptracks(ctx, username):
    print(username)
    tracks = get_top_tracks(username)
    generate_chart(tracks)
    await ctx.send(file=discord.File('chart.png'))


# Run the bot
bot.run(config.botToken)
