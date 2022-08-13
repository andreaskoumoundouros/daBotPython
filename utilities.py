import json
from urllib import parse, request
import random

def get_gif_url(query):
        url = "http://api.giphy.com/v1/gifs/search"

        if len(query) > 25:
            query = query[:20]

        params = parse.urlencode ({
            "q": str(query),
            "api_key": "Dub2GdVra05BjQdXByxJ0dhuTryqNn54",
            "limit": "10",
            "rating": "r"
        })

        with request.urlopen("".join((url, "?", params))) as response:
            data = json.loads(response.read())

        urls = []
        for item in data["data"]:
            url = str(item["images"]["original"]["url"])
            urls.append(url)

        if len(urls) > 0:
            return random.choice([x for x in urls])
        else:
            return "Uwu, s-s-senpai I sowwy, I failed to send a gify wiphy.... :("