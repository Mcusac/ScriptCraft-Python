def apply_tag_rules(value: str) -> str:
    """
    Business rules ONLY.
    Must assume sanitized input.
    """

    if not value:
        return ""

    # padding rule
    if len(value) == 5 and value[0] in {"3", "4"}:
        return "000" + value

    return value