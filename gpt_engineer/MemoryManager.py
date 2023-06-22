from langchain.memory import ConversationBufferMemory


class MemoryManager:
    summary: str
    current_step: ConversationBufferMemory
    current_iteration: ConversationBufferMemory

    def __init__(self):
        self.current_step = ConversationBufferMemory()
        self.current_iteration = ConversationBufferMemory()

    def get_step_memory(self) -> str:
        return self.current_step.load_memory_variables({})["history"]

    def get_iteration_memory(self) -> str:
        return self.current_iteration.load_memory_variables({})["history"]

    def save(self, user_message: str, ai_message: str) -> None:
        self.current_step.save_context({"input": user_message}, {"output": ai_message})
        self.current_iteration.save_context(
            {"input": user_message}, {"output": ai_message}
        )

    def clear_step(self) -> None:
        self.current_step.clear()

    def clear_iteration(self) -> None:
        self.current_iteration.clear()

    def summarize_iteration(self):
        # TODO: add summary
        return "hello world"
