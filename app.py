import requests
from dotenv import load_dotenv
from llama_index.llms.groq import Groq
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool
from fastapi import FastAPI

load_dotenv()

app = FastAPI()

llm = Groq(model="llama-3.1-70b-versatile", temperature=0)


def welcome_httpie() -> str:
    data = requests.get(url='https://httpie.io/Hello')
    response = data.json()

    return response


def write_haiku(topic: str) -> str:
    return llm.complete(f"escreva um Haicai sobre {topic}")


def count_characters(text: str) -> int:
    return len(text)


if __name__ == "__main__":
    print("*** Hello Agents LlamaIndex ***", end='\n\n')

    tool1 = FunctionTool.from_defaults(
        fn=write_haiku,
        name="write_haiku",
        description="Useful to write a haiku about a given topic",
    )
    tool2 = FunctionTool.from_defaults(
        fn=count_characters,
        name="count_characters",
        description="Useful to count the number of characters in a text",
    )
    tool3 = FunctionTool.from_defaults(
        fn=welcome_httpie,
        name="bem_vindo_httpie",
        description="Faz um get para o endpoint do httpie",
    )

    agent = ReActAgent.from_tools(
        tools=[tool1, tool2, tool3],
        llm=llm,
        verbose=True
    )

    resposta = agent.query('Escreva para mim um haicai sobre olimpiadas e conte a quantidade de caracteres nele ')
    print(resposta)

    resposta = agent.query('Qual a mensagem de bem vinda do serviço httpie?')
    print(resposta)
