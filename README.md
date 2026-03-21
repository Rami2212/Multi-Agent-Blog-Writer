# Multi-Agent Blog Writer

This project is an advanced **Multi-Agent System** that automates the process of researching and writing high-quality blog posts. By leveraging **LangGraph** for orchestration and **Google Gemini** as the underlying LLM, it coordinates a team of specialized AI agents to handle everything from initial research to the final draft, all accessible through a clean **Streamlit** interface.

## Features

- **Automated Research**: Uses a dedicated Research Team to search the web and scrape detailed information on the given topic.
- **Structured Writing**: A Writing Team collaborates to first outline the post, then write the content section by section.
- **Chart Generation**: Includes a data visualization agent capable of writing Python code to generate charts and graphs to support the content.
- **Interactive UI**: A Streamlit dashboard to input topics, view real-time agent progress, and download the final blog post.
- **File Management**: Automatically saves outlines and drafts to a local `temp/` directory.

## Agent Architecture

The system is built on a hierarchical agent graph managed by a Supervisor:

### 1. **Supervisor Agent**
   - Orchestrates the workflow between the Research and Writing teams.
   - Decides which team should act next based on the current state and conversation history.

### 2. **Research Team**
   - **Search Agent**: queries the web for relevant information using the Tavily Search API.
   - **Web Scraper Agent**: extracting content from specific URLs to provide in-depth context.

### 3. **Writing Team**
   - **Note Taker**: Synthesizes research into a structured outline.
   - **Document Writer**: Drafts the full blog post based on the outline and research notes. It manages file creation and editing.
   - **Chart Generator**: Creates visual data representations (charts/graphs) using a Python REPL environment if the topic requires data visualization.

## Tech Stack

- **Python 3.12+**
- **LangChain & LangGraph**: For building stateful, multi-agent workflows.
- **Google Gemini (via `langchain-google-genai`)**: The primary LLM used for reasoning and generation.
- **Tavily API**: For high-quality search results optimized for LLMs.
- **Streamlit**: For the web-based user interface.
- **BeautifulSoup4**: For web scraping.

## Prerequisites

Before running the application, ensure you have the following API keys:

1.  **Google AI Studio API Key**: For accessing Gemini models.
2.  **Tavily API Key**: For web search capabilities.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Rami2212/Multi-Agent-Blog-Writer.git
    cd Multi-Agent-Blog-Writer
    ```

2.  **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables**:
    Create a `.env` file in the root directory and add your keys:
    ```env
    GOOGLE_API_KEY=your_google_api_key_here
    TAVILY_API_KEY=your_tavily_api_key_here
    ```

## Usage

1.  **Start the Streamlit app**:
    ```bash
    streamlit run app.py
    ```

2.  **Open your browser**: The app should automatically open at `http://localhost:8501`.

3.  **Generate a Blog Post**:
    - Enter a topic in the text area (e.g., *"The Future of AI in Education"*).
    - Click **"Start Workflow"**.
    - Watch as the agents perform research, outline the post, and write the content.
    - Once finished, you can view the final output in the UI and download the generated `.txt` file.

## Project Structure

- `app.py`: Main entry point for the Streamlit application.
- `graph.py`: Defines the main `super_graph` connecting the Supervisor and sub-teams.
- `research_team.py`: Defines the research subgraph and its agents.
- `writing_team.py`: Defines the writing subgraph and its agents.
- `tools.py`: Custom tools for scraping, file I/O, and Python execution.
- `state.py`: Defines the `State` schema used across the graph.
- `llm.py`: Configures the LLM (Google Gemini) and rate limits.
- `utils.py`: Utility functions, including the supervisor node creation logic.
- `config.py`: Configuration and environment validation.

## ⚠Notes

- The application creates a `temp/` directory to store intermediate files (outlines, drafts).
- Ensure your API keys have sufficient quotas, as multi-agent loops can generate multiple LLM calls per run.

## License

This project is licensed under the MIT License.