import requests
from langchain_core.tools import tool
from langchain_community.utilities import WikipediaAPIWrapper


custom_headers = {
    "User-Agent": (
        "AgenticLangChainBot/1.0 "
        "(https://github.com; email@example.com) "
        "generic-library/requests"
    )
}


@tool
def search_wikipedia(query: str) -> str:
    """
    Queries the Wikipedia API to search for structural or background
    information.
    """
    try:
        wiki = WikipediaAPIWrapper()

        import wikipedia
        wikipedia.extensions.requests.headers.update(custom_headers)

        return wiki.run(query)

    except requests.exceptions.HTTPError as http_err:
        if http_err.response.status_code == 429:
            return ("Error: The Wikipedia API is currently rate-limiting this"
                    "bot. Please retry in a few moments.")
        return f"HTTP error occurred: {http_err}"

    except Exception:
        return ("Wikipedia tool error encountered: Wikipedia rate-limiting "
                "triggered a non-JSON error sequence.")
