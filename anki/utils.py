import re


def remove_ruby_tag(card_info: dict) -> dict:
    # 모든 종류의 루비 태그를 처리하는 단일 정규식 패턴
    pattern = r"<ruby>([^<]+)(?:<rp>\(</rp>)?<rt>[^<]+</rt>(?:<rp>\)</rp>)?</ruby>"

    for field_name, field_data in card_info.items():
        if "value" in field_data and isinstance(field_data["value"], str):
            field_data["value"] = re.sub(pattern, r"\1", field_data["value"])

    return card_info
