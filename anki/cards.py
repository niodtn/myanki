from .invoke import invoke


def find(query: str) -> dict:
    response = invoke("findCards", params={"query": query})
    return response
