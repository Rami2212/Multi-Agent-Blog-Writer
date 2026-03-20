from typing import TypedDict, List, Literal
from langchain_core.language_models import BaseChatModel
from langgraph.types import Command
from langgraph.graph import END

from state import State

def make_supervisor_node(llm: BaseChatModel, members: List[str]):
    options = ["FINISH"] + members
    system_prompt = (
        f"You are a supervisor agent tasked with managing a conversation between the "
        f"following workers: {members}. Given the following user requests, respond with "
        f"the worker to act next. Each worker will perform a task and respond with their "
        f"results and status. When finished, respond with FINISH."
    )

    class Router(TypedDict):
        next: str

    def supervisor(state: State) -> Command:
        messages = [
            {"role": "system", "content": system_prompt}
        ] + state["messages"]

        response = llm.with_structured_output(Router).invoke(messages)
        goto = response["next"]
        if goto == "FINISH":
            goto = END

        return Command(goto=goto, update={"next": goto})

    return supervisor

