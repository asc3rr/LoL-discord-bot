"""
### Class that handle champions for given positions
Gets list of champions that should play on given position

Usage:
>>> pos = Position("top")
>>> list_of_champions = pos.get_champions()
"""

from bs4 import BeautifulSoup
import requests

class Position:
    position_name = None
    champions = []
    url = "https://rankedboost.com/{}-tier-list/"

    def __init__(self, position_name:str):
        """
        ## Position

         - position_name - Name of position that we want champions for
        """
        self.position_name = position_name

        if position_name == "top" or position_name == "mid":
            position_name += "-lane"

        self.url = self.url.format(position_name)

    def _make_request(self):
        site_content = requests.get(self.url).content
        soup = BeautifulSoup(site_content, "html.parser")

        unprocessed_data = soup.find_all("span", class_="champion_name-tl")

        processed_data = []

        for data in unprocessed_data:
            data_to_append = str(data).split(">")[1]

            data_to_append = data_to_append.split("<")[0]

            processed_data.append(data_to_append)

        return processed_data

    def get_champions(self):
        """
        ### Returns discord formated string of champions
        """

        champions = self._make_request()

        output_string = f"""
=== **Postacie do grania na {self.position_name}** ===
```
"""

        for champion in champions:
            output_string += champion + "\n"

        output_string += "```"

        return output_string