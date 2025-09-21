import asyncio
import platform
import signal
import sys
from contextlib import asynccontextmanager

# Try to use uvloop for better performance on Linux
if platform.system() != "Windows":
    try:
        import uvloop
        uvloop.install()
        print("✅ Using uvloop for better performance")
    except ImportError:
        print("⚠️  uvloop not available, using default event loop")

from program import LOGS
from pytgcalls import idle
from driver.core import start_clients, stop_clients, health_check, music_bot

class MusicBotManager:
    """Music bot manager with advanced features"""
    
    def __init__(self):
        self.running = False
        self.shutdown_event = asyncio.Event()
    
    async def startup(self):
        """Initialize and start the bot"""
        try:
            LOGS.info("🚀 Starting Music Bot...")
            
            # Start all clients
            if not await start_clients():
                LOGS.error("❌ Failed to start clients")
                return False
            
            # Health check
            health = await health_check()
            if not health.get("overall", False):
                LOGS.error("❌ Health check failed")
                return False
            
            LOGS.info("✅ All systems operational!")
            LOGS.info(f"🎵 {music_bot.bot_info.first_name if music_bot.bot_info else 'Music Bot'} is ready!")
            
            self.running = True
            return True
            
        except Exception as e:
            LOGS.error(f"❌ Startup failed: {e}")
            return False
    
    async def shutdown(self):
        """Gracefully shutdown the bot"""
        try:
            if not self.running:
                return
            
            LOGS.info("🔄 Shutting down Music Bot...")
            self.running = False
            
            # Stop all clients
            await stop_clients()
            
            # Cancel all running tasks
            tasks = [task for task in asyncio.all_tasks() if not task.done()]
            for task in tasks:
                task.cancel()
            
            if tasks:
                LOGS.info(f"⏳ Waiting for {len(tasks)} tasks to complete...")
                await asyncio.gather(*tasks, return_exceptions=True)
            
            LOGS.info("✅ Shutdown complete")
            
        except Exception as e:
            LOGS.error(f"❌ Shutdown error: {e}")
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        if platform.system() != "Windows":
            for sig in (signal.SIGTERM, signal.SIGINT):
                signal.signal(sig, lambda s, f: asyncio.create_task(self.handle_shutdown()))
    
    async def handle_shutdown(self):
        """Handle shutdown signal"""
        LOGS.info("🛑 Shutdown signal received")
        self.shutdown_event.set()
    
    async def run_with_monitoring(self):
        """Run bot with health monitoring"""
        monitor_interval = 300  # 5 minutes
        
        while self.running:
            try:
                # Wait for shutdown signal or monitor interval
                try:
                    await asyncio.wait_for(
                        self.shutdown_event.wait(), 
                        timeout=monitor_interval
                    )
                    break  # Shutdown requested
                except asyncio.TimeoutError:
                    pass  # Normal monitoring cycle
                
                # Health check
                if self.running:
                    health = await health_check()
                    if not health.get("overall", False):
                        LOGS.warning("⚠️  Health check failed, attempting recovery...")
                        # Add recovery logic here if needed
                
            except Exception as e:
                LOGS.error(f"❌ Monitoring error: {e}")
                await asyncio.sleep(30)  # Wait before retry

async def main():
    """Main application entry point"""
    bot_manager = MusicBotManager()
    
    try:
        # Setup signal handlers
        bot_manager.setup_signal_handlers()
        
        # Start the bot
        if not await bot_manager.startup():
            LOGS.error("❌ Failed to start the bot")
            return 1
        
        # Run with monitoring and idle
        await asyncio.gather(
            bot_manager.run_with_monitoring(),
            idle()  # PyTgCalls idle
        )
        
    except KeyboardInterrupt:
        LOGS.info("🛑 Received keyboard interrupt")
    except Exception as e:
        LOGS.error(f"❌ Unexpected error: {e}")
        return 1
    finally:
        # Graceful shutdown
        await bot_manager.shutdown()
    
    return 0

# Alternative simple main function (for compatibility)
async def simple_main():
    """Simple main function similar to original"""
    try:
        LOGS.info("🚀 Starting Music Bot (Simple Mode)...")
        
        # Start clients
        if not await start_clients():
            LOGS.error("❌ Failed to start clients")
            return
        
        LOGS.info("✅ Bot started successfully!")
        
        # Keep alive
        await idle()
        
    except KeyboardInterrupt:
        LOGS.info("🛑 Received keyboard interrupt")
    except Exception as e:
        LOGS.error(f"❌ Error: {e}")
    finally:
        LOGS.info("🔄 Stopping bot...")
        await stop_clients()

if __name__ == "__main__":
    # Choose which main function to use
    USE_ADVANCED_MODE = True
    
    if USE_ADVANCED_MODE:
        # Advanced mode with monitoring and graceful shutdown
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    else:
        # Simple mode (similar to original)
        asyncio.run(simple_main())
