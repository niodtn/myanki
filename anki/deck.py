from .invoke import invoke


def is_exist(deck_name: str) -> bool:
    """덱 존재 여부 확인"""
    decks = invoke("deckNames")
    return deck_name in decks["result"]


def get_config(deck_name: str):
    return invoke("getDeckConfig", params={"deck": deck_name})


def create(deck_name: str) -> None:
    invoke("createDeck", params={"deck": deck_name})
