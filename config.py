import os
import sys
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Global admin dictionary
admins = {}

def getenv_bool(name: str, default: bool = False) -> bool:
    """Helper function to get boolean environment variables"""
    return os.getenv(name, str(default)).lower() in ('true', '1', 'yes', 'on')

def getenv_int(name: str, default: int = 0) -> int:
    """Helper function to get integer environment variables"""
    try:
        return int(os.getenv(name, default))
    except (ValueError, TypeError):
        return default

def getenv_list(name: str, default: str = "") -> List[str]:
    """Helper function to get list environment variables"""
    value = os.getenv(name, default)
    return [item.strip() for item in value.split() if item.strip()]

def getenv_int_list(name: str, default: str = "") -> List[int]:
    """Helper function to get integer list environment variables"""
    try:
        return [int(x.strip()) for x in os.getenv(name, default).split() if x.strip().isdigit()]
    except (ValueError, AttributeError):
        return []

# =======================
# CLIENT CONFIGURATION
# =======================
API_ID = getenv_int("API_ID", 26128734)
API_HASH = os.getenv("API_HASH", "ff991e0856938ede932dc88fa2f15b61")
BOT_TOKEN = os.getenv("BOT_TOKEN", "5990830200:AAGlQbppgRb5J9xIh2MrKJOrGW7IP768yRs")
SESSION_NAME = os.getenv("SESSION_NAME", "MusicBot_Session")
SESSION_STRING = os.getenv("SESSION_STRING", "")

# Validate critical variables
if not all([API_ID, API_HASH, BOT_TOKEN]):
    print("❌ ERROR: Missing critical environment variables (API_ID, API_HASH, BOT_TOKEN)")
    sys.exit(1)

# =======================
# BOT CONFIGURATION
# =======================
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "rda")
ALIVE_NAME = os.getenv("ALIVE_NAME", "Music Bot")
BOT_USERNAME = os.getenv("BOT_USERNAME", "MusicBot")
BOT_NAME = os.getenv("BOT_NAME", "Music Bot")

# Repository settings
UPSTREAM_REPO = os.getenv("UPSTREAM_REPO", "https://github.com/X02lx/")
UPSTREAM_BRANCH = os.getenv("UPSTREAM_BRANCH", "main")

# Music settings
DURATION_LIMIT = getenv_int("DURATION_LIMIT", 60)  # minutes
SONG_DOWNLOAD_DURATION = getenv_int("SONG_DOWNLOAD_DURATION", 9)  # minutes
PLAYLIST_FETCH_LIMIT = getenv_int("PLAYLIST_FETCH_LIMIT", 25)

# =======================
# GROUP/CHANNEL SETTINGS
# =======================
GROUP_SUPPORT = os.getenv("GROUP_SUPPORT", "Hirosi_hr")
UPDATES_CHANNEL = os.getenv("UPDATES_CHANNEL", "Hirosi_hr")
LOG_GROUP_ID = getenv_int("LOG_GROUP_ID", 0)

# =======================
# DATABASE CONFIGURATION
# =======================
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb+srv://veez:mega@cluster0.heqnd.mongodb.net/veez?retryWrites=true&w=majority")

# =======================
# PERMISSIONS
# =======================
COMMAND_PREFIXES = getenv_list("COMMAND_PREFIXES", "شغل تشغيل ش / ! . #")
OWNER_ID = getenv_int_list("OWNER_ID", "6878196064")
SUDO_USERS = getenv_int_list("SUDO_USERS", "6878196064")

# Combine owner and sudo users
OWNER_ID.extend(SUDO_USERS)
OWNER_ID = list(set(OWNER_ID))  # Remove duplicates

# =======================
# IMAGE RESOURCES
# =======================
IMG_1 = os.getenv("IMG_1", "https://te.legra.ph/file/2a726c634dbc3b9e8f451.png")
IMG_2 = os.getenv("IMG_2", "https://te.legra.ph/file/90e3b3aeb77e3e598d66d.png")
IMG_3 = os.getenv("IMG_3", "https://te.legra.ph/file/d70bb6fa92728763c671f.png")
IMG_4 = os.getenv("IMG_4", "https://te.legra.ph/file/430dcf25456f2bb38109f.png")
IMG_5 = os.getenv("IMG_5", "https://te.legra.ph/file/cd5c96a3c7e8ae1913ef3.png")
ALIVE_IMG = os.getenv("ALIVE_IMG", "https://telegra.ph/file/c83b000f004f01897fe18.png")

# Group all images for easy access
IMAGES = [IMG_1, IMG_2, IMG_3, IMG_4, IMG_5]

# =======================
# FEATURES TOGGLE
# =======================
AUTO_LEAVING_ASSISTANT = getenv_bool("AUTO_LEAVING_ASSISTANT", True)
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")
GENIUS_API_TOKEN = os.getenv("GENIUS_API_TOKEN", "")

# =======================
# ADVANCED SETTINGS
# =======================
MAX_CONCURRENT_TRANSMISSIONS = getenv_int("MAX_CONCURRENT_TRANSMISSIONS", 3)
CLEANMODE_DELETE_MINS = getenv_int("CLEANMODE_DELETE_MINS", 5)

# Auto-join channels (improved)
AUTO_JOIN_CHANNELS = getenv_list("AUTO_JOIN_CHANNELS", "RR3R2 xl444")

# =======================
# VALIDATION
# =======================
def validate_config():
    """Validate configuration and show warnings"""
    warnings = []
    
    if not SESSION_STRING and not SESSION_NAME:
        warnings.append("⚠️  No session provided for userbot")
    
    if not MONGODB_URL or "mongodb" not in MONGODB_URL.lower():
        warnings.append("⚠️  MongoDB URL seems invalid")
    
    if len(OWNER_ID) == 0:
        warnings.append("⚠️  No owner IDs configured")
    
    if warnings:
        print("Configuration Warnings:")
        for warning in warnings:
            print(warning)
        print()

# Run validation
validate_config()

# =======================
# EXPORT ALL VARIABLES
# =======================
__all__ = [
    'API_ID', 'API_HASH', 'BOT_TOKEN', 'SESSION_NAME', 'SESSION_STRING',
    'OWNER_USERNAME', 'ALIVE_NAME', 'BOT_USERNAME', 'BOT_NAME',
    'DURATION_LIMIT', 'GROUP_SUPPORT', 'UPDATES_CHANNEL',
    'MONGODB_URL', 'COMMAND_PREFIXES', 'OWNER_ID', 'SUDO_USERS',
    'IMG_1', 'IMG_2', 'IMG_3', 'IMG_4', 'IMG_5', 'ALIVE_IMG', 'IMAGES',
    'AUTO_LEAVING_ASSISTANT', 'AUTO_JOIN_CHANNELS', 'admins'
]
