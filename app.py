import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Multi-Agent Blog Writer", layout="wide")

st.title("Multi-Agent Blog Writer")

# Ensure required API keys exist
if not os.environ.get("GOOGLE_API_KEY") or not os.environ.get("TAVILY_API_KEY"):
    st.error("Missing API keys. Please set GOOGLE_API_KEY and TAVILY_API_KEY in your .env or system environment.")
    st.stop()

# Import graph after environment variables are set
try:
    from graph import super_graph
except Exception as e:
    st.error(f"Failed to initialize the agent graph: {e}")
    st.stop()

# User Input
user_input = st.text_area("What would you like to research and write about?", height=150)

if st.button("Start Workflow"):
    if not user_input.strip():
        st.warning("Please enter a topic.")
    else:
        st.write("Initializing agents...")

        initial_state = {
            "messages": [
                ("user", user_input)
            ]
        }

        # Container for output
        output_container = st.container()

        with st.status("Running Workflow...", expanded=True) as status:
            try:
                # Run the graph
                for chunk in super_graph.stream(initial_state, {"recursion_limit": 50}):
                    for node, update in chunk.items():

                        # Handle supervisor routing updates
                        if "next" in update:
                            next_node = update["next"]
                            status.write(f"Supervisor routed to: **{next_node}**")
                            continue

                        # Handle messages updates
                        if "messages" in update:
                            messages = update["messages"]
                            if messages:
                                last_msg = messages[-1]
                                content = last_msg.content
                                name = last_msg.name if hasattr(last_msg, "name") else node

                                status.write(f"**{node}** completed a step.")

                                # Display in main container
                                with output_container:
                                    with st.expander(f"Output from {name or node}", expanded=True):
                                        st.markdown(content)

            except Exception as e:
                status.update(label="Error occurred", state="error")
                st.error(f"An error occurred during execution: {e}")