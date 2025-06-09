def load_and_combine_style_guides() -> str:
    """
    Loads the two Analysis style guides and combines them into a single string.
    """
    try:
        with open("./docs/analysis_style_guide.md", 'r', encoding='utf-8') as f:
            docs_guide = f.read()
    except FileNotFoundError:
        docs_guide = "Analysis Style Guide (from docs) not found."

    try:
        with open("./analysis_cache/analysis_style_guide.md", 'r', encoding='utf-8') as f:
            cache_guide = f.read()
    except FileNotFoundError:
        cache_guide = "Analysis Style Guide (from cache) not found."

    combined_guide = f"""<analysis_style_guide>
<high_level_guide>
{docs_guide}
</high_level_guide>

<actionable_checklist_guide>
{cache_guide}
</actionable_checklist_guide>
</analysis_style_guide>"""

    return combined_guide 