from restapi import RESTManager
from WebsocketManager import WebsocketManager
import json
from ClientUser import ClientUser
import asyncio
import aiohttp
import nest_asyncio
nest_asyncio.apply()
from pymitter import EventEmitter

APIEndpoint = 'https://discord.com/api/v9'


class Client:
    """
        Main Client for Discord Bots
    """
    def __init__(self, token):
        self.endpoint = APIEndpoint
        self.token = token
        self.ws = WebsocketManager(self)
        self.manage = RESTManager(self.token, APIEndpoint)
        self.events = EventEmitter()
        
        asyncio.run(self.create_session())
    
    """
        Send a message through Discord's REST API
    """
    async def sendMessage(self, message, channelId, *embed):
        self.messageJSON = {
            'content': f'{message}',
            'embeds': []
        }

        r = self.manage.RESTPostMessage(self.token, APIEndpoint, channelId, self.messageJSON)
        
        return r

    async def MessageEmbed(self, title, description):
        self.MessageEmbedJSON = {
            'title': title,
            'description': description
        }

        return self.MessageEmbedJSON
        
    """
        Create a WebSocket Session
    """
    async def create_session(self):
        loop = asyncio.get_event_loop()
        
        self.session = aiohttp.ClientSession()

        self.connection = await self.session.ws_connect('wss://gateway.discord.gg/?v=9&encoding=json')
        
        tasks = [
            asyncio.ensure_future(self.ws.heartbeat()),
        ]
        
        self.user = ClientUser(await self.ws.connect(self.connection))
        
        try:
            loop.run_until_complete(asyncio.wait(tasks))
            loop.run_forever()
        except KeyboardInterrupt:
            await self.ws.connection.close()