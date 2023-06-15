from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI

from config import MODEL


def _get_callbacks():
    return [StreamingStdOutCallbackHandler()]


def _get_openai():
    return ChatOpenAI(temperature=0, model_name=MODEL, callbacks=_get_callbacks())


def get_llm():
    return _get_openai()
