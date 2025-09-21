import asyncio
from pyrogram import Client

async def generate_session():
    print("🔑 Session String Generator")
    print("=" * 40)
    
    api_id = input("Enter your API_ID: ")
    api_hash = input("Enter your API_HASH: ")
    
    try:
        api_id = int(api_id)
    except ValueError:
        print("❌ API_ID must be a number!")
        return
    
    if not api_hash.strip():
        print("❌ API_HASH cannot be empty!")
        return
    
    try:
        async with Client(
            name="session_generator",
            api_id=api_id,
            api_hash=api_hash,
            in_memory=True
        ) as client:
            session_string = await client.export_session_string()
            
            print("\n✅ Session String Generated Successfully!")
            print("=" * 50)
            print("SESSION_STRING =", session_string)
            print("=" * 50)
            print("\n📋 Copy this session string to your .env file")
            
    except Exception as e:
        print(f"❌ Error generating session: {e}")

if __name__ == "__main__":
    asyncio.run(generate_session())
