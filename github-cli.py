import argparse
import logging
from api import list_followers, list_following, list_non_followers, list_unfollowers, unfollow_non_followers
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    commands = {
        'followers': 'List your followers',
        'following': 'List users you are following',
        'non-followers': 'List users you follow who do not follow you back',
        'unfollowers': 'List users who unfollowed you since last check',
        'unfollow-non-followers': 'Unfollow users who do not follow you back'
    }

    parser = argparse.ArgumentParser(description="GitHub Follower Management CLI")
    parser.add_argument('command', nargs='?', choices=commands.keys(), help="Command to execute")
    parser.add_argument('--username', required=True, help="GitHub username")
    parser.add_argument('--token', required=True, help="GitHub personal access token")

    args = parser.parse_args()

    if args.command:
        command = args.command
    else:
        print(Fore.CYAN + Style.BRIGHT + "GitHub Follower Management CLI")
        print(Fore.YELLOW + Style.BRIGHT + "Available Commands:")
        for key, description in commands.items():
            print(Fore.GREEN + f"{key}: {description}")
        command = input(Fore.CYAN + "Enter the command you want to execute: ")

    if command == 'followers':
        list_followers(args.username, args.token)
    elif command == 'following':
        list_following(args.username, args.token)
    elif command == 'non-followers':
        list_non_followers(args.username, args.token)
    elif command == 'unfollowers':
        list_unfollowers(args.username, args.token)
    elif command == 'unfollow-non-followers':
        unfollow_non_followers(args.username, args.token)
    else:
        print(Fore.RED + "Invalid command. Exiting.")

if __name__ == "__main__":
    main()
