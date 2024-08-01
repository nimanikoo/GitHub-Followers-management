import argparse
import logging
import os
from api import list_followers, list_following, list_non_followers, list_unfollowers, unfollow_non_followers
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    commands = {
        'followers': list_followers,
        'following': list_following,
        'non-followers': list_non_followers,
        'unfollowers': list_unfollowers,
        'unfollow-non-followers': unfollow_non_followers
    }

    parser = argparse.ArgumentParser(description="GitHub Follower Management CLI")
    parser.add_argument('command', nargs='?', choices=commands.keys(), help="Command to execute")

    args = parser.parse_args()

    if args.command:
        command = args.command
    else:
        print(Fore.CYAN + Style.BRIGHT + "GitHub Follower Management CLI")
        print(Fore.YELLOW + Style.BRIGHT + "Available Commands:")
        for key, description in commands.items():
            print(Fore.GREEN + f"{key}: {description.__doc__}")
        command = input(Fore.CYAN + "Enter the command you want to execute: ")

    command_func = commands.get(command)
    if command_func:
        try:
            command_func(os.environ.get('GITHUB_USERNAME'), os.environ.get('GITHUB_TOKEN'))
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            print(Fore.RED + "An error occurred while executing the command. Please try again.")
    else:
        print(Fore.RED + "Invalid command. Exiting.")

if __name__ == "__main__":
    main()
