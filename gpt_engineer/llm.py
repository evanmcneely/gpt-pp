from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI, ChatAnthropic

from config import OpenAIModels, AnthropicAIModels


def _get_callbacks():
    return [StreamingStdOutCallbackHandler()]


def _get_openai(model):
    return ChatOpenAI(stream=True, temperature=0, model_name=model, callbacks=_get_callbacks())

def _get_anthropic(model):
    return ChatAnthropic(stream=True, temperature=0, model=model, callbacks=_get_callbacks())


def get_llm(model):
    match model:
        case OpenAIModels.GPT_3_5_TURBO:
            return _get_openai(model)
        case OpenAIModels.GPT_3_5_TURBO_16K:
            return _get_openai(model)
        case OpenAIModels.GPT_4:
            return _get_openai(model)
        case OpenAIModels.GPT_4_32k:
            return _get_openai(model)
        case AnthropicAIModels.CLAUDE:
            return _get_anthropic(model)

    raise ValueError(f"Invalid model: {model}")
