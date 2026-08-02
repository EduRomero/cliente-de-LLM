from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from google import genai
from openai import AsyncOpenAI
from openai import OpenAIError
from google.genai.types import GenerateContentConfig
from google.genai.errors import ClientError
from schemas import (GenerationConfig, ChatMessage, ModelResponse)

class BaseLLMClient(ABC):

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        config: GenerationConfig
    ) -> ModelResponse:
        pass

    @abstractmethod
    async def stream(
        self,
        prompt: str,
        config: GenerationConfig
    ) -> AsyncGenerator[str, None]:
        pass

class GeminiClient(BaseLLMClient):

    def __init__(self, api_key: str):
        self.client = genai.Client(
            api_key=api_key
        )
        self.model = "gemini-3.6-flash"

    async def generate(
        self,
        prompt: str,
        config: GenerationConfig
    ) -> ModelResponse:

        try:

            message = ChatMessage(
                role="user",
                content=prompt
            )

            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=message.content,
                config=GenerateContentConfig(
                    temperature=config.temperature,
                    max_output_tokens=config.max_tokens
                )
            )

            return ModelResponse(
                provider="Gemini",
                model=self.model,
                response=response.text
            )
        
        except ClientError as e:

            return ModelResponse(
                provider="Gemini",
                model=self.model,
                response=f"Error: {str(e)}"
            )

    async def stream(
        self,
        prompt: str,
        config: GenerationConfig
    ) -> AsyncGenerator[str, None]:

        try:

            message = ChatMessage(
                role="user",
                content=prompt
            )

            stream = await self.client.aio.models.generate_content_stream(
                model=self.model,
                contents=message.content,
                config=GenerateContentConfig(
                    temperature=config.temperature,
                    max_output_tokens=config.max_tokens
                )
            )

            async for chunk in stream:

                if chunk.text:
                    yield chunk.text

        except ClientError as e:
            yield f"Error: {str(e)}"


class GroqClient(BaseLLMClient):

    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        self.model = "llama-3.3-70b-versatile"

    async def generate(
        self,
        prompt: str,
        config: GenerationConfig
    ) -> ModelResponse:

        try:

            message = ChatMessage(
                role="user",
                content=prompt
            )

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    message.model_dump()
                ],
                temperature=config.temperature,
                max_tokens=config.max_tokens
            )

            return ModelResponse(
                provider="Groq",
                model=self.model,
                response=response.choices[0].message.content
            )
        
        except OpenAIError as e:

            return ModelResponse(
                provider="Groq",
                model=self.model,
                response=f"Error: {str(e)}"
            )
        
    async def stream(self, prompt: str, config: GenerationConfig) -> AsyncGenerator[str, None]:

        try:
            message = ChatMessage(
                role="user",
                content=prompt
            )

            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=[message.model_dump()],
                stream=True,
                temperature=config.temperature,
                max_tokens=config.max_tokens
            )

            async for chunk in stream:
                if chunk.choices:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        yield delta

        except OpenAIError as e:
            yield f"Error: {str(e)}"