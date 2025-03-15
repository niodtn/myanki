from .invoke import invoke


def find(query: str) -> dict:
    response = invoke("findCards", params={"query": query})
    return response


def info(cards: list[int]):
    response = invoke("cardsInfo", params={"cards": cards})
    return response
