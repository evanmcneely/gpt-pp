import logging

from dotenv import load_dotenv
from decouple import config


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


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
