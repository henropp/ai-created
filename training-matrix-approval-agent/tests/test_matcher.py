from matcher import match_staff_name


def test_unclear_match_flagged():
    aliases = []
    matched, conf = match_staff_name('Completely Different', ['Azger Ali'], aliases, threshold=95)
    assert matched is None
    assert conf < 0.95
