
import requests
from sol_types import Team, Champion, Player
from bs4 import BeautifulSoup

class ScrapesofLegends:
    # helper method to scrape GoL, returns BeautifulSoup html object
    def gol_scrape(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        # use the requests package to read the page to a response
        response = requests.get(url, headers=headers)

        if response.status_code != 200: # if abnormal response, raise error
            raise Exception('Status Code:' + response.status_code + '\nStatus Code Description:' + response.reason)
        
        return BeautifulSoup(response.content, 'html.parser') 

    # helper method to get text of table headers, returns list of headers
    def get_headers(self, soup):
        heads = soup.find_all('th')                 # find table headers in BeautifulSoup obj
        headers = []
        for h in heads:
            headers.append(h.get_text(strip=True))  # add header text to return list
        return headers

    # helper method to get text of table rows, returns nested list of table cell values
    def get_table(self, soup, headers):
        rows = soup.find_all('tr')                  # find table rows
        table_data = []
        for i in range (len(rows)):                 # for each row
            if rows[i].td:                          # if row has <td> items
                if rows[i].td.find('a'):            # if first <td> item has <a> item (not necessarily meaningful, but restricts return to relevant rows for this purpose)
                    data = rows[i].find_all('td')   # get data from row
                    table_data.append([])           # add empty list to hold row data
                    url = data[0].a.get('href') # get url linking to table row data
                    for s in url.split('/'):        # split url by '/' character
                        if s.isnumeric():           # get id from url
                            id = s
                            break
                    table_data[len(table_data)-1].append(id) 
                    for j in range(len(headers)):
                        table_data[len(table_data)-1].append(data[j].get_text(strip=True)) # add row data to list item
        return table_data

    # helper method to get tournament options from GamesofLegends
    def get_tournaments(self, soup):
        print("Fetching tournaments...")
        t_list = []
        tourn = soup.find('select', id="cbtournament")  # get HTML of tournament list dropdown box from BeautifulSoup object
        opts = tourn.find_all('option')                 # get list of options
        for o in opts:
            t_list.append(o.get_text())                 # append option text to list of tournaments
        return t_list

    # method to get GamesofLegends data, returns list of data
    def scrape(self, type, season=14, split='Summer', tournament = 'ALL'):
        print("Fetching " + type + '...')
        data_list = []
        # input validation
        if type not in ['teams', 'players', 'champion']:                # validate data type parameter
            raise Exception("Invalid data type; must be teams, players, champion")
        if season not in range(6,15):                                   # validate season parameter
            raise Exception("Invalid split parameter; must be integer between 6 and 14")
        if split not in [ 'Spring', 'Pre-Season', 'Summer']:   # validate split parameter
            raise Exception("Invalid season parameter; must be Spring, Pre-Season, or Summer")
        url = 'https://gol.gg/' + type + '/list/' + 'season-S' + str(season) + '/split-' + split + '/tournament-ALL/'
        soup = self.gol_scrape(url)  # get page HTML
        if tournament != 'ALL':
            if tournament not in self.get_tournaments(soup): # validate tournament parameter
                raise Exception("Invalid tournament parameter; must be in " + str(self.get_tournaments(soup)))
            url = 'https://gol.gg/' + type + '/list/' + 'season-S' + str(season) + '/split-' + split + '/tournament-' + tournament + '/'
        
        # get data
        soup = self.gol_scrape(url)                  # BeautifulSoup object of html of desired page
        headers= self.get_headers(soup)              # headers of desired data table
        rows = self.get_table(soup, headers)         # rows of desired table
        if (type == 'teams'):
            for i in range(len(rows)):
                n = Team(headers, rows[i])      # create Team obj with data from ith row
                data_list.append(n)                 # add obj to list
        elif(type == 'players'):
            for i in range(len(rows)):
                n = Player(headers, rows[i])    # create Player obj with data from ith row
                data_list.append(n)                 # add obj to list
        elif(type == 'champion'):
            for i in range(len(rows)):
                n = Champion(headers, rows[i])  # create Champion obj with data from ith row
                data_list.append(n)                 # add obj to list    
        return data_list

    # method to sort 'list' by value of 'key', order controlled with 'rev' parameter
    def sort(self, list, key, rev = False):
        if key not in list[0].get_keys():
            raise Exception("invalid key parameter; must be in " + str(list[0].get_keys()))
        return sorted(list, key=lambda item: item.get_value(key), reverse=rev)

    # method to get max n items by key value
    def max(self, list, key, n = 1):
        return self.sort(list, key, rev = True)[:n]

    # method to get min n items by key value
    def min(self, list, key, n = 1):
        return self.sort(list, key)[:n]

    # method to filter data by key value
    def filter(self, list, key, value):
        ret = []
        if key not in list[0].get_keys():
            raise Exception("invalid key parameter; must be in " + str(list[0].get_keys()))
        for item in list:
            if item.get_value(key) == value:
                ret.append(item)
        return ret

if __name__=="__main__":
    s = ScrapesofLegends()
    players = s.scrape('players', season=13, split='Summer', tournament='LEC Summer 2023')
    for p in players:
        print(p)
    