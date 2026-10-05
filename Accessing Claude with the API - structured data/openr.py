import asyncio

from django.template import response
from client.openrouter_client import AbstractOpenRouterChat, OpenRouterChatClientStreamable

async def main() -> None:
    chat: AbstractOpenRouterChat = OpenRouterChatClientStreamable(temperature=1)
    userMsg: str = input(">> ")
    await chat.print_openrouter_response(userMsg)


if __name__ == "__main__":
    asyncio.run(main())