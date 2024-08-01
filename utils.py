import requests
import logging
import json
import os
from colorama import Fore, Style
from tabulate import tabulate

FOLLOWERS_FILE = 'followers.json'

def get_github_data(url, username, token):
    results = []
    while url:
        logging.info(f"Fetching data from {url}")
        try:
            response = requests.get(url, auth=(username, token), timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Request error occurred: {req_err}")
            raise

        try:
            results.extend(response.json())
        except ValueError as json_err:
            logging.error(f"JSON decoding error: {json_err}")
            raise

        url = response.links.get('next', {}).get('url')
    logging.info(f"Fetched {len(results)} items from GitHub")
    return results

def display_list(title, data):
    table = [[index + 1, user] for index, user in enumerate(data)]
    print(Fore.CYAN + Style.BRIGHT + title)
    print(tabulate(table, headers=[Fore.YELLOW + Style.BRIGHT + "Index", Fore.YELLOW + Style.BRIGHT + "Username"], tablefmt='grid'))
    print()

def save_followers(followers):
    with open(FOLLOWERS_FILE, 'w') as file:
        json.dump(followers, file)
    logging.info(f"Saved {len(followers)} followers to {FOLLOWERS_FILE}")

def load_previous_followers():
    if os.path.exists(FOLLOWERS_FILE):
        with open(FOLLOWERS_FILE, 'r') as file:
            followers = json.load(file)
        logging.info(f"Loaded {len(followers)} previous followers from {FOLLOWERS_FILE}")
        return followers
    return []

def find_unfollowers(current_followers, previous_followers):
    unfollowers = set(previous_followers) - set(current_followers)
    logging.info(f"Found {len(unfollowers)} users who unfollowed you")
    return unfollowers
