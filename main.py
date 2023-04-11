import dotenv
import configparser
import os
import ast
import time
import random
from bs4 import BeautifulSoup as bs
import logging 
logging.basicConfig(level='INFO',
                format='%(asctime)s - %(message)s',
                datefmt='%H:%M:%S')

from scraptf import ScrapRaffles

def os_path(file):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), file)

def main():
    dotenv.load_dotenv(dotenv.find_dotenv())
    proxy = os.getenv('PROXY')
    authenticate = os.getenv('COOKIE')

    timeouts = {}
    config = configparser.ConfigParser()
    config.read(os_path('config.ini'))
    timeouts['captcha'] = ast.literal_eval(config.get('TIMEOUTS', 'captcha'))
    timeouts['next_raffle'] = ast.literal_eval(config.get('TIMEOUTS', 'next_raffle'))
    timeouts['next_refresh'] = ast.literal_eval(config.get('TIMEOUTS', 'next_refresh'))

    scrap = ScrapRaffles(authenticate, proxy, sorting='ending')

    while True:
        content = scrap.get_content(f"https://scrap.tf/raffles/{scrap.sorting}")
        raffles = scrap.get_raffles(content)
        entered = raffles['entered']
        not_entered = raffles['not_entered']

        logging.info(f"Joining {len(not_entered)} raffles ({len(entered)} joined).")

        for _, raffle_id in enumerate(not_entered, 1):
            logging.info(f"#{_} Joining raffle {raffle_id}.")

            content = scrap.get_content(f"https://scrap.tf/raffles/{raffle_id}")
            if not content:
                continue
            soup = bs(content, 'html.parser')

            csrf = scrap.fetch_csrf(soup)
            raffle_hash = scrap.fetch_hash(soup)
            
            status = scrap.post_join_raffle(raffle_id, csrf, raffle_hash)
            if "captcha" in status:
                lower_bound, upper_bound = timeouts['next_refresh']
                timeout = random.uniform(lower_bound, upper_bound)
                logging.critical(f"Captcha required. Waiting {timeout} seconds.")
                time.sleep(timeout)

            if "success" not in status:
                message = status['message']
                logging.info(f"Could not join raffle. Scrap message: {message}")
                
                if 'Please wait' in message:
                    timeout = int(message.split(" ")[2])
                    time.sleep(timeout)
                else:
                    time.sleep(5)

            lower_bound, upper_bound = timeouts['next_raffle']
            timeout = random.uniform(lower_bound, upper_bound)
            time.sleep(timeout)

        lower_bound, upper_bound = timeouts['next_refresh']
        timeout = random.uniform(lower_bound, upper_bound)
        logging.info(f"Refreshing raffles in {timeout} seconds.")
        time.sleep(timeout)

if __name__ == "__main__":
    main()        