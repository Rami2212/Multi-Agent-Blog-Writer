from typing import Literal
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph
from langgraph.types import Command

from state import State
from llm import llm
from utils import make_supervisor_node
from research_team import research_graph
from writing_team import writing_graph


teams_supervisor_node = make_supervisor_node(llm, ["research", "writing"])


def call_research_team(state: State) -> Command[Literal["supervisor"]]:
    response = research_graph.invoke({"messages": state["messages"][-1]})
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=response["messages"][-1].content, name="research"
                )
            ]
        },
        goto="supervisor",
    )


def call_writing_team(state: State) -> Command[Literal["supervisor"]]:
    response = writing_graph.invoke({"messages": state["messages"][-1]})
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=response["messages"][-1].content, name="writing"
                )
            ]
        },
        goto="supervisor",
    )


super_builder = StateGraph(State)
super_builder.add_node("supervisor", teams_supervisor_node)
super_builder.add_node("research", call_research_team)
super_builder.add_node("writing", call_writing_team)

super_builder.set_entry_point("supervisor")
super_graph = super_builder.compile()

