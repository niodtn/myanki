import re
from collections import defaultdict, Counter

from anki import AnkiConnectError, cards, utils


def main():
    card_ids = cards.find("deck:日本語")["result"]
    card_info = cards.info(card_ids)["result"]
    processed_cards = list(map(info_parser, card_info))

    # 일본어 필드 중복 확인
    duplicates = find_duplicates(processed_cards, "日本語")
    if duplicates:
        print("중복된 일본어 항목:")
        for japanese_text, _cards in duplicates.items():
            print(f"'{japanese_text}' - {len(_cards)}개 카드 중복:")
            for card in _cards:
                print(f"  - {card}")
    else:
        print("중복된 일본어 항목이 없습니다.")
    
    # 한자 사용 빈도 분석
    kanji_counts = count_kanji(processed_cards, "日本語")
    print("\n한자 사용 빈도 (상위 20개):")
    for kanji, count in kanji_counts.most_common(20):
        print(f"{kanji}: {count}회")


def count_kanji(cards, field_name):
    """
    주어진 필드에서 한자 사용 빈도를 계산합니다.
    
    Args:
        cards: 처리된 카드 목록
        field_name: 한자를 추출할 필드 이름
        
    Returns:
        한자와 그 출현 횟수를 담은 Counter 객체
    """
    # 한자 범위: CJK 통합 한자 (U+4E00 ~ U+9FFF)
    kanji_pattern = re.compile(r'[\u4e00-\u9fff]')
    
    kanji_counter = Counter()
    for card in cards:
        text = card.get(field_name, "")
        # 텍스트에서 한자만 추출
        kanji_list = kanji_pattern.findall(text)
        kanji_counter.update(kanji_list)
    
    return kanji_counter


def find_duplicates(cards, field_name):
    """
    주어진 필드 이름에 대해 중복된 값을 가진 카드들을 찾습니다.
    단, 모든 필드 내용이 완전히 동일한 카드는 중복으로 간주하지 않습니다.

    Args:
        cards: 처리된 카드 목록
        field_name: 중복을 확인할 필드 이름

    Returns:
        중복된 값을 키로 하고, 해당 값을 가진 카드 목록을 값으로 하는 딕셔너리
    """
    # 1. 필드 값으로 카드 그룹화
    field_values = defaultdict(list)
    for card in cards:
        value = card.get(field_name, "").strip()
        if value:  # 빈 값은 무시
            field_values[value].append(card)
    
    # 2. 카드 내용이 완전히 동일한지 확인하는 헬퍼 함수
    def cards_are_identical(card1, card2):
        if set(card1.keys()) != set(card2.keys()):
            return False
        return all(card1[k] == card2[k] for k in card1)
    
    # 3. 중복 필터링
    result = {}
    for value, card_group in field_values.items():
        if len(card_group) <= 1:
            continue
            
        # 내용이 완전히 같은 카드들은 제외하고 진짜 중복만 찾기
        unique_cards = []
        for card in card_group:
            # 이 카드가 다른 카드와 완전히 동일하지 않으면 추가
            if not any(cards_are_identical(card, other) 
                      for other in card_group if card is not other):
                unique_cards.append(card)
                
        if len(unique_cards) > 1:
            result[value] = unique_cards
            
    return result


def info_parser(card_info: dict) -> dict:
    fields = card_info.pop("fields")
    fields = utils.remove_ruby_tag(fields)

    # 필드 구조 단순화: {"필드": {value: "~~~", order: n}, ...} -> {"필드" : "~~~", ...}
    simplified = {}
    for field_name, field_data in fields.items():
        simplified[field_name] = field_data.get("value", "")

    return simplified


if __name__ == "__main__":
    try:
        main()
    except AnkiConnectError as e:
        print(f"에러: {e}")
