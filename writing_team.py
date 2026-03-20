from typing import Literal
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph
from langgraph.types import Command

from state import State
from llm import llm
from tools import create_outline, read_document, write_document, edit_document, python_repl_tool
from utils import make_supervisor_node


# Document Writer Agent
doc_writer_agent = create_agent(
    llm,
    tools=[write_document, read_document, edit_document],
    system_prompt="You can read, write and edit documents based on note taker's outlines. Don't ask followup questions.",
)


def doc_writer_node(state: State) -> Command[Literal["supervisor"]]:
    result = doc_writer_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=result["messages"][-1].content, name="doc_writer"
                )
            ]
        },
        goto="supervisor",
    )


# Note Taker Agent
note_taker_agent = create_agent(
    llm,
    tools=[create_outline],
    system_prompt="You can read and create outlines for the document writer. Don't ask followup questions.",
)


def note_taker_node(state: State) -> Command[Literal["supervisor"]]:
    result = note_taker_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=result["messages"][-1].content, name="note_taker"
                )
            ]
        },
        goto="supervisor",
    )


# Chart Generator Agent
chart_generator_agent = create_agent(
    llm,
    tools=[read_document, python_repl_tool],
)


def chart_generator_node(state: State) -> Command[Literal["supervisor"]]:
    result = chart_generator_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=result["messages"][-1].content, name="chart_generator"
                )
            ]
        },
        goto="supervisor",
    )


# Supervisor
doc_writer_supervisor_node = make_supervisor_node(
    llm, ["note_taker", "doc_writer", "chart_generator"]
)

# Graph
writing_builder = StateGraph(State)
writing_builder.add_node("supervisor", doc_writer_supervisor_node)
writing_builder.add_node("doc_writer", doc_writer_node)
writing_builder.add_node("note_taker", note_taker_node)
writing_builder.add_node("chart_generator", chart_generator_node)

writing_builder.set_entry_point("supervisor")
writing_graph = writing_builder.compile()

