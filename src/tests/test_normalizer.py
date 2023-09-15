from normalizer import Normalizer


def test_normalize_name_with_leading_whitespace():
    assert Normalizer.normalize_name("   Alice") == "Alice"


def test_normalize_name_with_trailing_whitespace():
    assert Normalizer.normalize_name("Bob  ") == "Bob"


def test_normalize_name_with_extra_whitespace():
    assert Normalizer.normalize_name("  Charlie  ") == "Charlie"


def test_normalize_name_with_multiple_words():
    assert Normalizer.normalize_name("  john doe  ") == "John Doe"


def test_normalize_name_with_all_caps():
    assert Normalizer.normalize_name("  JANE DOE  ") == "Jane Doe"
