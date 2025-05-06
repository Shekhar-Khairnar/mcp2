import asyncio
from langchain_groq import ChatGroq

from mcp_use import MCPAgent, MCPClient
import os 
from dotenv import load_dotenv

async def run_memory_chat():
    """ Run a chat using MCPAgent's built in conversation memory"""
    load_dotenv()
    os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')


    config_file = 'server/weather.json'

    print('Initializing chat...')

    client = MCPClient.from_config_file(config_file)
    llm = ChatGroq(model="llama3-8b-8192")

    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        memory_enabled=True,
    )

    print("\n ====Interactive MCP chat ===")
    print(" Type 'exit' or 'quit' to end ther conversation")
    print(" Type 'clear' to clear conversation history")
    print(" ====================== ")

    try:
        #main chat loop
        while True:
            user_input = input("\n You: ")

            # check if exit command
            if user_input.lower( )in ['exit','quit']:
                print('Ending Conv....')
                break

            if user_input.lower() =='clear':
                agent.clear_conversation_history()
                print("conversation history cleared")
                continue

            #get response from agent
            print("\n Assistant: ",end="",flush=True)

            try:
                # run the agent with the user input (memory handling is automatic)
                response = await agent.run(user_input)
                print(response)

            except Exception as e:
                print(f"error: {e}")

    finally:
        # clean up
        if client and client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(run_memory_chat())
