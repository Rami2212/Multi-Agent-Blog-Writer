from typing import Literal
from langchain_core.messages import HumanMessage
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langgraph.graph import StateGraph
from langgraph.types import Command

from state import State
from llm import llm
from tools import scrape_webpages
from utils import make_supervisor_node

# Tools
tavily_tool = TavilySearch(max_results=3)

# Search Agent
search_agent = create_agent(llm, tools=[tavily_tool])


def search_node(state: State) -> Command[Literal["supervisor"]]:
    result = search_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=result["messages"][-1].content, name="search"
                )
            ]
        },
        goto="supervisor",
    )

# Web Scraping Agent
web_scraping_agent = create_agent(llm, tools=[scrape_webpages])


def web_scraper_node(state: State) -> Command[Literal["supervisor"]]:
    result = web_scraping_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=result["messages"][-1].content, name="web_scraper"
                )
            ]
        },
        goto="supervisor",
    )

# Supervisor
research_supervisor_node = make_supervisor_node(llm, ["search", "web_scraper"])

# Graph
research_builder = StateGraph(State)
research_builder.add_node("supervisor", research_supervisor_node)
research_builder.add_node("search", search_node)
research_builder.add_node("web_scraper", web_scraper_node)

research_builder.set_entry_point("supervisor")
research_graph = research_builder.compile()

