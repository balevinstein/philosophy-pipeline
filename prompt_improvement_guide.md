# Prompt Improvement Guide

## Current Status
- Phase II.1 has been enhanced with XML tags, system prompts, and better JSON handling
- Other phases (I.2, II.2-6, III.1-2) still need similar improvements

## Standard Improvements to Apply

### 1. Add System Prompts
Every phase should define the LLM's role clearly:
```python
system_prompt = """You are an expert philosophy researcher analyzing academic papers.
Your role is to [specific task for this phase].
You must output valid JSON that will be parsed by downstream pipeline stages."""
```

### 2. Add XML Structure Tags
Wrap all prompts with clear sections:
```xml
<context>
Explain what phase this is and what happens before/after
</context>

<task>
Clear description of what to do
</task>

<requirements>
- Specific requirement 1
- Specific requirement 2
</requirements>

<output_format>
Exact JSON schema expected
</output_format>
```

### 3. JSON Formatting Rules
Add to every prompt that outputs JSON:
```
CRITICAL JSON FORMATTING RULES:
1. Output ONLY valid JSON - no markdown, no explanations
2. Use double quotes for all strings
3. Escape quotes in text with \"
4. For multiline text, replace newlines with spaces
5. Ensure all brackets/braces are properly closed
```

### 4. Pipeline Context
Add to every prompt:
```
You are part of an automated pipeline. Your output will be parsed by code, not read by humans.
Any malformed JSON will cause the pipeline to fail.
```

## Phase-Specific Focus Areas

### Phase I.2 (Literature Search)
- Current issue: Manual PDF download required
- Consider: Adding automated PDF retrieval
- Focus: Clear query generation for Tavily API

### Phase II.2 (Thematic)
- Needs: XML structure for theme extraction
- Add: Clear examples of philosophical themes

### Phase II.3 (Quote Selection)
- Critical: Maintain page numbers from II.1
- Add: Quote quality criteria

### Phase II.4 (Structure)
- Needs: Clear argument structure templates
- Add: Section word count guidance

### Phase II.5 (Objections)
- Add: Types of philosophical objections
- Include: Response strategy examples

### Phase II.6 (Related Angle)
- Clarify: What makes an angle "related but fresh"
- Add: Novelty criteria

### Phase III.1 (Section Writing)
- Critical: Use quotes with page numbers
- Add: Academic writing style guide

### Phase III.2 (Integration)
- Focus: Smooth transitions
- Add: Citation formatting rules

## Model Selection Guide

### Use Cheaper Models (3.5 Sonnet/Haiku) For:
- Adding XML tags and system prompts
- Implementing JSON formatting rules
- Basic prompt restructuring
- Following this guide's patterns

### Use Opus For:
- Debugging complex issues
- Optimizing quote integration strategies
- Rivet graph modifications
- Novel architectural changes

## Testing Strategy
After improving each phase:
1. Run the phase individually if possible
2. Check JSON output validity
3. Verify quotes maintain page numbers
4. Compare output quality to baseline

## Success Metrics
- Zero JSON parsing errors
- All quotes have page numbers
- Output follows schema exactly
- Pipeline runs end-to-end without manual intervention 