def load_text_file(file_path: str) -> str:
    """Loads a text file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read() 