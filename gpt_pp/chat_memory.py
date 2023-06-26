from typing import List

from langchain.memory import ChatMessageHistory
from langchain.schema import BaseMessage


class ChatMemory(ChatMessageHistory):
    def load_messages(self):
        messages: List[BaseMessage] = self.messages
        history: str = ""

        for message in messages:
            if message.type == "human":
                history += "Human: " + message.content + "\n"
            elif message.type == "ai":
                history += "AI: " + message.content + "\n"

        return history