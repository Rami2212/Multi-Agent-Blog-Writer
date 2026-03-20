import os
from dotenv import load_dotenv

load_dotenv()

# Ensure the temp directory exists
os.makedirs(os.path.join(os.getcwd(), "temp"), exist_ok=True)

def _set_if_undefined(var: str):
    """Raise an error if env var is missing."""
    if not os.environ.get(var):
        raise EnvironmentError(f"{var} is not set. Please add it to your .env file or system environment.")

def check_env_vars():
    """Check required environment variables."""
    _set_if_undefined("TAVILY_API_KEY")
    _set_if_undefined("GOOGLE_API_KEY")

# Run the check
check_env_vars()