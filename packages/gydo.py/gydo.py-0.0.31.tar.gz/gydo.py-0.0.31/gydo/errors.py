class Error(Exception):
    pass

class DiscordAPIError(Error):
    """
        If there is a Discord API Error this will be raised
    """
    def __init__(self, status, message):
        self.status = status
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return f'{self.status}: {self.message}'

class WebsocketError(Error):
    """
        Websocket Error handling
    """
    def __init__(self, status, message):
        self.status = status
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return f'{self.status}: {self.message}'