import os

from decouple import config

OPENAI_API_KEY = config("OPENAI_API_KEY", default="")
ANTHROPIC_API_KEY = config("ANTHROPIC_API_KEY", default="")
VERBOSE = config("VERBOSE", default=False, cast=bool)
LANGCHAIN_TRACING = config("LANGCHAIN_TRACING", default="false")
GITHUB_ACCESS_TOKEN = config("GITHUB_ACCESS_TOKEN", default="")

os.environ.setdefault("LANGCHAIN_TRACING", LANGCHAIN_TRACING)


class AnthropicAIModels:
    CLAUDE_1_3_100k = "claude-1.3-100k"
    CLAUDE_1_3 = "claude-1.3"


class OpenAIModels:
    GPT_3_5_TURBO_16K = "gpt-3.5-turbo-16k"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"
    GPT_4_32k = "gpt-4-32k"


class Models:
    CODE_MODEL = config("CODE_MODEL", default=OpenAIModels.GPT_3_5_TURBO_16K)
    INTERPRETATION_MODEL = config(
        "INTERPRETATION_MODEL", default=OpenAIModels.GPT_3_5_TURBO_16K
    )
    CONVERSATION_MODEL = config("CHAT_MODEL", default=OpenAIModels.GPT_3_5_TURBO)
