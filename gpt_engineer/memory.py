from langchain.memory import ConversationBufferMemory


class MemoryManager:
    key: str = "chat_history"
    current_step: ConversationBufferMemory
    current_iteration: ConversationBufferMemory

    def __init__(self, key="chat_history"):
        self.key = key
        self.current_step = ConversationBufferMemory(
            memory_key=key, return_messages=True
        )
        self.current_iteration = ConversationBufferMemory(
            memory_key=key, return_messages=True
        )

    def get_step_memory(self) -> ConversationBufferMemory:
        return self.current_step.load_memory_variables({})

    def get_iteration_memory(self) -> ConversationBufferMemory:
        return self.current_iteration.load_memory_variables({})

    def save(self, user_message: object, ai_message: object) -> None:
        self.current_step.save_context({"input": user_message}, {"output": ai_message})
        self.current_iteration.save_context(
            {"input": user_message}, {"output": ai_message}
        )

    def reset_step(self) -> None:
        self.current_step.clear()

    def reset_iteration(self) -> None:
        self.current_iteration.clear()

    def summarize_iteration(self):
        # TODO: add summary
        return "hello world"
