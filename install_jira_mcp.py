import json
import os
import sys

CONFIG_PATH = os.path.expanduser("~/.config/Claude/claude_desktop_config.json")

def install_jira_mcp():
    print("Atlassian Jira MCP Installer for Claude Desktop")
    print("-----------------------------------------------")
    print(f"Target Configuration File: {CONFIG_PATH}")
    
    jira_url = input("Enter your Jira URL (e.g., https://your-domain.atlassian.net): ").strip()
    if not jira_url:
        print("Error: Jira URL is required.")
        return

    email = input("Enter your Atlassian Email: ").strip()
    if not email:
        print("Error: Email is required.")
        return

    token = input("Enter your Atlassian API Token: ").strip()
    if not token:
        print("Error: API Token is required.")
        return

    # Prepare the new config entry
    # Using 'npx -y' to ensure it installs without prompting if missing
    new_config = {
        "command": "npx",
        "args": [
            "-y",
            "@modelcontextprotocol/server-atlassian"
        ],
        "env": {
            "JIRA_URL": jira_url,
            "ATLASSIAN_EMAIL": email,
            "ATLASSIAN_API_TOKEN": token
        }
    }

    # Load existing config or create new
    data = {"mcpServers": {}}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r') as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
        except json.JSONDecodeError:
            print(f"Warning: Could not parse {CONFIG_PATH}. Creating a new one.")
        except Exception as e:
            print(f"Error reading config: {e}")
            return
    else:
        # Ensure directory exists
        try:
            os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        except OSError as e:
            print(f"Error creating directory: {e}")
            return

    if "mcpServers" not in data:
        data["mcpServers"] = {}

    # specific key for jira
    data["mcpServers"]["jira"] = new_config

    try:
        with open(CONFIG_PATH, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\nSuccess! Configuration written to {CONFIG_PATH}")
        print("Please restart Claude Desktop to apply changes.")
    except Exception as e:
        print(f"Error writing config: {e}")

if __name__ == "__main__":
    install_jira_mcp()
