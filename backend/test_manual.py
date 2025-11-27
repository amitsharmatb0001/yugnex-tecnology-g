"""
FILE: test_manual.py
PATH: yugnex/backend/test_manual.py
PURPOSE: A CLI tool to interact with YugNex agents for testing.
USAGE:
    python test_manual.py
"""

import asyncio
import os
import sys

# Add current directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.connection import AsyncSessionLocal
from agents.registry import AgentRegistry
from memory.conversation import ConversationManager

async def run_test_session():
    print("="*60)
    print("🤖 YUGNEX v1.0 - MANUAL AGENT TEST CONSOLE")
    print("="*60)
    
    # 1. Initialize DB Session
    async with AsyncSessionLocal() as db:
        
        # 2. Select Agent
        print("\nAvailable Agents:")
        print("1. Tilotma (Chief AI Officer)")
        print("2. Advait (Tech Lead)")
        print("3. Saanvi (Analyst)")
        print("4. Shubham (Developer)")
        print("5. Navya (Reviewer)")
        
        choice = input("\nSelect agent (1-5) [Default: 1]: ").strip()
        agent_map = {
            "1": "tilotma", "2": "advait", "3": "saanvi", 
            "4": "shubham", "5": "navya"
        }
        agent_key = agent_map.get(choice, "tilotma")
        
        try:
            agent = AgentRegistry.get_agent(agent_key, db)
            print(f"\n✅ Connected to {agent_key.upper()}.")
        except Exception as e:
            print(f"❌ Error loading agent: {e}")
            return

        # 3. Create a Dummy Conversation
        conv_manager = ConversationManager(db)
        # Assuming user_id=1 exists (if not, script might fail on FK, ensure DB has a user)
        # For testing, we just simulate the flow without saving if strict FK is an issue,
        # but BaseAgent expects DB.
        
        print("\nType your message (or 'exit' to quit):")
        print("-" * 60)

        while True:
            user_input = input(f"\nYou > ")
            if user_input.lower() in ["exit", "quit"]:
                break
            
            print(f"\n{agent_key.title()} is thinking...", end="", flush=True)
            
            try:
                # Run the agent
                response = await agent.run(user_input=user_input)
                print(f"\r{agent_key.title()} > {response}")
                
            except Exception as e:
                print(f"\n❌ Error: {e}")
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    try:
        asyncio.run(run_test_session())
    except KeyboardInterrupt:
        print("\nSession ended.")