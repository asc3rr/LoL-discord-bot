"""
### Class that handle getting champion builds
Gets runes, bulids and sumonner spells for given champion

Usage:
>>> champion = Champion("jax")
>>> full_build = champion.get_build()
"""

## TODO getting skills order

from bs4 import BeautifulSoup
import requests

class Champion:
    champion_name = None

    runes = None
    spells = None
    items = None

    def __init__(self, champion_name:str):
        """
        ## Champion

         - champion_name - champion name that we want to get build for.
        """
        self.champion_name = champion_name

    #Working
    def _get_runes(self):
        url = "https://u.gg/lol/champions/{}/build/".format(self.champion_name)

        site_content = requests.get(url).content
        soup = BeautifulSoup(site_content, "html.parser")

        #Processing titles
        titles = []
        unprocessed_titles = soup.find_all("div", class_="perk-style-title")[2:]

        for title in unprocessed_titles:
            data = str(title).replace('<div class="perk-style-title">', "")
            data = data.replace("</div>", "")

            titles.append(data)

        #Processing runes
        runes = []
        unprocessed_runes = soup.find_all("div", class_="perk-active")

        for i in unprocessed_runes:
            data = str(i).split('alt="')
            data = data[1].split('"')

            runes.append(data[0].replace("The Rune ", ""))

        return titles, runes[6:]

    def _get_skill_order(self):
        url = "https://u.gg/lol/champions/{}/build/".format(self.champion_name)
        
        site_content = requests.get(url).content
        soup = BeautifulSoup(site_content, "html.parser")

        unprocessed_order = soup.find_all("div", class_="skill-label bottom-center")[5:] ## skill-priority-path
        processed_order = []
        
        for data_piece in unprocessed_order:
            data = str(data_piece).replace('<div class="skill-label bottom-center">', "").replace("</div>", "")

            processed_order.append(data)

        return processed_order

    #Working
    def _get_spells(self):
        url = "https://www.leaguespy.gg/league-of-legends/champion/{}/stats".format(self.champion_name)

        site_content = requests.get(url).content
        soup = BeautifulSoup(site_content, "html.parser")

        unprocessed_spells = soup.find_all("div", class_="spell-block__content")

        spells = []

        for spell in unprocessed_spells:
            semi_processed_spell = str(spell).split("<h4>")[1]
            processed_spell = semi_processed_spell.split("</h4>")[0]

            spells.append(processed_spell)


        return spells[:2]

    #Working
    def _get_items(self):
        url = "https://www.leaguespy.gg/league-of-legends/champion/{}/stats".format(self.champion_name)

        site_content = requests.get(url).content
        soup = BeautifulSoup(site_content, "html.parser")

        unprocessed_items = soup.find_all("div", class_="item-block__top")

        processed_items = []

        for item in unprocessed_items:
            data = str(item).split('alt="')
            data = data[1].split('"')

            processed_items.append(data[0])

        return processed_items

    #Working
    def get_build(self):
        """
        ### Returns discord formatted string of runes, build and sumonner spells
        """

        titles, runes = self._get_runes()
        items = self._get_items()
        spells = self._get_spells()
        skill_order = self._get_skill_order()

        primary_runes_str = ", ".join(runes[:4])
        secondary_runes_str = ", ".join(runes[4:])
        items_str = ", ".join(items)
        spells_str = ", ".join(spells)
        skill_order_str = f"**`{skill_order[0]}`** => **`{skill_order[1]}`** => **`{skill_order[2]}`**"

        answer = f"""
**Champion:** {self.champion_name.capitalize()}
Build:
> **Runy**: 
>   {titles[0]} => {primary_runes_str}
>   {titles[1]} => {secondary_runes_str}
> **Itemki**: 
>   {items_str}
> **Spelle**: 
>   {spells_str}

Kolejność skilli:
> {skill_order_str}"""

        return answer

if __name__ == "__main__":
    champion = Champion("jax")
    print(champion.get_build())