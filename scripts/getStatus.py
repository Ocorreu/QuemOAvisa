import requests
from facepy import GraphAPI
import json
import io
from regexParser import regexParser, filepath

r = requests.get('https://graph.facebook.com/oauth/access_token?grant_type=client_credentials&client_id=1708163546094790&client_secret=f8fc99141be1411af3dd043343a11123')
access_token = r.text.split('=')[1]

print('Access token aquired!')

graph = GraphAPI(access_token)

print('GraphAPI')

albums = graph.get('118723868183136/photos') #This is the timeline album for PSP

found = False

while(not found):
    try:
        for element in albums["data"]:
            if "name" in element:
                if "QUEM O AVISA" in element["name"]:
                    found = True
                    f = io.open(filepath, 'w', encoding='utf-8')
                    f.write(element["name"])
                    f.write("\n")
                    f = io.open(filepath,'a')
                    f.write("THE END")
                    f.close()
        albums = requests.get(albums['paging']['next']).json()
    except KeyError:
        break

regexParser()


print('Done!')
