import logging
import requests
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from utils import get_github_data, display_list, save_followers, load_previous_followers, find_unfollowers

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# GitHub API request session with retries
session = requests.Session()
retries = Retry(total=5, backoff_factor=2, status_forcelist=[500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))

def fetch_paginated_data(url, username, token):
    """
    Fetches paginated data from GitHub API and handles rate limits.
    """
    data = []
    page = 1

    while True:
        headers = {"Authorization": f"token {token}"}
        response = session.get(f"{url}?page={page}&per_page=100", headers=headers, timeout=30)

        # Handle rate limits
        if response.status_code == 403 and "X-RateLimit-Remaining" in response.headers:
            reset_time = int(response.headers.get("X-RateLimit-Reset", time.time()))
            wait_time = reset_time - int(time.time()) + 1
            logging.warning(f"Rate limit exceeded. Waiting {wait_time} seconds...")
            time.sleep(wait_time)
            continue  # Retry after waiting

        # Handle errors
        try:
            response.raise_for_status()
            page_data = response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data from {url}: {e}")
            break

        if not page_data:
            break  # No more pages

        data.extend(page_data)
        page += 1

    return data

def get_user_following(username, token):
    logging.info(f"Getting users followed by {username}")
    following_url = f"https://api.github.com/users/{username}/following"
    following_data = fetch_paginated_data(following_url, username, token)
    following = [user["login"] for user in following_data]
    logging.info(f"{username} is following {len(following)} users")
    return following

def get_user_followers(username, token):
    logging.info(f"Getting followers of {username}")
    followers_url = f"https://api.github.com/users/{username}/followers"
    followers_data = fetch_paginated_data(followers_url, username, token)
    followers = [user["login"] for user in followers_data]
    logging.info(f"{username} has {len(followers)} followers")
    return followers

def find_non_followers(following, followers):
    logging.info("Finding users who do not follow back")
    non_followers = set(following) - set(followers)
    logging.info(f"Found {len(non_followers)} users who do not follow back")
    return non_followers

def unfollow_user(username, target_user, token):
    unfollow_url = f"https://api.github.com/user/following/{target_user}"
    headers = {"Authorization": f"token {token}"}

    try:
        response = session.delete(unfollow_url, headers=headers, timeout=30)
        response.raise_for_status()
        if response.status_code == 204:
            logging.info(f"Successfully unfollowed {target_user}")
        else:
            logging.error(f"Failed to unfollow {target_user}: {response.status_code}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error occurred while unfollowing {target_user}: {req_err}")

def list_followers(username, token):
    """List all followers."""
    followers = get_user_followers(username, token)
    display_list("Followers", followers)

def list_following(username, token):
    """List all users you are following."""
    following = get_user_following(username, token)
    display_list("Following", following)

def list_non_followers(username, token):
    """List users you follow who do not follow you back."""
    following = get_user_following(username, token)
    followers = get_user_followers(username, token)
    non_followers = find_non_followers(following, followers)
    display_list("Non-Followers", non_followers)

def list_unfollowers(username, token):
    """List users who have unfollowed you since the last check."""
    current_followers = get_user_followers(username, token)
    previous_followers = load_previous_followers()
    save_followers(current_followers)
    unfollowers = find_unfollowers(current_followers, previous_followers)
    display_list("Unfollowers", unfollowers)

def unfollow_non_followers(username, token):
    """Automatically unfollow users who do not follow you back."""
    following = get_user_following(username, token)
    followers = get_user_followers(username, token)
    non_followers = find_non_followers(following, followers)
    for user in non_followers:
        unfollow_user(username, user, token)
