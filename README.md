
## GitHub Folloers Manager CLI Tool

<div style="text-align: center;">
    <img src="https://user-images.githubusercontent.com/76784461/156901083-8fb10d9d-4509-4f55-a071-6d0d3faed233.png" alt="GitHub CLI Tool" style="width: 200px; height: auto;">
</div>

A powerful command-line interface (CLI) tool for managing and tracking GitHub followers and following relationships.
This tool allows you to list your followers, see who you're following, identify users who don't follow you back, find unfollowers, and even automatically unfollow users who don't follow you.

## Features

- **List Followers**: Display all users who follow you.
- **List Following**: Show all users you are following.
- **List Non-Followers**: Identify users you follow who do not follow you back.
- **List Unfollowers**: Track users who have unfollowed you since the last check.
- **Unfollow Non-Followers**: Automatically unfollow users who do not follow you back.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- GitHub Personal Access Token (PAT) with appropriate permissions. [Generate a PAT here](https://github.com/settings/tokens).

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/nimanikoo/GitHub-Followers-management.git
   cd GitHub-Followers-management
   ```

2. **Set Up a Virtual Environment** (Recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To use the GitHub CLI tool, run the following command:

```bash
python github_cli.py [command]
```

### Available Commands

- **`followers`**: List all followers.
  ```bash
  python github_cli.py followers
  ```

- **`following`**: List all users you are following.
  ```bash
  python github_cli.py following
  ```

- **`non-followers`**: List users you follow who do not follow you back.
  ```bash
  python github_cli.py non-followers
  ```

- **`unfollowers`**: List users who have unfollowed you since the last check.
  ```bash
  python github_cli.py unfollowers
  ```

- **`unfollow-non-followers`**: Automatically unfollow users who do not follow you back.
  ```bash
  python github_cli.py unfollow-non-followers
  ```

## File Descriptions

- **`github_cli.py`**: Main script for handling commands and user interactions.
- **`github/api.py`**: Functions for interacting with the GitHub API.
- **`github/utils.py`**: Utility functions for data management, including saving and loading followers.
- **`requirements.txt`**: Lists necessary Python libraries.
- **`env`**: Github Username and Token values

```text
GITHUB_USERNAME=USERNAME
GITHUB_TOKEN=TOKEN
```

### Export env
You can use `env` sample file to define your own values then use command below to export all variables into the environment:
```sh
export $(grep -v '^#' env | xargs)
```

## Contributing

Contributions are welcome! If you have suggestions or improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

## Contact

For any questions or feedback, please reach out to [nikoonazar.nima@gmail.com](mailto:nikoonazar.nima@gmail.com).

**Note**: Ensure to replace `[your-github-username]` and `[your-github-token]` with your actual GitHub username and personal access token when using the tool.
