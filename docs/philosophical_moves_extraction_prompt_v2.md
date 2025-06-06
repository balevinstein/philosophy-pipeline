# Philosophical Moves Extraction Prompt V2

## Task
Analyze this philosophy paper and extract distinct "philosophical moves" - the argumentative techniques, conceptual maneuvers, and dialectical strategies that make the philosophy work.

## CRITICAL REQUIREMENT: Self-Contained Context
Each extracted move MUST be understandable in isolation. When quoting, include:
- **Setup context**: What was established before this move
- **The move itself**: The core argumentative technique
- **Resolution**: How the move concludes or what it establishes

If the quote references "the first type" or "this view" or "as shown above", you MUST either:
1. Include enough preceding text to explain what these refer to, OR
2. Add a brief [Context: ...] note before the quote explaining the reference

## For Each Move, Extract:

### 1. MOVE IDENTIFICATION
- **Name**: Descriptive name (e.g., "Extreme Case Counterexample")
- **Quote**: SELF-CONTAINED text (2-4 paragraphs typically)
- **Context Notes**: Brief explanation of any references [if needed]
- **Location**: Section/paragraph reference

### 2. MOVE CLASSIFICATION (Pick 1-2 Primary)
- **Offensive**: Attacking/undermining positions (counterexamples, reductios)
- **Defensive**: Protecting positions (distinctions, scope limits)
- **Constructive**: Building arguments (analyses, frameworks)
- **Meta**: Managing discussion (framing, positioning)

### 3. MOVE MECHANICS
- **Prerequisites**: What must already be established
- **Mechanism**: How the move works logically/rhetorically
- **Achievement**: What philosophical work it accomplishes

### 4. REUSABILITY
- **Pattern**: Abstract template that could transfer to other contexts
- **Domain**: General vs. specific to ethics/epistemology/etc.
- **Quality**: High/Medium/Low effectiveness

## Example of Good Context Capture:

❌ BAD (missing context):
Quote: "This avoids the problem of the first type while maintaining theoretical elegance."

✅ GOOD (self-contained):
Quote: "I have identified two types of failure in joint action: failing to 'do our part' (Type 1) and failing to respect collaborators (Type 2). The distinction I propose avoids the problem of the first type - where agents accidentally fail their contributions but immediately repair them - while maintaining theoretical elegance. Unlike Gilbert's account, we need not classify every minor stumble as a wronging."

OR with context note:
Context: [Type 1 failures are when agents fail to contribute to joint intentions but immediately repair]
Quote: "This avoids the problem of the first type while maintaining theoretical elegance..."

## Output Format:

```json
{
  "paper_info": {
    "title": "Paper Title",
    "author": "Author Name",
    "main_thesis": "One sentence thesis"
  },
  "philosophical_moves": [
    {
      "move_name": "Descriptive name",
      "quote": "SELF-CONTAINED quote with full context",
      "context_notes": "[Optional: explains any external references]",
      "location": "Section 2.1",
      "classification": ["offensive", "defensive", "constructive", "meta"],
      "prerequisites": "What reader needs to understand first",
      "mechanism": "How the move works",
      "achievement": "What it accomplishes",
      "pattern": "Transferable template",
      "domain": "General or specific",
      "quality": "High/Medium/Low"
    }
  ],
  "extraction_notes": "Any observations about move patterns in this paper"
}
```

## Guidelines:
1. **Prefer longer quotes** that include setup and payoff
2. **Test each quote**: Could someone understand this without reading the paper?
3. **5-8 high-quality moves** better than 10-15 fragmentary ones
4. **Focus on moves** that could teach an AI how to do philosophy

Remember: These moves will be used as few-shot examples. They must be pedagogically useful! 