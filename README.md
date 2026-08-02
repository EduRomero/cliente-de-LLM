# Pre-Entrega 1

Cliente unificado y asíncrono para interactuar con múltiples proveedores de modelos de lenguaje (LLMs) mediante una interfaz común.

Actualmente soporta:

- Gemini (Google AI)
- Groq

## Características

- Arquitectura orientada a interfaces (`BaseLLMClient`)
- Programación asíncrona con `async/await`
- Streaming de respuestas
- Validación de datos con Pydantic
- Patrón Factory para desacoplar proveedores
- Fácil de extender con nuevos modelos

## Estructura del proyecto

```
.
├── clients.py        # Implementaciones de los clientes
├── factory.py        # Factory de proveedores
├── schemas.py        # Modelos Pydantic
├── main.py           # Ejemplo de uso
├── requirements.txt
├── .env
└── README.md
```

## Requisitos

- Python 3.12+
- API Key de Gemini
- API Key de Groq

## Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd pre-entrega1
```

### 2. Crear un entorno virtual

Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Configuración

Crear un archivo `.env`:

```env
GEMINI_API_KEY=tu_api_key
GROQ_API_KEY=tu_api_key
```

## Uso

```python
import asyncio

from factory import LLMFactory, Provider
from schemas import LLMConfig, GenerationConfig

async def main():

    config = LLMConfig()

    generation = GenerationConfig(
        temperature=0.1,
        max_tokens=512
    )

    gemini = LLMFactory.create_client(
        Provider.GEMINI,
        config
    )

    response = await gemini.generate(
        "¿Qué es la entropía?",
        generation
    )

    print(response.response)

asyncio.run(main())
```

## Streaming

```python
async for token in gemini.stream(
    "Explica la entropía",
    generation
):
    print(token, end="")
```

## Arquitectura

```
                 BaseLLMClient
                      ▲
          ┌───────────┴───────────┐
          │                       │
     GeminiClient            GroqClient
          ▲                       ▲
          └───────────┬───────────┘
                      │
                  LLMFactory
                      │
                    main.py
```

## Agregar un nuevo proveedor

1. Crear una clase que herede de `BaseLLMClient`.
2. Implementar `generate()`.
3. Implementar `stream()`.
4. Agregar el proveedor al `Enum Provider`.
5. Actualizar `LLMFactory`.

## Tecnologías

- Python 3.12
- asyncio
- Pydantic
- Google GenAI SDK
- Groq API
