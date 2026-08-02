from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class ChatMessage(BaseModel):
    role: str = Field(
        description="Rol del mensaje (user, assistant o system)"
    )
    content: str = Field(
        min_length=1,
        description="Contenido del mensaje"
    )


class ModelResponse(BaseModel):
    provider: str
    model: str
    response: str


class GenerationConfig(BaseModel):
    temperature: float = Field(
        default=0.7,
        ge=0,
        le=2
    )

    max_tokens: int = Field(
        default=512,
        gt=0
    )


class LLMConfig(BaseSettings):
    gemini_api_key: SecretStr
    groq_api_key: SecretStr

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

