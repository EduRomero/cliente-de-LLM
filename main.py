import asyncio

from dotenv import load_dotenv
from factory import LLMFactory, Provider
from schemas import LLMConfig, GenerationConfig

load_dotenv()

async def main():

    config = LLMConfig()

    generation_config = GenerationConfig(
        temperature=0.1,
        max_tokens=2000
    )

    clients = [
        ("Gemini", LLMFactory.create_client(Provider.GEMINI, config)),
        ("Groq", LLMFactory.create_client(Provider.GROQ, config)),
    ]

    for name, client in clients:

        print(f"\n{'=' * 20} {name} {'=' * 20}")

        print("\nRespuesta completa:\n")

        response = await client.generate("¿Qué es la entropía?", generation_config)

        print(response.response)

        print("\n\nStreaming:\n")

        async for token in client.stream("¿Qué es la entropía?", generation_config):
            print(token, end="", flush=True)

        print("\n")
    
if __name__ == "__main__":
    asyncio.run(main())