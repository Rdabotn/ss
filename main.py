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
            
            # Start all clients with error handling
            if not await start_clients():
                LOGS.error("❌ Failed to start clients")
                return False
            
            # Health check with timeout
            try:
                health = await asyncio.wait_for(health_check(), timeout=30)
                if not health.get("overall", False):
                    LOGS.error("❌ Health check failed")
                    return False
            except asyncio.TimeoutError:
                LOGS.warning("⚠️  Health check timeout, proceeding anyway...")
            except Exception as e:
                LOGS.warning(f"⚠️  Health check error: {e}, proceeding anyway...")
            
            LOGS.info("✅ All systems operational!")
            LOGS.info(f"🎵 {music_bot.bot_info.first_name if hasattr(music_bot, 'bot_info') and music_bot.bot_info else 'Music Bot'} is ready!")
            
            self.running = True
            return True
            
        except Exception as e:
            LOGS.error(f"❌ Startup failed: {e}")
            import traceback
            LOGS.error(f"Full error: {traceback.format_exc()}")
            return False
    
    async def shutdown(self):
        """Gracefully shutdown the bot"""
        try:
            if not self.running:
                return
            
            LOGS.info("🔄 Shutting down Music Bot...")
            self.running = False
            
            # Stop all clients with timeout
            try:
                await asyncio.wait_for(stop_clients(), timeout=10)
            except asyncio.TimeoutError:
                LOGS.warning("⚠️  Client shutdown timeout")
            except Exception as e:
                LOGS.error(f"❌ Error stopping clients: {e}")
            
            # Cancel all running tasks
            tasks = [task for task in asyncio.all_tasks() if not task.done() and task != asyncio.current_task()]
            for task in tasks:
                task.cancel()
            
            if tasks:
                LOGS.info(f"⏳ Waiting for {len(tasks)} tasks to complete...")
                try:
                    await asyncio.wait_for(
                        asyncio.gather(*tasks, return_exceptions=True),
                        timeout=5
                    )
                except asyncio.TimeoutError:
                    LOGS.warning("⚠️  Some tasks didn't complete in time")
            
            LOGS.info("✅ Shutdown complete")
            
        except Exception as e:
            LOGS.error(f"❌ Shutdown error: {e}")
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        if platform.system() != "Windows":
            try:
                for sig in (signal.SIGTERM, signal.SIGINT):
                    signal.signal(sig, lambda s, f: asyncio.create_task(self.handle_shutdown()))
            except Exception as e:
                LOGS.warning(f"⚠️  Failed to setup signal handlers: {e}")
    
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
                
                # Health check with error handling
                if self.running:
                    try:
                        health = await asyncio.wait_for(health_check(), timeout=10)
                        if not health.get("overall", False):
                            LOGS.warning("⚠️  Health check failed, system may be unstable")
                    except Exception as e:
                        LOGS.warning(f"⚠️  Health monitoring error: {e}")
                
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
            idle(),  # PyTgCalls idle
            return_exceptions=True
        )
        
    except KeyboardInterrupt:
        LOGS.info("🛑 Received keyboard interrupt")
    except Exception as e:
        LOGS.error(f"❌ Unexpected error: {e}")
        import traceback
        LOGS.error(f"Full traceback: {traceback.format_exc()}")
        return 1
    finally:
        # Graceful shutdown
        await bot_manager.shutdown()
    
    return 0

# Alternative simple main function (for compatibility)
async def simple_main():
    """Simple main function with better error handling"""
    try:
        LOGS.info("🚀 Starting Music Bot (Simple Mode)...")
        
        # Start clients with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if await start_clients():
                    break
                else:
                    if attempt < max_retries - 1:
                        LOGS.warning(f"⚠️  Startup attempt {attempt + 1} failed, retrying...")
                        await asyncio.sleep(5)
                    else:
                        LOGS.error("❌ Failed to start clients after all retries")
                        return
            except Exception as e:
                LOGS.error(f"❌ Startup error (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(5)
                else:
                    return
        
        LOGS.info("✅ Bot started successfully!")
        
        # Keep alive with error handling
        try:
            await idle()
        except Exception as e:
            LOGS.error(f"❌ Idle error: {e}")
        
    except KeyboardInterrupt:
        LOGS.info("🛑 Received keyboard interrupt")
    except Exception as e:
        LOGS.error(f"❌ Error: {e}")
        import traceback
        LOGS.error(f"Full traceback: {traceback.format_exc()}")
    finally:
        LOGS.info("🔄 Stopping bot...")
        try:
            await stop_clients()
        except Exception as e:
            LOGS.error(f"❌ Error during shutdown: {e}")

if __name__ == "__main__":
    # Choose which main function to use
    USE_ADVANCED_MODE = False  # Changed to False for better compatibility
    
    if USE_ADVANCED_MODE:
        # Advanced mode with monitoring and graceful shutdown
        try:
            exit_code = asyncio.run(main())
            sys.exit(exit_code)
        except Exception as e:
            print(f"❌ Critical error: {e}")
            sys.exit(1)
    else:
        # Simple mode (recommended for troubleshooting)
        try:
            asyncio.run(simple_main())
        except Exception as e:
            print(f"❌ Critical error: {e}")
            sys.exit(1)
