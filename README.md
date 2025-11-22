# YTradeBot

Small Python bot that connects to Steam, stores the session refresh token, and auto-accepts incoming gift trades.

### Support my bot project by gifting unused skins :
https://steamcommunity.com/profiles/76561198774956505/

## Prerequisites
- Python 3.10+
- Steam account with Steam Guard configured
- API requirements from the `steam` package

## Installation
1. Create and activate a virtual environment.
2. Install dependencies:
	```powershell
	pip install -r requirements.txt
	```
3. Create a `.env` file alongside `run.py` and add:
	```text
	STEAM_USER=your_steam_username
	STEAM_PASSW=your_password
	```

## Usage
- First run: the bot logs in with username/password and may prompt for a Steam Guard code. The refresh token is saved to `tokens.json` for future sessions.
- Subsequent runs: the bot reuses the stored refresh token to bypass Steam Guard, falling back to password login if needed.
- Every incoming trade is logged. Gift trades are accepted automatically.

Start the bot:
```powershell
python run.py
```

Stop the bot with `Ctrl+C`.

## Key Script Behaviors
- `load_refresh_token()` reads the cached token if it exists and is valid JSON.
- `save_refresh_token()` persists the latest token so the next launch can reuse it.
- `Bot.on_ready()` saves the current token as soon as Steam confirms the session.
- `Bot.on_auth_code_required()` prompts for the Steam Guard code and submits it.
- `Bot.on_trade()` prints trade summaries and accepts gift trades automatically.
- `main()` orchestrates the login flow, preferring token-based login over password login.
