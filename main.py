import asyncio
import os

from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

async def main():

    model = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0.2,
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Sos un profesor experto en física que responde de forma clara y breve."
            ),
            (
                "human",
                "{pregunta}"
            )
        ]
    )

    parser = StrOutputParser()

    chain = prompt | model | parser

    respuesta = await chain.ainvoke(
        {
            "pregunta": "¿Qué es la entropía?"
        }
    )

    print(respuesta)

if __name__ == "__main__":
    asyncio.run(main())