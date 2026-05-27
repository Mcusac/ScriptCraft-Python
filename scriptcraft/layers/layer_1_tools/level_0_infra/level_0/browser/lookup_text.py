"""PeopleSoft lookup string normalization (no Playwright dependency)."""


def normalize_lookup_text(value: str) -> str:
    """Collapse whitespace for PeopleSoft lookup link vs input comparison."""
    return " ".join(str(value).split()).strip()


def text_matches_lookup(link_text: str, expected: str) -> bool:
    normalized_link = normalize_lookup_text(link_text)
    normalized_expected = normalize_lookup_text(expected)
    if normalized_link == normalized_expected:
        return True
    return normalized_link.replace(" ", "") == normalized_expected.replace(" ", "")


def format_location_for_lookup(value: str) -> str:
    """
    PeopleSoft location lookup expects building + two spaces + room.
    Display fields often render a single space; reconciliation CSVs use two.
    """
    text = str(value).replace("\u00a0", " ")
    collapsed = normalize_lookup_text(text)
    building, _, room = collapsed.partition(" ")
    if room:
        return f"{building}  {room}"
    return collapsed
