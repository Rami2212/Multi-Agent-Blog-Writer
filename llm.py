from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.rate_limiters import InMemoryRateLimiter

rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.16,
    check_every_n_seconds=0.5,
    max_bucket_size=5,
)

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite-preview",
    max_retries=3,
    rate_limiter=rate_limiter,
)

