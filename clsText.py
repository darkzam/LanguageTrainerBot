
from newspaper import *

class Text:

    def __init__(self, url):
        self.url = url
        self.text = ""
        self.paragraphs = []

    async def loadArticle(self):
        article = Article(self.url)
        article.download()
        article.parse()
        self.text = article.text
        self.paragraphs = article.text.split('\n')

    def getParagraph(self, size):
        
        for paragraph in self.paragraphs:
            if len(paragraph) >= size:
                return paragraph
        return ''