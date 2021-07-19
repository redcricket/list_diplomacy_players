import requests
import getpass
from bs4 import BeautifulSoup

# https://curl.trillworks.com/
# https://www.banjocode.com/post/python/scrape-authenticated/
players_url = 'https://www.playdiplomacy.com/stats.php?sub_page=1'


def do_login():
    headers = {
        'authority': 'www.playdiplomacy.com',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '^\\^',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'origin': 'https://www.playdiplomacy.com',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.playdiplomacy.com/index.php',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'PHPSESSID=aafcoiv82ps8du80f8p0bmue15; __utma=79580501.1672733399.1625371128.1625371128.1625371128'
                  '.1; __utmc=79580501; __utmz=79580501.1625371128.1.1.utmcsr=(direct)^|utmccn=(direct)^|utmcmd=('
                  'none); __utmt=1; __utmb=79580501.1.10.1625371128',
    }

    username = input('Enter your user name: ')
    password = getpass.getpass(f"Enter {username}'s password:")
    data = {
        'page_act': '',
        'username': username,
        'password': password,
        'remember_me': '1'
    }

    s = requests.session()
    response = s.post('https://www.playdiplomacy.com/login.php', headers=headers, data=data)
    if response.status_code != 200:
        print('Authentication failed.')
        return
    response = s.get(url=players_url)
    soup = BeautifulSoup(response.text, features="html.parser")
    next_link = soup.find('a', text='next')
    current_page = 1
    while next_link:
        # 35 is the last page of actual players.  This could change in the future.
        if current_page > 35:
            print(f'current_page is {current_page}. return')
            return
        current_page += 1
        players = False
        for i, player_il in enumerate(soup.find_all('li')):
            try:
                player_info = player_il.text.strip()
                # 17 is where MisterBimmler (my username) shows up.
                # This signals where player info we care about begins.
                if data['username'] in player_info and i == 17:
                    # print('set players true.')
                    players = True
                    continue
                if players:
                    print(player_info)
            except Exception as e:
                print(e)
                print("---------- end of list ---------")
                return
        if not players:
            print(f'NO PLAYERS FOUND players is {players}')
            return

        # https://www.playdiplomacy.com/stats.php?sub_page=1&current_page=2
        next_href = f'{players_url}&current_page={current_page}'
        response = s.get(url=next_href)
        soup = BeautifulSoup(response.text, features="html.parser")
        next_link = soup.find('a', text='next')


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    do_login()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
