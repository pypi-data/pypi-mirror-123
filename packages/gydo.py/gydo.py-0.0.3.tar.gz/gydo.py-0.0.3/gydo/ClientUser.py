import asyncio
import pymitter
import json

class ClientUser:
    def __init__(self, data):
        x = json.dumps(data.json())
        usr_data = json.loads(x)['d']
        
        self.id = usr_data['user']['id']
        
        self.discriminator = usr_data['user']['discriminator']
        
        self.username = usr_data['user']['username']

        self.tag = f'{self.username}#{self.discriminator}'