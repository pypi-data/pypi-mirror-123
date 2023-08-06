import requests

class RESTManager:
    def __init__(self, rest, endpoint):
        self.token = rest;
        
        self.headers = {
            'Authorization': f'Bot {rest}',
            'Content-Type': 'application/json'
        }
        
    def RESTGetCurrentUser(self, rest, endpoint):
        
        r = requests.get(f'{endpoint}/users/@me', headers=self.headers)
        
        return r
        
    def RESTPostMessage(self, rest, endpoint, channelId, json):
        
        self.MESSAGE_JSON = json
        
        r = requests.post(f'{endpoint}/channels/{channelId}/messages', headers=self.headers, json=self.MESSAGE_JSON)
        
        return r
        
    def RESTPost(self, endpoint, headers, json):
        
        self.postHeaders = headers
        self.postJSON = json
        
        post = requests.post(f'{endpoint}', headers=self.postHeaders, json=self.postJSON)
        
        return post 
        
    def RESTGet(self, endpoint, headers):
        self.getHeaders = headers
        
        get = requests.get(endpoint, headers=self.getHeaders)
        
        return get