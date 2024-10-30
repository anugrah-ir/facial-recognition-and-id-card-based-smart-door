def get_key_value_pair(text):
    if ":" in text:
        key, value = text.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key and value:
            return key, value