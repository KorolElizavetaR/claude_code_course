
from abc import ABC, abstractmethod
from uuid import UUID
import uuid

from openrouter import OpenRouter
import os

from openrouter import components

from dotenv import load_dotenv

from enum import Enum

class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

load_dotenv()
api_key: str = os.getenv("OPENROUTER_API_KEY")
model: str = os.getenv("MODEL")


class AbstractOpenRouterChat(ABC):
    
    def __init__(self, systemPrompt: str = None, temperature: float = 0.5):
        self.messages: list[dict] = []
        self.temperature: float = temperature
        if systemPrompt is not None:
            self.add_message(Role.SYSTEM, systemPrompt)
        self.client: OpenRouter = OpenRouter(api_key)
        self.chat_id: UUID = uuid.uuid4()
        
    @abstractmethod
    def _openrouter_response(self)-> components.ChatResult:
        ...

    @abstractmethod
    async def get_openrouter_text_response(self, userMsg) -> str:
        ...
        
    @abstractmethod
    async def print_openrouter_response(self, userMsg) -> None:
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
                model=model,
                max_tokens=2000,
                messages=self.messages,
                temperature=self.temperature,
                stream=True
            )
    
    async def print_openrouter_response(self, userMsg) -> None:
        self.add_user_message(userMsg)
        print("\n>> ", end="")
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

class OpenRouterChatClient(AbstractOpenRouterChat):
    def _openrouter_response(self)-> components.ChatResult:
            return self.client.chat.send(
                        model=model,
                        max_tokens=2000,
                        messages=self.messages,
                        temperature=self.temperature
                )
            
    def print_openrouter_response(self, userMsg) -> None:
        """
        Takes a result of @get_openrouter_text_response and prints it out
        """
        text = self.get_openrouter_text_response(userMsg=userMsg)
        print("\n>> ", end="")
        print(text) 

    def get_openrouter_text_response(self, userMsg) -> str:
        self.add_user_message(userMsg)
        response = self._openrouter_response()
        responseStr = response.choices[0].message.content
        self.add_assistant_message(responseStr)
        return responseStr