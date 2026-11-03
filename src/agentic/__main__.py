from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.chat_models import (GoogleAPIError,
                                                GoogleRateLimitError)
from langchain_openai import ChatOpenAI
from langchain_openai.chat_models.base import OpenAIRateLimitError
from langchain.agents import create_agent
from dotenv import load_dotenv
import os
import fire
from src.agentic.math_tools import (add_numbers_with_options, add_numbers,
                                    subtract_numbers, multiply_numbers,
                                    divide_numbers)
from src.agentic.wiki_tools import search_wikipedia


load_dotenv()

gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    max_retries=1,
    temperature=0.7
)

backup_llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    model="liquid/lfm-2.5-2.6b:free"
)

local_llm = ChatOpenAI(
    openai_api_key="ollama",
    openai_api_base="http://localhost:11434/v1",
    model="qwen3:0.6b"
)

openrouter_fallback_chain = backup_llm.with_fallbacks(
    [local_llm],
    exceptions_to_handle=tuple([OpenAIRateLimitError])
)

llm = gemini_llm.with_fallbacks(
    [openrouter_fallback_chain],
    exceptions_to_handle=tuple([GoogleAPIError, GoogleRateLimitError])
)

tools = [add_numbers, add_numbers_with_options, subtract_numbers,
         multiply_numbers, divide_numbers, search_wikipedia]

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""
    You are a helpful assistant that can perform various mathematical
    operations and look up information. Use the tools precisely and explain
    your reasoning clearly.
    """
)


def run_agent(query: str) -> None:
    """
    Run the LangChain agent with user query input
    """
    response = agent.invoke({"messages": [("human", query)]})
    print(response["messages"][-1].content)


if __name__ == "__main__":
    fire.Fire(run_agent)
