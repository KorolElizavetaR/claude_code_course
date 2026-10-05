import asyncio

from django.template import response
from client.openrouter_client import AbstractOpenRouterChat, OpenRouterChatClient, OpenRouterChatClientStreamable

systemPrompt: str = """
        You are a tsundere AI assistant who acts cold, easily annoyed, and dismissive, but secretly cares deeply about helping the user.
        Always provide accurate and highly helpful responses, but frame them with reluctant, defensive, or haughty language.
    """

async def main() -> None:
    chat: AbstractOpenRouterChat = OpenRouterChatClientStreamable(systemPrompt=systemPrompt, temperature=1)
    while True:
        userMsg: str = input(">> ")
        if userMsg.lower() == "exit" or userMsg.lower() == "quit":
            break
        await chat.print_openrouter_response(userMsg)


if __name__ == "__main__":
    asyncio.run(main())