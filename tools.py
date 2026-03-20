import os
import io
import sys
from typing import Annotated, List, Optional, Dict
from langchain_core.tools import tool
from langchain_community.document_loaders import WebBaseLoader

# Tools
@tool
def scrape_webpages(urls: List[str]) -> str:
    """Use requests and bs4 to scrape the provided web pages for detailed information."""
    loader = WebBaseLoader(urls)
    docs = loader.load()
    return "\n\n".join(
        [
            f'<Document name={d.metadata.get("title", "")}>\n{d.page_content}\n</Document>'
            for d in docs
        ]
    )

@tool
def create_outline(
    points: Annotated[List[str], "List of main points or sections"],
    file_name: Annotated[str, "File path to save the outline"],
) -> Annotated[str, "Path of the saved outline file"]:
    """Create and save an outline."""
    file_to_use = os.path.join(os.getcwd(), "temp", file_name)
    with open(file_to_use, "w") as file:
        for i, point in enumerate(points):
            file.write(f"{i + 1}. {point}\n")
    return f"Outline saved to {file_name}"

@tool
def read_document(
    file_name: Annotated[str, "File path of the document to read"],
    start: Annotated[Optional[int], "The start line. Default is 0"] = None,
    end: Annotated[Optional[int], "The end line. Default is None"] = None,
):
    """Read the specific document."""
    file_to_use = os.path.join(os.getcwd(), "temp", file_name)
    with open(file_to_use, "r") as file:
        lines = file.readlines()
    if start is None:
        start = 0
    return "\n".join(lines[start:end])

@tool
def write_document(
    content: Annotated[str, "Text content to be written to the document"],
    file_name: Annotated[str, "File path to save the document"],
):
    """Create and save a text document."""
    file_to_use = os.path.join(os.getcwd(), "temp", file_name)
    with open(file_to_use, "w") as file:
        file.write(content)
    return f"Document saved to {file_name}"

@tool
def edit_document(
    file_name: Annotated[str, "File path of the document to edit"],
    inserts: Annotated[
        Dict[int, str],
        "Dictionary where key is the line number and value is the text to be inserted at the line",
    ],
):
    """Edit a document by inserting text at specified line numbers."""
    file_to_use = os.path.join(os.getcwd(), "temp", file_name)
    # BUG FIX: open in "r" mode first to read existing lines, not "w" which truncates
    with open(file_to_use, "r") as file:
        lines = file.readlines()

    sorted_inserts = sorted(inserts.items())

    for line_num, text in sorted_inserts:
        if 1 <= line_num <= len(lines) + 1:
            lines.insert(line_num - 1, text + "\n")
        else:
            return f"Error: Line number {line_num} is out of range"

    with open(file_to_use, "w") as file:
        file.writelines(lines)

    return f"Document edited and saved to {file_name}"

@tool
def python_repl_tool(
    code: Annotated[str, "The python code to execute to generate the chart"],
):
    """Use this to execute python code. If you want to see the output of a value, you should print it with `print(...)`. This is visible to the user."""
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()
    try:
        exec(code, {})
    except BaseException as e:
        sys.stdout = old_stdout
        return f"Error executing code: {e}"
    finally:
        sys.stdout = old_stdout
    result = buffer.getvalue()
    return f"Code executed.\nResult:\n```\n{code}\n```\nStdout: {result}"

