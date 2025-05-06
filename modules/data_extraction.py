import re

def detect_and_extract_credential(text):
    pattern = r'ID\s*:\s*(\d{11})'
    match = re.search(pattern, text)

    if match:
        return match.group(1)
    else:
        return None