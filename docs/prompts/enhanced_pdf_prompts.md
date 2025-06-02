# Enhanced PDF Reading Prompts (Anthropic Best Practices)

## Phase II.1 PDF Reading Enhancement

### System Prompt
```
You are an expert philosophy researcher conducting deep analytical reading of academic papers. You excel at:
1. Identifying core philosophical arguments and their structure
2. Extracting quotable passages with precise citations
3. Recognizing opportunities for philosophical engagement
4. Understanding dialectical positioning within debates
```

### Two-Stage Reading Process

#### Stage 1: Quote Extraction
```xml
<task>First Pass: Extract Key Quotations</task>

<instructions>
Read through the paper and extract 5-10 key quotations that:
1. State the main thesis or claims
2. Define key concepts or distinctions
3. Present crucial arguments or examples
4. Acknowledge limitations or objections
5. Position the work relative to other philosophers

For each quote:
- Include the EXACT text in quotation marks
- Note the page number
- Add a brief note about why this quote matters
</instructions>

<output_format>
QUOTES:
1. [p. X] "Exact quote text here" 
   - Why it matters: [Brief explanation]

2. [p. Y] "Another exact quote"
   - Why it matters: [Brief explanation]
</output_format>
```

#### Stage 2: Deep Analysis
```xml
<task>Second Pass: Philosophical Analysis</task>

<context>
Here are the key quotes from the paper:
[INSERT NUMBERED QUOTES FROM STAGE 1]
</context>

<analysis_tasks>
1. THESIS AND ARGUMENT STRUCTURE
   - State the main thesis (cite quote number)
   - Map the argument structure using the quotes
   - Identify the philosophical problem being addressed

2. KEY MOVES AND INNOVATIONS
   - What novel philosophical moves does the author make?
   - How do they advance beyond existing positions?
   - What conceptual distinctions do they introduce?

3. DIALECTICAL POSITIONING
   - Which philosophers/positions do they engage? (cite quotes)
   - What objections do they anticipate?
   - What objections do they miss?

4. ENGAGEMENT OPPORTUNITIES
   Using specific quotes as jumping-off points:
   - Where could we push their argument further?
   - What counterexamples might challenge their view?
   - What implications haven't they explored?
   - Where might their distinctions break down?

5. TERMINOLOGY AND CONCEPTS
   - Key technical terms (with quote references)
   - Important distinctions made
   - Conceptual framework employed
</analysis_tasks>

<output_format>
{
  "thesis": {
    "statement": "...",
    "supporting_quotes": [1, 3, 5]
  },
  "argument_structure": {
    "main_premises": [...],
    "key_moves": [...],
    "conclusion": "..."
  },
  "engagement_opportunities": [
    {
      "type": "extension",
      "description": "...",
      "relevant_quote": 4
    }
  ],
  "key_terminology": {...}
}
</output_format>
```

### Integration Instructions for Development

When implementing, ensure:
1. **Two-pass structure**: First extract quotes, then analyze using those quotes
2. **Quote numbering**: Makes referencing much cleaner
3. **Page numbers**: Critical for academic credibility
4. **Engagement focus**: Always looking for how to build on/challenge the work

### Example Enhancement for Key Concepts

For papers introducing new concepts/distinctions:
```xml
<concept_extraction>
For each major concept or distinction:
1. The exact definition (with quote and page)
2. How it differs from existing concepts
3. What work it's supposed to do
4. Potential weaknesses or ambiguities
5. How we might use or challenge it
</concept_extraction>
``` 