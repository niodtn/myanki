from anki import AnkiConnectError, cards, utils


def main():
    a = cards.find("deck:日本語")["result"]
    b = cards.info(a[:1])
    b = b["result"]
    b = list(map(info_parser, b))
    print(b)


def info_parser(card_info: dict) -> dict:
    ret = card_info.pop("fields")
    ret = utils.remove_ruby_tag(ret)
    return ret


if __name__ == "__main__":
    try:
        main()
    except AnkiConnectError as e:
        print(f"에러: {e}")
