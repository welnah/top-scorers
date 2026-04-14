"""
Manual CSV parser — implemented without standard libraries.
This module handles converting raw CSV string data into structured dictionaries.
"""

def parse_csv(raw_text: str) -> list[dict]:
    lines = raw_text.splitlines()
    records = []

# Remove empty lines and lines that are just whitespace
    lines = [line for line in lines if line.strip()]

    if not lines:
        return records

# Extract headers from the first line (column names)
    headers = _split_line(lines[0])

    for line in lines[1:]:
        fields = _split_line(line)

        if len(fields) != len(headers):
            continue
 # Map each field to its corresponding header
        record = {headers[i]: fields[i] for i in range(len(headers))}
        records.append(record)

    return records


def _split_line(line: str) -> list[str]:

    """
    Helper to split a single CSV line by commas while respecting quoted fields.
    """
    fields = []
    current = ""
    inside_quotes = False

    for char in line:
        if char == '"':
            inside_quotes = not inside_quotes
        elif char == ',' and not inside_quotes:
            fields.append(current.strip())
            current = ""
        else:
            current += char

    fields.append(current.strip())
    return fields