import requests
import re
import asyncio

class TextService:

    def __init__(self, language):
        self.baseUrl = 'https://newsapi.org/v2/everything?'
        self.apiKey = 'eb65b1a71b3b40908f3ded58ba908255'
        self.language = language
        self.json = None
        self.index = 0

    async def getJsonByKeyword(self, keyword):

        payload = { 'q':keyword, 'language': self.language, 'apiKey': self.apiKey}

        data = requests.get(self.baseUrl, params=payload)
        
        self.json = data.json()

    def getUrlNext(self):
        
        if self.json:  
            if self.index > len(self.json["articles"])-1 :
                self.index = 0
            
            url = self.json["articles"][self.index]["url"]
            self.index += 1
            return url
           
        else:
            print("The json is empty.")
