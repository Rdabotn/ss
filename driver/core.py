import asyncio
import sys
from typing import Optional
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from config import (
    API_HASH, 
    API_ID, 
    BOT_TOKEN, 
    SESSION_NAME, 
    SESSION_STRING,
    BOT_NAME,
    AUTO_JOIN_CHANNELS
)

class MusicBot:
    def __init__(self):
        self.bot: Optional[Client] = None
        self.user: Optional[Client] = None
        self.calls: Optional[PyTgCalls] = None
        self.bot_info = None
        self.user_info = None

# Global instance
music_bot = MusicBot()

# =======================
# BOT CLIENT
# =======================
try:
    bot = Client(
        name="MusicBot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        plugins={"root": "program"},
        in_memory=True,  # Better performance
        max_concurrent_transmissions=3  # Prevent flood limits
    )
    music_bot.bot = bot
    print("✅ Bot client initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize bot client: {e}")
    sys.exit(1)

# =======================
# USERBOT CLIENT (ASSISTANT)
# =======================
try:
    if SESSION_STRING:
        user = Client(
            name=SESSION_NAME,
            session_string=SESSION_STRING,
            api_id=API_ID,
            api_hash=API_HASH,
            in_memory=True,
            max_concurrent_transmissions=3
        )
    else:
        user = Client(
            name=SESSION_NAME,
            api_id=API_ID,
            api_hash=API_HASH,
            in_memory=True,
            max_concurrent_transmissions=3
        )
    music_bot.user = user
    print("✅ Userbot client initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize userbot client: {e}")
    sys.exit(1)

# =======================
# PYTGCALLS CLIENT (FIXED)
# =======================
try:
    calls = PyTgCalls(
        user,
        cache_duration=120  # Removed log_mode parameter
    )
    music_bot.calls = calls
    print("✅ PyTgCalls client initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize PyTgCalls client: {e}")
    # Try without cache_duration as fallback
    try:
        calls = PyTgCalls(user)
        music_bot.calls = calls
        print("✅ PyTgCalls client initialized successfully (fallback mode)")
    except Exception as fallback_error:
        print(f"❌ Failed to initialize PyTgCalls client (fallback): {fallback_error}")
        sys.exit(1)

# =======================
# HELPER FUNCTIONS
# =======================
async def get_bot_info():
    """Get bot information safely"""
    try:
        if not music_bot.bot_info and music_bot.bot:
            music_bot.bot_info = await music_bot.bot.get_me()
        return music_bot.bot_info
    except Exception as e:
        print(f"❌ Error getting bot info: {e}")
        return None

async def get_user_info():
    """Get user information safely"""
    try:
        if not music_bot.user_info and music_bot.user:
            music_bot.user_info = await music_bot.user.get_me()
        return music_bot.user_info
    except Exception as e:
        print(f"❌ Error getting user info: {e}")
        return None

async def join_channel_safely(client: Client, channel: str):
    """Join channel with error handling"""
    try:
        await client.join_chat(channel)
        print(f"✅ Successfully joined: {channel}")
        return True
    except Exception as e:
        print(f"⚠️  Failed to join {channel}: {e}")
        return False

async def auto_join_channels():
    """Auto join configured channels"""
    if not AUTO_JOIN_CHANNELS or not music_bot.user:
        return
    
    print("🔄 Auto-joining channels...")
    for channel in AUTO_JOIN_CHANNELS:
        await join_channel_safely(music_bot.user, channel)
        await asyncio.sleep(2)  # Rate limiting

# =======================
# STARTUP FUNCTIONS
# =======================
async def start_clients():
    """Start all clients safely"""
    try:
        # Start bot client
        if music_bot.bot and not music_bot.bot.is_connected:
            await music_bot.bot.start()
            print("✅ Bot client started")
        
        # Start userbot client
        if music_bot.user and not music_bot.user.is_connected:
            await music_bot.user.start()
            print("✅ Userbot client started")
        
        # Start calls client with error handling
        if music_bot.calls:
            try:
                await music_bot.calls.start()
                print("✅ PyTgCalls client started")
            except Exception as e:
                print(f"⚠️  PyTgCalls start error: {e}")
                # Try to reinitialize calls client
                try:
                    music_bot.calls = PyTgCalls(music_bot.user)
                    await music_bot.calls.start()
                    print("✅ PyTgCalls client reinitialized and started")
                except Exception as reinit_error:
                    print(f"❌ Failed to reinitialize PyTgCalls: {reinit_error}")
                    return False
        
        # Get client info
        bot_info = await get_bot_info()
        user_info = await get_user_info()
        
        if bot_info:
            print(f"🤖 Bot: @{bot_info.username} ({bot_info.first_name})")
        if user_info:
            print(f"👤 Assistant: {user_info.first_name} ({user_info.id})")
        
        # Auto join channels
        await auto_join_channels()
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to start clients: {e}")
        import traceback
        print(f"Full error: {traceback.format_exc()}")
        return False

async def stop_clients():
    """Stop all clients safely"""
    try:
        if music_bot.calls:
            try:
                await music_bot.calls.stop()
                print("✅ PyTgCalls client stopped")
            except Exception as e:
                print(f"⚠️  Error stopping PyTgCalls: {e}")
        
        if music_bot.user and music_bot.user.is_connected:
            try:
                await music_bot.user.stop()
                print("✅ Userbot client stopped")
            except Exception as e:
                print(f"⚠️  Error stopping userbot: {e}")
        
        if music_bot.bot and music_bot.bot.is_connected:
            try:
                await music_bot.bot.stop()
                print("✅ Bot client stopped")
            except Exception as e:
                print(f"⚠️  Error stopping bot: {e}")
            
    except Exception as e:
        print(f"❌ Error stopping clients: {e}")

# =======================
# PYTGCALLS EVENTS (Optional)
# =======================
@calls.on_update()
async def on_calls_update(client: PyTgCalls, update: Update):
    """Handle PyTgCalls updates"""
    pass  # Add your update handlers here

# =======================
# HEALTH CHECK FUNCTIONS
# =======================
async def health_check():
    """Check if all clients are healthy"""
    try:
        bot_ok = music_bot.bot and music_bot.bot.is_connected
        user_ok = music_bot.user and music_bot.user.is_connected
        calls_ok = music_bot.calls and hasattr(music_bot.calls, 'is_connected') and music_bot.calls.is_connected
        
        return {
            "bot": bot_ok,
            "user": user_ok, 
            "calls": calls_ok,
            "overall": all([bot_ok, user_ok, calls_ok])
        }
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return {"overall": False}

async def restart_client(client_name: str):
    """Restart specific client"""
    try:
        if client_name == "bot" and music_bot.bot:
            await music_bot.bot.restart()
        elif client_name == "user" and music_bot.user:
            await music_bot.user.restart()
        elif client_name == "calls" and music_bot.calls:
            # PyTgCalls doesn't have restart method, stop and start instead
            await music_bot.calls.stop()
            await asyncio.sleep(1)
            await music_bot.calls.start()
        
        print(f"✅ {client_name} client restarted")
        return True
    except Exception as e:
        print(f"❌ Failed to restart {client_name}: {e}")
        return False

# =======================
# BACKWARD COMPATIBILITY
# =======================
# For old code compatibility
app = bot  # Alias for old code

# =======================
# EXPORTS
# =======================
__all__ = [
    'bot', 'user', 'calls', 'app',
    'music_bot', 'start_clients', 'stop_clients',
    'health_check', 'restart_client',
    'get_bot_info', 'get_user_info'
]
