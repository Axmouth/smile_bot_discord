import json
import requests
import urllib.parse

RIOT_KEY = 'RGAPI-89b7150b-a43e-4c4b-a023-65e431cb3283'
API_VER = "v3"
SERVERS = ["EUW1", "KR", "NA1", "EUN1", "BR", "TR1", "LA1", "LA2", "JP1", "OC1", "RU", ]


def request_summoner_data_by_name(region, summoner_name, APIKey):
    # Here is how I make my URL.  There are many ways to create these.
    summoner_name = urllib.parse.quote(summoner_name)
    URL = "https://<region>.api.riotgames.com/lol/summoner" \
          "/<api>/summoners/by-name/<summonername>?api_key=<key>"\
        .replace("<region>", region).replace("<summonername>", summoner_name).replace("<key>", APIKey)\
        .replace("<api>", API_VER)
    print(URL)
    # requests.get is a function given to us my our import "requests".
    # It basically goes to the URL we made and gives us back a JSON.
    response = requests.get(URL)
    # Here I return the JSON we just got.
    return response.json()


def request_ranked_data(region, ID, APIKey):
    URL = "https://<region>.api.riotgames.com/lol/summoner" \
          "/<api>/summoners/by-name/<summonername>?api_key=<key>"\
        .replace("<region>", region).replace("<summonername>", summoner_name).replace("<key>", APIKey)\
        .replace("<api>", API_VER)
    print(URL)
    # requests.get is a function given to us my our import "requests".
    # It basically goes to the URL we made and gives us back a JSON.
    response = requests.get(URL)
    # Here I return the JSON we just got.
    return response.json()


if __name__ == "__main__":
    print('test')
    resp = requests.get('https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/RiotSchmick?api_key=<key>'
                        .replace('<key>',RIOT_KEY))
    print(resp.json())
    print(request_summoner_data_by_name('EUW1', 'QuietHeroine', RIOT_KEY))
    print(request_summoner_data_by_name('EUW1', 'Zero Deaths', RIOT_KEY))