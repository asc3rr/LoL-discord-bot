"""
### Class that handle getting stats from op.gg
Gets stats of given player
"""

from bs4 import BeautifulSoup
import riotwatcher as rw
import requests
import json

class Player:
    ## Basic data
    account_id = None
    player_id = None
    puuid = None

    username = None
    lvl = None

    ## Ranked data {
    ### Ranked flex
    number_of_flex_games = None
    flex_wins = None
    flex_loses = None
    flex_tier = None
    flex_rank = None
    flex_lp = None
    flex_win_percentage = None # Win/Lose ratio


    ### Ranked solo
    number_of_games = None
    wins = None
    loses = None
    tier = None
    rank = None
    lp = None
    win_percentage = None # Win/Lose ratio

    ## }

    ## API data
    server = None
    api_key = None
    region = None

    ## Riotwatcher objects
    watcher = None

    def __init__(self, username:str, api_key:str, server:str, region:str):
        """
        ### Stats

         - player_name - Name of player that we want to get stats of.
         - server - Server which player plays(e.g. eune)
         - api-key
         - region - Americas / Europe / Asia / Sea
        """
        self.username = username
        self.server = server.lower()
        self.api_key = api_key
        self.region = region.lower()

        self.watcher = rw.LolWatcher(self.api_key)

    def _get_basic_data(self):
        basic_data = self.watcher.summoner.by_name(self.server, self.username)

        self.player_id = basic_data["id"]
        self.puuid = basic_data["puuid"]
        self.lvl = basic_data["summonerLevel"]

    def _get_ranked_data(self):
        if not self.player_id:
            raise RuntimeError("You have to get basic data first")

        ranked_data = self.watcher.league.by_summoner(self.server, self.player_id)

        if ranked_data == []:
            self.rank, self.tier, self.lp, self.wins, self.loses = "Brak danych", "Brak danych", "Brak danych", "Brak danych", "Brak danych"
            return

        ## Getting flex data
        flex_data = ranked_data[0]
        self.flex_tier = flex_data["tier"]
        self.flex_rank = flex_data["rank"]
        self.flex_wins = flex_data["wins"]
        self.flex_loses = flex_data["losses"]
        self.flex_lp = flex_data["leaguePoints"]

        ### Calculating wl_ratio
        self.number_of_flex_games = self.flex_wins + self.flex_loses

        self.flex_win_percentage = int((self.flex_wins * 100) / self.number_of_flex_games)

        ## Getting solo data
        solo_data = ranked_data[1]
        self.tier = solo_data["tier"]
        self.rank = solo_data["rank"]
        self.wins = solo_data["wins"]
        self.loses = solo_data["losses"]
        self.lp = solo_data["leaguePoints"]

        ### Calculating wl_ratio
        self.number_of_games = self.wins + self.loses

        self.win_percentage = int((self.wins * 100) / self.number_of_games)

    def get_stats(self):
        self._get_basic_data()
        self._get_ranked_data()

        output = f"""
**Statystyki gracza {self.username}**
**_Poziom konta: {self.lvl}_**

**Statystyki rankingowe**
_SOLO_
> Ilość meczy: {self.number_of_games}
> Ilość wygranych meczy: {self.wins}
> Ilość przegranych meczy: {self.loses}
> Procent wygranych: {self.win_percentage}%
> Tier: {self.tier}
> Ranga: {self.rank}
> LP: {self.lp}

_FLEX_
> Ilość meczy: {self.number_of_flex_games}
> Ilość wygranych meczy: {self.flex_wins}
> Ilość przegranych meczy: {self.flex_loses}
> Procent wygranych: {self.flex_win_percentage}%
> Tier: {self.flex_tier}
> Ranga: {self.flex_rank}
> LP: {self.flex_lp}
"""
        return output