import requests
import time
import fake_useragent
from bs4 import BeautifulSoup as bs

ua = fake_useragent.UserAgent()
chrome = ua.chrome

class ScrapRaffles:
    def __init__(self, authenticate: str, proxy: str | None = None, 
                 retries: int | None = 5, delay: float | None = 2.5,
                 sorting: str | None = ''):
        
        self.retries = retries
        self.delay = delay
        self.sorting = sorting
        
        self.session = requests.Session()
        self.session.cookies.update({'scr_session': authenticate})
        self.session.headers.update({'user-agent': chrome})
        if proxy:
            self.session.proxies.update({"http": f"http://{proxy}"})

    def get_content(self, url: str) -> bytes | None:
        for _ in range(self.retries):
            response = self.session.get(url)
            if response.status_code == 200:
                return response.content

            time.sleep(self.delay)


    def get_raffles(self, content: bytes) -> list | None:
        raffles_entered = []
        if not content:
            return
    
        soup = bs(content, 'html.parser')
        entered = fetch_raffles_entered(soup)
        not_endered = fetch_raffles_not_entered(soup, entered)

        return {
            'entered': entered,
            'not_entered': not_endered
        }
    
    def post_join_raffle(self, raffle_id: str, csrf: str, raffle_hash: str):
        data = {
            'raffle': raffle_id,
            'captcha': '',
            'hash': raffle_hash,
            'flag': 'false',
            'csrf': csrf,
        }
        return self.session.post('https://scrap.tf/ajax/viewraffle/EnterRaffle', data=data).json()

    def fetch_csrf(self, soup: bs) -> str:
        return soup.find("input", {"name" : "csrf"})['value']

    def fetch_hash(self, soup: bs) -> str:
        return soup.find('button', {'id': 'raffle-enter'})['onclick'].split("'")[3]

def fetch_raffles_not_entered(soup: bs, entered: list) -> list:
    _all = []
    raffles_div = soup.find("div", {'id': 'raffles-list'})
    raffles = raffles_div.find_all("div", class_="panel-raffle")
    for raffle in raffles:
        id = raffle.find("div", class_="raffle-name").find("a")['href'].split("/")[2]
        _all.append(id) 

    not_entered = [_ for _ in _all if _ not in entered]
    return not_entered

def fetch_raffles_entered(soup: bs) -> list:
    entered = []
    raffles_div = soup.find("div", {'id': 'raffles-list'})
    raffles = raffles_div.find_all("div", class_="panel-raffle raffle-entered")

    for raffle in raffles:
        id = raffle.find("div", class_="raffle-name").find("a")['href'].split("/")[2]
        entered.append(id) 

    return entered