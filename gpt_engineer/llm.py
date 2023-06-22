from langchain.chat_models import ChatOpenAI, ChatAnthropic

from config import OpenAIModels, AnthropicAIModels, OPENAI_API_KEY, ANTHROPIC_API_KEY

def _get_openai(model: str, **kwargs):
    return ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0, model_name=model, **kwargs)


def _get_anthropic(model: str, **kwargs):
    return ChatAnthropic(anthropic_api_key=ANTHROPIC_API_KEY, temperature=0, model=model, **kwargs)


def get_llm(model: str, **kwargs):
    match model:
        case OpenAIModels.GPT_3_5_TURBO:
            return _get_openai(model, **kwargs)
        case OpenAIModels.GPT_3_5_TURBO_16K:
            return _get_openai(model, **kwargs)
        case OpenAIModels.GPT_4:
            return _get_openai(model, **kwargs)
        case OpenAIModels.GPT_4_32k:
            return _get_openai(model, **kwargs)
        case AnthropicAIModels.CLAUDE:
            return _get_anthropic(model, **kwargs)

    raise ValueError(f"Invalid model: {model}")
