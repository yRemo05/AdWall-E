# Discord Bot Template

A JSON-configured Discord bot template built with Python cogs. The project includes moderation, server settings, security, ticket, help, event, and utility modules that can be customized for a Discord server.

## Features

- Cog-based command organization under `Cogs/`
- Prefix configuration from `Data/configuration.json`
- Moderation commands for bans, kicks, purges, channel locks, and role management
- Server settings for welcome/leave messages, auto roles, ticket panels, embeds, and stat counters
- Security helpers for blacklisted words, channel message restrictions, and server locking
- Ticket creation through Discord interactions
- JSON-backed data files for configuration, statuses, guild data, reaction roles, and changelogs
- Windows launcher script through `bot.bat`

## Project Structure

```text
.
|-- main.py
|-- bot.bat
|-- Cogs/
|   |-- Development.py
|   |-- Errors.py
|   |-- Events.py
|   |-- Help.py
|   |-- Moderation.py
|   |-- Security.py
|   |-- Settings.py
|   |-- Utility.py
|   `-- Ext/
`-- Data/
    |-- Changelogs.json
    |-- Guild.json
    |-- Reaction_Roles.json
    |-- Statuses.json
    `-- configuration.json
```

## Requirements

- Python 3.8 or newer
- A Discord bot application and token from the Discord Developer Portal
- Discord gateway intents enabled for the bot
- Python packages used by the bot code, including:
  - `discord.py` or the Discord API wrapper version your fork uses
  - `colorama`

This repository does not currently include a `requirements.txt`, so install the packages that match your local bot wrapper before running.

## Setup

1. Clone the repository.
2. Install the required Python packages.
3. Open `Data/configuration.json`.
4. Set the bot token:

```json
{
  "token": "YOUR_BOT_TOKEN",
  "prefix": "!"
}
```

5. Configure any channel IDs, role IDs, embed defaults, ticket settings, and moderation settings needed for your server.
6. Invite the bot to your Discord server with the permissions required by the commands you plan to use.
7. Run the bot:

```powershell
python main.py
```

On Windows, you can also start it with:

```powershell
.\bot.bat
```

## Configuration

The main settings live in `Data/configuration.json`.

Common values to update:

- `application_ID`: Discord application ID
- `token`: Discord bot token
- `prefix`: command prefix
- `settings_perms`, `ticket_perms`, `giveaway_perms`, `mod_perms`: role IDs allowed to use protected commands
- `ticket_category`, `ticket_message`, `ticket_information_channel`: ticket system IDs
- `welcome_channel`, `bye-bye_channel`: member event channels
- `role_to_assing_to_joined_member`: auto-role ID
- `blacklisted_words`: words removed by the message watcher
- `logging`: console logging toggle

Keep real bot tokens out of public commits.

## Running

When `main.py` starts, it reads `Data/configuration.json`, creates a command bot with all intents, loads every `.py` file in `Cogs/`, and connects to Discord with the configured token.

## License

This project is licensed under the terms in `LICENSE`.
