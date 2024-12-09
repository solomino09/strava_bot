import aiohttp
import asyncio
import discord
import logging
import server
import urllib.parse
from discord import ButtonStyle
from discord.ext import commands
from discord.ui import Button, View
from config import (
    BASE_URL,
    BOT_TOKEN,
    CLIENT_ID,
    LOGIN_URL,
    CLIENT_SECRET,
    REDIRECT_URI,
    ACCESS_TOKEN_ENDPOINT
)

from authlib.integrations.httpx_client import AsyncOAuth2Client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s, %(levelname)s: %(name)s:%(lineno)d - %(message)s",
)
logger = logging.getLogger(__name__)

client_intents = discord.Intents.default()
client_intents.message_content = True
client = commands.Bot(command_prefix=".", intents=client_intents)
access_token = None
user_tokens = {}


@client.event
async def on_ready() -> None:
    logger.info(f"Logged in as a bot {client.user.name}")


@client.command()
async def ping(ctx) -> None:
    """check whether bot is active or not
    ping -> pong!!!"""
    await ctx.send("Pong!")


@client.command(name="login")
async def login_with(ctx) -> None:
    """starts login with process"""
    await ctx.send("Login with OAuth")
    client = AsyncOAuth2Client(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
    )
    uri, state = client.create_authorization_url (LOGIN_URL, state="test")
    decoded_uri = urllib.parse.unquote(uri)

    button = Button(label="🔑 Login with OAuth", url=decoded_uri)
    view = View()
    view.add_item(button)
    await ctx.send("Click the button below to log in with OAuth:", view=view)

    # define callback function to handle code parameter
    async def handle_authorization_response(authorization_response):
        parsed_response = urllib.parse.urlparse(authorization_response)
        query_params = urllib.parse.parse_qs(parsed_response.query)
        code = query_params.get("code", [''])[0]
        if not code:
            print("No authorization code found")
            return

        url = f"{BASE_URL}oauth/token"
        params = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': code
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=params, headers=headers) as response:
                if response.status == 200:
                    response_data = await response.json()
                    token = response_data.get('access_token')
                    user_tokens[ctx.author.id] = token
                    firstname = response_data['athlete'].get('firstname', 'Unknown')
                    lastname = response_data['athlete'].get('lastname', 'Unknown')
                    city = response_data['athlete'].get('city', 'Unknown')
                    country = response_data['athlete'].get('country', 'Unknown')
                    message = f"{lastname} {firstname} from {city}, {country} authorized successfully!"
                    activities_button = Button(label="📋 Get Activities", style=ButtonStyle.primary)

                    async def activities_callback(interaction):
                        await interaction.response.defer()
                        await ctx.invoke(get_activities)

                    activities_button.callback = activities_callback
                    a_view = View()
                    a_view.add_item(activities_button)
                    await ctx.send(message, view=a_view)
                else:
                    print(f"Error: {response.status}")
                    print(await response.text())

    # start http server
    server.start(handle_authorization_response)


@client.command(name="activities")
async def get_activities(ctx) -> None:
    """Fetches and displays the user's activities from Strava"""
    token = user_tokens.get(ctx.author.id)
    if not token:
        await ctx.send("Access token not found. Please login first.")
        return

    url = f"{BASE_URL}athlete/activities"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                activities = await response.json()

                if not activities:
                    await ctx.send("No activities found.")
                    return

                messages = []
                for activity in activities:
                    start_date = activity.get('start_date', 'N/A')
                    activity_type = activity.get('type', 'N/A')
                    distance = activity.get('distance', 'N/A')
                    el_gain = activity.get("elevation_gain", "N/A")
                    av_speed = activity.get("average_speed", "N/A")
                    moving_time = activity.get('moving_time', 'N/A')
                    name = activity.get('name', 'N/A')

                    message = f"{start_date} - {activity_type} - {distance}m - {moving_time}s - " \
                              f"elevation gain: {el_gain} m - av.speed: {av_speed} m/s - {name}"
                    messages.append(message)

                for msg in messages[:5]:  # Sending the first 5 activities (can be increased or changed)
                    await ctx.send(msg)
            else:
                await ctx.send(f"Failed to fetch activities. Status code: {response.status}")
                error_message = await response.text()
                print(f"Error: {error_message}")


client.run(BOT_TOKEN)
