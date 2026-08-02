from clients import GeminiClient, GroqClient, BaseLLMClient
from schemas import LLMConfig
from enum import Enum


class Provider(str, Enum):
    GEMINI = "gemini"
    GROQ = "groq"

class LLMFactory:

    @staticmethod
    def create_client(
        provider: Provider,
        config: LLMConfig
    ) -> BaseLLMClient:

        if provider == Provider.GEMINI:
            return GeminiClient(
                config.gemini_api_key.get_secret_value()
            )
        elif provider == Provider.GROQ:
            return GroqClient(
                config.groq_api_key.get_secret_value()
            )

        else:
            raise ValueError(
                f"Proveedor no soportado: {provider}"
            )

class AsyncLLMManager:

    def __init__(
        self,
        client: BaseLLMClient
    ):
        self.client = client

    async def generate(
        self,
        prompt: str
    ):
        return await self.client.generate(prompt)

    async def stream(
        self,
        prompt: str
    ):
        async for token in self.client.stream(prompt):
            yield token        