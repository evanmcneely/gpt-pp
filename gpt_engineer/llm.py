from langchain.chat_models import ChatOpenAI, ChatAnthropic

from config import OpenAIModels, AnthropicAIModels, OPENAI_API_KEY, ANTHROPIC_API_KEY

def _get_openai(model: str):
    return ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0, model_name=model)


def _get_anthropic(model: str):
    return ChatAnthropic(anthropicai_api_key=ANTHROPIC_API_KEY, temperature=0, model=model)


def get_llm(model: str):
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
