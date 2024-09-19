import requests
from bs4 import BeautifulSoup
import json
import re

# Fundamental BeautifulSoup scraper as in the video recording

# Error handeling ( try - except) for incorrect URL to check if there's an error from the beginning of the code
def scrape_the_data(url):
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Main function 1 - getting the team roaster from fbref website to be accessible for the user
def squad_details(url):

    import json

    soup = scrape_the_data(url)
    #Finding the tbody that contains the player data
    tbody = soup.find('tbody')
    # Checking if the tbody exists
    if tbody:
      # Extracting all rows <tr> within the tbody
      rows = tbody.find_all('tr')
    else:
      # If no tbody is found, try finding rows directly inside the table
      rows = soup2.find_all('tr')

    global team_dict

# creating a dictionary with sub-dictionaries for every position

    team_dict = {
      'Goalkeepers': {},
      'Defenders': {},
      'Midfielders': {},
      'Forwards': {}
      }

    for row in rows:
      # Extract player data by position

      if row:
        player_name = row.find('th', {'data-stat': 'player'}).get_text(strip=True)
        player_position = row.find('td', {'data-stat': 'position'}).get_text(strip=True)
        player_ID = row.find('th', {'data-append-csv': True})['data-append-csv']

        # Assigning players to their positions according to the website for clarity and organization
        # players are assigned to Goalkeepers/ Defenders/ Midfielders/ Forwards
        if 'GK' in player_position:
            team_dict['Goalkeepers'][player_ID] = {
                'Player_name': player_name,
                'Player_position': player_position
            }
        elif 'DF' in player_position:
            team_dict['Defenders'][player_ID] = {
                'Player_name': player_name,
                'Player_position': player_position
            }
        elif 'MF' in player_position:
            team_dict['Midfielders'][player_ID] = {
                'Player_name': player_name,
                'Player_position': player_position
            }
        elif 'FW' in player_position:
            team_dict['Forwards'][player_ID] = {
                'Player_name': player_name,
                'Player_position': player_position
            }

    # Print the final dict with all positions and all players

    for positions, players in team_dict.items():
        print(positions + ':')
        print(json.dumps(players, indent=4, ensure_ascii=False))
        print()

# Main function 2 - Printing player stats for the user

def player_stats(url):
    soup = scrape_the_data(url)

    # Find the div with id that starts with "div_scout_summary" table which contains the summary
    div = soup.find('div', id=lambda x: x and x.startswith('div_scout_summary'))

    # checking if div exists to get the stats
    if div:
      div_id = div.get('id')
      result = div_id.replace('div_', '')

    specific_table = soup.find('table', id= result)
    
    if specific_table:
      rows = specific_table.find_all('tr')

    for row in rows:
        #this for loop there is a <th> tag and it contains text
        stat_name_tag = row.find('th')
        stat_name = stat_name_tag.text.strip()

        # Find all <td> elements in the code
        td_tags = row.find_all('td')
        # ensure there are at least two
        if len(td_tags) >= 2:
            # Check if there's a div in the second <td> element
            div_tag = td_tags[1].find('div')
            if div_tag:
                percentile = div_tag.text.strip()
                print(f"Statistic: {stat_name}, Percentile: {percentile}")
            else:
                continue

# getting the ID from dictionary created
def get_player_id(dictionary, name):
    for position, players in dictionary.items():
        for player_id, info in players.items():
            if info.get("Player_name") == name:
                return player_id, info["Player_name"]
                # this returns none if there's no id match found
    return None, None


def main():
    print("Welcome to squad debriefer")
    URL = input("Please input the team URL:  ")

    # REGEX was used here
    pattern = r'/squads/\w+/([^/]+)'
    raw_name = re.search(pattern, URL)
    team_name = raw_name.group(1)
    team_name = team_name.replace('-Stats','')

    print(f"{team_name} squad details: ")
    squad_details(URL)

# Flags for errors and terminating the program

    flag = True
    

# while looop for starting the program when Flag is true

    while (flag):
        print("which player would you like to investigate?")
        name = input("Please copy and paste the name from dictionary:  ")

        #player_id, player_name = get_player_id(team_dict, name)
        #player_name_insert = player_name.replace(" ","-")

        name_flag = True
        
        while name_flag:
            player_id, player_name = get_player_id(team_dict, name)
            if player_name:
                player_name_insert = player_name.replace(" ", "-")
                name_flag = False
            else:
                print('Error detected. Please provide a proper name from the dictionary.')
                name = input("Please copy and paste the name from the dictionary: ")

        name_url = "https://fbref.com/en/players/"+player_id+"/"+player_name_insert
        print()
        player_stats(name_url)


# while loop for continuation of the program after getting the first summary stats

        while True:
            response = input("Continue? (Y/N): ")
            if response == "Y":
                break
            elif response == "N":
                flag = False
                break
            else:
                print("Please respond with Y or N")


main()

#we used GPT for starting point on Beautifulsoup functions (ex. request, .find, .findall) and certain complex operations (ex. ascii=false, Json dump, dictionary setting, regex)
#However, all code structure and functionalitties have been thought of and implemented by human activites