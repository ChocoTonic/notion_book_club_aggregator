from titlecase import titlecase


class Normalizer:
    """
    A utility class for normalizing names.
    """

    @staticmethod
    def normalize_name(name: str) -> str:
        """Normalize a name.

        Args:
            name (str): The name to be normalized.

        Returns:
            str: The normalized name.
        """
        # an edge case to consider here is variable spacing between words or presence or absence of dash-like characters
        return titlecase(name.lower().strip())


if __name__ == "__main__":
    assert Normalizer.normalize_name("   aLice") == "Alice"
    assert Normalizer.normalize_name("BOB  ") == "Bob"
    assert Normalizer.normalize_name("  cHArLiE  ") == "Charlie"

    print("All assertions passed!")
