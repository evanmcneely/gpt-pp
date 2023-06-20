from decouple import config


OPENAI_API_KEY = config("OPENAI_API_KEY", default="")
ANTHROPIC_API_KEY = config("ANTHROPIC_API_KEY", default="")


class AnthropicAIModels:
    CLAUDE = "claude-1.3"


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
    CONVERSATION_MODEL = config("CONVERSE_MODEL", default=OpenAIModels.GPT_3_5_TURBO)
