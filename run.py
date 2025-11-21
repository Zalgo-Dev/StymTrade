import os
import json
from pathlib import Path
from steam import Client
from dotenv import load_dotenv


load_dotenv()


USER = os.getenv("STEAM_USER")
PASS = os.getenv("STEAM_PASSW")

TOKENS_FILE = Path("tokens.json")

def load_refresh_token():
    """Return the stored refresh token if available, else None."""
    if TOKENS_FILE.exists():
        try:
            data = json.loads(TOKENS_FILE.read_text() or "{}")
            return data.get("refresh_token")
        except json.JSONDecodeError:
            return None
    return None

def save_refresh_token(refresh_token: str):
    """Persist the refresh token for future sessions."""
    data = {"refresh_token": refresh_token}
    TOKENS_FILE.write_text(json.dumps(data))


class Bot(Client):
    """Steam client that auto-saves tokens and accepts gift trades."""
    async def on_ready(self):
        print("Logged in as", self.user)
        if self.refresh_token:
            current = load_refresh_token()
            if current != self.refresh_token:
                save_refresh_token(self.refresh_token)
                print("Refresh token saved.")


    async def on_auth_code_required(self, code_type):
        code = input(f"Enter the {code_type} code (Steam Guard): ")
        await self.submit_code(code)


    async def on_trade(self, trade):
        print(f"Trade received #{trade.id}")
        if trade.is_gift():
            print("Gift trade detected; accepting automatically.")
            await trade.accept()


def main():
    """Launch the Steam bot with stored credentials or password fallback."""
    if not USER:
        print("Environment variable STEAM_USER is missing.")
        return
    refresh_token = load_refresh_token()
    bot = Bot()

    if refresh_token:
        print("Attempting login with refresh token (no 2FA expected)...")
        try:
            bot.run(refresh_token=refresh_token)
            return
        except Exception as e:
            print(f"Refresh token failed: {e}. Trying username and password.")

    if not PASS:
        print("Environment variable STEAM_PASS is missing. Add it to .env.")
        return
    print("Attempting password login (Steam Guard may be required).")
    bot.run(USER, PASS)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Keyboard interruption received. Shutting down without restart.")