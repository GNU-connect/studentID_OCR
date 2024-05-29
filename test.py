

from difflib import SequenceMatcher


def get_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

print(get_similarity('컴퓨터공학과', '컴퓨터공학부'))