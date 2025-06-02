# JSON Parsing Improvement Strategies

## Current Issues
1. LLMs sometimes add explanatory text after JSON
2. Complex nested structures get malformed
3. Quotes and special characters cause parsing failures

## Proposed Solutions

### 1. Enhanced Prompt Instructions
Add to all prompts:
```
CRITICAL JSON FORMATTING RULES:
- Output ONLY valid JSON, no explanatory text before or after
- Use double quotes for ALL strings
- Escape special characters: \", \\, \n, \r, \t
- No trailing commas
- No comments (// or /* */)
- Numbers and booleans should NOT be quoted
- Ensure all brackets and braces are properly closed
- VERIFY your JSON is valid before outputting
```

### 2. Output Validation in Prompts
Add a validation reminder:
```
Before outputting, verify:
1. First character is { or [
2. Last character is } or ]
3. All strings use double quotes
4. No unescaped quotes inside strings
```

### 3. Simpler JSON Structures
Instead of deeply nested structures, use flatter designs:

**Current (complex)**:
```json
{
  "analysis": {
    "thesis": {
      "statement": "...",
      "supporting_quotes": [1, 2, 3]
    }
  }
}
```

**Better (flatter)**:
```json
{
  "thesis_statement": "...",
  "thesis_supporting_quotes": [1, 2, 3]
}
```

### 4. Two-Stage Output Approach
For complex outputs, use two stages:
1. First output: Core structured data (JSON)
2. Second output: Narrative analysis (Markdown)

This prevents mixing formats in single response.

### 5. JSON Schema Validation
Add explicit schema in prompts:
```
Output must match this schema:
{
  "field1": "string",
  "field2": ["array", "of", "strings"],
  "field3": {
    "nested": "object"
  }
}
```

### 6. Alternative: Use YAML
YAML is more forgiving and human-readable:
```yaml
thesis_statement: "The main thesis"
supporting_quotes:
  - quote: "First quote"
    page: 10
  - quote: "Second quote"
    page: 15
```

### 7. Enhanced JSON Cleaner
Add these improvements to json_utils.py:
- Strip everything before first { or [
- Strip everything after last } or ]
- Better handling of escaped characters
- More aggressive quote fixing

### 8. Prompt Engineering for Specific Models
For Claude 4 Sonnet:
- Use <json> tags to clearly delineate JSON output
- Add thinking tags before JSON for complex reasoning
- Use prefill to start the JSON correctly

## Recommended Approach

1. **Immediate**: Add enhanced JSON formatting rules to all prompts
2. **Short-term**: Implement better pre/post stripping in JSON cleaner
3. **Medium-term**: Flatten JSON structures where possible
4. **Long-term**: Consider YAML or other alternatives for complex data 