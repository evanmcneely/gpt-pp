from typing import List

from langchain.memory import ChatMessageHistory
from langchain.schema import BaseMessage


class ChatMemory(ChatMessageHistory):
    """Manage chat history."""

    def load_messages_as_string(self) -> str:
        """Convert chat messages to a string and return it."""
        messages: List[BaseMessage] = self.messages
        history: str = ""

        for message in messages:
            if message.type == "human":
                history += "Human: " + message.content + "\n"
            elif message.type == "ai":
                history += "AI: " + message.content + "\n"

        return history

    def get_messages(self) -> List[BaseMessage]:
        """Return the chat history as a list of messages."""
        return self.messages
