from bs4 import BeautifulSoup
import requests
import json

def get_rotation(region:str, api_key:str):
    #changing server names to region names

    region = region.lower()

    if region == "eune":
        region = "eun1"

    elif region == "euw":
        region = "euw1"

    elif region == "br":
        region = "br1"

    elif region == "lan":
        region = "la1"

    elif region == "las":
        region = "la2"

    elif region == "na":
        region = "na1"
    
    elif region == "oce":
        region = "oce1"

    elif region == "ru":
        region = "ru1"

    elif region == "tr":
        region = "tr1"

    elif region == "jp":
        region = "jp1"

    ## Getting rotation
    rotation_champs_ids = []
    rotation_champs_names = []

    url = f"https://{region}.api.riotgames.com/lol/platform/v3/champion-rotations?api_key={api_key}"

    resp = requests.get(url)

    json_data = resp.json()

    try:
        rotation_champs_ids = json_data["freeChampionIds"]

    except:
        return None

    for champ_id in rotation_champs_ids:
        rotation_champs_names.append(get_champion_name(champ_id))

    return "\n".join(rotation_champs_names)

def get_champion_name(champ_id:int):
    url = "https://ddragon.leagueoflegends.com/cdn/10.24.1/data/en_US/champion.json"

    resp = requests.get(url)

    json_data = json.loads(resp.content)

    for champ in json_data["data"]:
        if json_data["data"][champ]["key"] == str(champ_id):
            return json_data["data"][champ]["id"]