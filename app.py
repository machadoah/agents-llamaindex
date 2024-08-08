import subprocess

import requests
from dotenv import load_dotenv
from llama_index.llms.groq import Groq
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool
from fastapi import FastAPI

load_dotenv()

app = FastAPI()

llm = Groq(model="llama-3.1-70b-versatile", temperature=0)


def open_url(url: str) -> str:
    """
    Opens a url in browser chrome

    :param url:
    :return:
    """

    try:
        subprocess.Popen(["xdg-open", url])
        return "successfully open url"
    except Exception as e:
        print(e)


def open_application(application_name: str) -> str:
    """
    Opens an application in my computer

    :param application_name: name of application

    :return: succesfully opened application or failed
    """

    try:
        subprocess.Popen([application_name])
        return "successfully opened " + application_name
    except Exception as e:
        return f"Error: {str(e)}"


def creator_aplication(application_name: str) -> str:
    return llm.complete(
        f"quem criou a aplicação ou biblioteca chamada={application_name}"
    )


def welcome_httpie() -> str:
    data = requests.get(url="https://httpie.io/Hello")
    response = data.json()

    return response


def write_haiku(topic: str) -> str:
    return llm.complete(f"escreva um Haicai sobre {topic}")


def count_characters(text: str) -> int:
    return len(text)


if __name__ == "__main__":
    print("*** Hello Agents LlamaIndex ***", end="\n\n")

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

    tool4 = FunctionTool.from_defaults(
        fn=creator_aplication,
        name="adivinhando_creador",
        description="Vê quem desenvolvou dado aplicativo ou framework",
    )

    tool5 = FunctionTool.from_defaults(
        fn=open_application,
        name="open_application",
        description="Open a application in Operating System",
    )

    tool6 = FunctionTool.from_defaults(
        fn=open_url, name="open_url", description="Open a url in chrome browser"
    )

    agent = ReActAgent.from_tools(
        tools=[tool1, tool2, tool3, tool4, tool5, tool6], llm=llm, verbose=True
    )

    # resposta = agent.query('Abra o site https://github.com/machadoah/agents-llamaindex no chrome!')
    # resposta = agent.query('Abra o aplicativo local vscode em meu computador!')
    try:
        resposta = agent.query(
            "Crie um haiku sobre python e abra o aplicativo da minha maquina vscode"
        )
        print(resposta)
    except Exception as e:
        print("🤖: CARACA!\nVocê me fez pensar demais!")

