from langchain.chat_models import ChatAnthropic, ChatOpenAI

from config import (ANTHROPIC_API_KEY, OPENAI_API_KEY, AnthropicAIModels,
                    OpenAIModels)


def _get_openai(model: str, **kwargs):
    """Return an instance of ChatOpenAI configured with the passed in
    keyword arguments.
    """
    return ChatOpenAI(
        openai_api_key=OPENAI_API_KEY, temperature=0, model_name=model, **kwargs
    )


def _get_anthropic(model: str, **kwargs):
    """Return an instance of ChatAnthropic configured with the passed in
    keyword arguments.
    """
    return ChatAnthropic(
        anthropic_api_key=ANTHROPIC_API_KEY, temperature=0, model=model, **kwargs
    )


def get_llm(model: str, **kwargs):
    """Return a language configured model instance for the passed in model name."""
    match model:
        case OpenAIModels.GPT_3_5_TURBO:
            return _get_openai(model, **kwargs)
        case OpenAIModels.GPT_3_5_TURBO_16K:
            return _get_openai(model, **kwargs)
        case OpenAIModels.GPT_4:
            return _get_openai(model, **kwargs)
        case OpenAIModels.GPT_4_32k:
            return _get_openai(model, **kwargs)
        case AnthropicAIModels.CLAUDE_1_3_100k:
            return _get_anthropic(model, **kwargs)
        case AnthropicAIModels.CLAUDE_1_3:
            return _get_anthropic(model, **kwargs)

    raise ValueError(f"Invalid model: {model}")
