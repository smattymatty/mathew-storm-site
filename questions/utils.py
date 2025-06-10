# questions/utils.py

def generate_readable_name_from_slug(title_id_slug: str) -> str:
    """
    Converts a slug string into a human-readable title.

    Returns an empty string if the input is falsy. Each hyphen-separated part
    of the slug is capitalized and joined with spaces.
    """
    if not title_id_slug:
        return ""

    parts = title_id_slug.split('-')
    # Capitalize each part. For "01", .capitalize() keeps it "01".
    # For "first", .capitalize() makes it "First".
    processed_parts = [part.capitalize() for part in parts]
    return " ".join(processed_parts)
