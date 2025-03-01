# src/prompts/json_format.py


class JSONFormattingRequirements:
    """Centralized JSON formatting requirements used across the pipeline"""

    def __init__(self):
        self.JSON_FORMATTING_REQUIREMENTS = r"""
        CRITICAL JSON REQUIREMENTS - ANY VIOLATION WILL CAUSE PARSING TO FAIL

    1. BASIC JSON STRUCTURE
    - Property names must be in double quotes: {"property": "value"}
    - Arrays must use proper commas: ["first", "second", "last"]
    - WRONG array formats:
        * Missing commas: ["first" "second"]
        * Trailing comma: ["first", "second",]
    - No trailing commas in objects: {"a": 1, "b": 2}  # NOT {"a": 1, "b": 2,}
    - All content must be on a single line (use \n for line breaks)

    2. TEXT CONTENT RULES
    - NEVER use raw double quotes (") in content. Just for properties and values:
    - NEVER use Python-style triple quotes
    - Use either:
        a) Single quotes: "content": "Using 'quoted text' like this"
        b) QUOTE markers: "content": "Using QUOTE quoted text QUOTE like this"
    - For nested quotes, use numbered QUOTE markers:
        "content": "He said QUOTE1 I think QUOTE2 maybe QUOTE2 is right QUOTE1"

    3. LATEX NOTATION
    Pure LaTeX (for reference):
    $B_i(\phi) \rightarrow \Box B_i(\phi)$

    In JSON (note double backslashes):
    "formal_notation": "$B_i(\\phi) \\rightarrow \\Box B_i(\\phi)$"

    Common notation with proper escaping:
    * "\\phi", "\\psi" for variables
    * "\\rightarrow" for implication
    * "\\Box" for necessity
    * "\\Diamond" for possibility
    * "\\forall", "\\exists" for quantifiers
    * "\\land", "\\lor" for conjunction/disjunction

    4. ESCAPING RULES
    - Line breaks: \n
    - Tabs: \t
    - LaTeX backslashes must be doubled: \\ becomes \\\\
    - Example of complex content:
        {
            "content": "First line\\nSecond line with LaTeX $\\\\phi$"
        }

    5. Special Cases to Avoid:
   - Don't use JSON-style colons in content:
     WRONG: "content": "This can be expressed 'as': '$\\phi \\rightarrow \\psi$' "
     WRONG: "content": "This can be expressed "as": "$\\phi \\rightarrow \\psi$" "
     CORRECT: "content": "This can be expressed as: $\\phi \\rightarrow \\psi$"

   - For possessives, use straight apostrophes:
     WRONG: "content": "The agent"'s belief"
     CORRECT: "content": "The agent's belief"

    COMPREHENSIVE EXAMPLES:

    1. Simple quoted text:
    CORRECT: "content": "Alice said 'hello' to Bob"
    CORRECT: "content": "Alice said QUOTE hello QUOTE to Bob"
    WRONG: "content": "Alice said "hello" to Bob"

    2. Nested quotes:
    CORRECT: "content": "Bob said QUOTE1 I think Alice means QUOTE2 maybe QUOTE2 QUOTE1"
    WRONG: "content": "Bob said \"I think Alice means \"maybe\"\""

    3. Quotes with LaTeX:
    CORRECT: "content": "The theorem states QUOTE $\\\\phi \\\\rightarrow \\\\psi$ holds QUOTE"
    WRONG: "content": "The theorem states \"$\phi \rightarrow \psi$ holds\""

    4. Formal notation:
    CORRECT: "formal_notation": "$\\\\forall x(\\\\phi(x) \\\\land \\\\psi(x))$"
    WRONG: "formal_notation": "$\forall x(\phi(x) \land \psi(x))$"

    5. Multi-line content (must use \n):
    CORRECT: {
        "content": "First line\\nSecond line\\nThird line"
    }
    WRONG: {
        "content": "First line
        Second line
        Third line"
    }
    """
