import logging
import os
import sys
import time

import telegram.ext as tg
from pyrogram import Client
from telethon import TelegramClient

StartTime = time.time()

# Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger("telethon").setLevel(logging.ERROR)
logging.getLogger("pymongo").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pyrate_limiter").setLevel(logging.ERROR)

LOGGER = logging.getLogger(__name__)

# Python version check
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error("Python 3.6+ required. Bot quitting.")
    quit(1)

ENV = bool(os.environ.get("ENV", False))

if ENV:
    # 🔑 REQUIRED VARIABLES
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    TOKEN = os.environ.get("BOT_TOKEN")
    OWNER_ID = int(os.environ.get("OWNER_ID"))
    DB_URI = os.environ.get("DATABASE_URL")

    # ⚙️ OPTIONAL
    ALLOW_CHATS = os.environ.get("ALLOW_CHATS", True)
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", False)
    CASH_API_KEY = os.environ.get("CASH_API_KEY", None)
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))
    EVENT_LOGS = os.environ.get("EVENT_LOGS", None)
    INFOPIC = bool(os.environ.get("INFOPIC", "True"))
    LOAD = os.environ.get("LOAD", "").split()
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
    NO_LOAD = os.environ.get("NO_LOAD", "").split()

    START_IMG = os.environ.get(
        "START_IMG", "https://telegra.ph/file/40eb1ed850cdea274693e.jpg"
    )

    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", True))
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", "SupportGroup")
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    TIME_API_KEY = os.environ.get("TIME_API_KEY", None)
    WORKERS = int(os.environ.get("WORKERS", 8))

    # 🛡 SAFE LISTS
    def safe_int_set(var):
        try:
            return set(int(x) for x in os.environ.get(var, "").split() if x)
        except:
            return set()

    BL_CHATS = safe_int_set("BL_CHATS")
    DRAGONS = safe_int_set("DRAGONS")
    DEV_USERS = safe_int_set("DEV_USERS")
    DEMONS = safe_int_set("DEMONS")
    TIGERS = safe_int_set("TIGERS")
    WOLVES = safe_int_set("WOLVES")

else:
    from FallenRobot.config import Development as Config

    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    TOKEN = Config.TOKEN
    OWNER_ID = int(Config.OWNER_ID)
    DB_URI = Config.DATABASE_URL

    ALLOW_CHATS = Config.ALLOW_CHATS
    ALLOW_EXCL = Config.ALLOW_EXCL
    CASH_API_KEY = Config.CASH_API_KEY
    DEL_CMDS = Config.DEL_CMDS
    EVENT_LOGS = Config.EVENT_LOGS
    INFOPIC = Config.INFOPIC
    LOAD = Config.LOAD
    MONGO_DB_URI = Config.MONGO_DB_URI
    NO_LOAD = Config.NO_LOAD
    START_IMG = Config.START_IMG
    STRICT_GBAN = Config.STRICT_GBAN
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
    TIME_API_KEY = Config.TIME_API_KEY
    WORKERS = Config.WORKERS

    BL_CHATS = set(Config.BL_CHATS or [])
    DRAGONS = set(Config.DRAGONS or [])
    DEV_USERS = set(Config.DEV_USERS or [])
    DEMONS = set(Config.DEMONS or [])
    TIGERS = set(Config.TIGERS or [])
    WOLVES = set(Config.WOLVES or [])

# ✅ FINAL SETUP
DRAGONS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)

updater = tg.Updater(TOKEN, workers=WORKERS, use_context=True)
dispatcher = updater.dispatcher

telethn = TelegramClient("Fallen", API_ID, API_HASH)
pbot = Client("FallenRobot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)

print("[INFO]: Getting Bot Info...")
BOT_ID = dispatcher.bot.id
BOT_NAME = dispatcher.bot.first_name
BOT_USERNAME = dispatcher.bot.username

# Convert sets to lists
DRAGONS = list(DRAGONS) + list(DEV_USERS)
DEV_USERS = list(DEV_USERS)
WOLVES = list(WOLVES)
DEMONS = list(DEMONS)
TIGERS = list(TIGERS)

# Handlers
from FallenRobot.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler