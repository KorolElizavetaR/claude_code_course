
from abc import ABC, abstractmethod

from openrouter import OpenRouter
import os

from openrouter import components

from dotenv import load_dotenv

from enum import Enum

class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

DEFAULT_SYSTEM_PROMPT : str = """
        Generate json based on user's suggestion
    """

class AbstractOpenRouterChat(ABC):
    
    def __init__(self, systemPrompt: str = DEFAULT_SYSTEM_PROMPT, temperature: float = 0.5):
        load_dotenv()
        self.api_key: str = os.getenv("OPENROUTER_API_KEY")
        self.model: str = os.getenv("MODEL")
        self.messages: list[dict] = []
        self.temperature: float = temperature
        self.add_message(Role.SYSTEM, systemPrompt if systemPrompt else self.systemPrompt)
        self.client: OpenRouter = OpenRouter(self.api_key)
    
    @abstractmethod
    def _openrouter_response(self)-> components.ChatResult:
        ...
        
    @abstractmethod
    def print_openrouter_response(self, userMsg) -> None:
        ...

    def add_message(self, role: Role, text):
        message: dict = {"role": role.value, "content": text}
        self.messages.append(message)

    def add_user_message(self, text):
        self.add_message(Role.USER, text)

    def add_assistant_message(self, text):
        self.add_message(Role.ASSISTANT, text)

class OpenRouterChatClientStreamable(AbstractOpenRouterChat):
    async def _openrouter_response(self)-> components.ChatResult:
        return await self.client.chat.send_async(
                model=self.model,
                max_tokens=2000,
                messages=self.messages,
                temperature=self.temperature,
                stream=True
            )
    
    async def print_openrouter_response(self, userMsg) -> None:
        self.add_user_message(userMsg)
        print("\n>> ", end="")
        self.add_assistant_message("```")
        streamable_response = await self._openrouter_response()
        parts: list[str] = []
        async with streamable_response as stream:
            async for chunk in stream:
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if delta.content:
                        parts.append(delta.content)
                        print(delta.content, end="", flush=True)
        agentMsg = "".join(parts)
        print()
        self.add_assistant_message(agentMsg)
