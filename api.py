import logging

import requests

from utils import get_github_data, display_list, save_followers, load_previous_followers, find_unfollowers


def get_user_following(username, token):
    logging.info(f"Getting users followed by {username}")
    following_url = f'https://api.github.com/users/{username}/following'
    following_data = get_github_data(following_url, username, token)
    following = [user['login'] for user in following_data]
    logging.info(f"{username} is following {len(following)} users")
    return following

def get_user_followers(username, token):
    logging.info(f"Getting followers of {username}")
    followers_url = f'https://api.github.com/users/{username}/followers'
    followers_data = get_github_data(followers_url, username, token)
    followers = [user['login'] for user in followers_data]
    logging.info(f"{username} has {len(followers)} followers")
    return followers

def find_non_followers(following, followers):
    logging.info("Finding users who do not follow back")
    non_followers = set(following) - set(followers)
    logging.info(f"Found {len(non_followers)} users who do not follow back")
    return non_followers

def unfollow_user(username, target_user, token):
    unfollow_url = f'https://api.github.com/user/following/{target_user}'
    try:
        response = requests.delete(unfollow_url, auth=(username, token), timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error occurred while unfollowing {target_user}: {req_err}")
    else:
        if response.status_code == 204:
            logging.info(f"Successfully unfollowed {target_user}")
        else:
            logging.error(f"Failed to unfollow {target_user}: {response.status_code}")

def list_followers(username, token):
    """
    List all followers.
    """
    followers = get_user_followers(username, token)
    display_list("Followers", followers)

def list_following(username, token):
    """
    List all users you are following.
    """
    following = get_user_following(username, token)
    display_list("Following", following)

def list_non_followers(username, token):
    """
    List users you follow who do not follow you back.
    """
    following = get_user_following(username, token)
    followers = get_user_followers(username, token)
    non_followers = find_non_followers(following, followers)
    display_list("Non-Followers", non_followers)

def list_unfollowers(username, token):
    """
    List users who have unfollowed you since the last check.
    """
    current_followers = get_user_followers(username, token)
    previous_followers = load_previous_followers()
    save_followers(current_followers)
    unfollowers = find_unfollowers(current_followers, previous_followers)
    display_list("Unfollowers", unfollowers)

def unfollow_non_followers(username, token):
    """
    Automatically unfollow users who do not follow you back.
    """
    following = get_user_following(username, token)
    followers = get_user_followers(username, token)
    non_followers = find_non_followers(following, followers)
    for user in non_followers:
        unfollow_user(username, user, token)
