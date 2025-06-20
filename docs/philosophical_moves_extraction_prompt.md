# Philosophical Moves Extraction Prompt

## Task
Analyze this philosophy paper and extract distinct "philosophical moves" - the argumentative techniques, conceptual maneuvers, and dialectical strategies that make the philosophy work.

## For Each Move, Extract:

### 1. MOVE IDENTIFICATION
- **Name**: Give it a descriptive name (e.g., "Extreme Case Counterexample", "Conceptual Precision Through Cases")
- **Quote**: The exact text demonstrating this move (1-3 paragraphs)
- **Location**: Where in the paper's argument this appears

### 2. MOVE CLASSIFICATION (Multiple Categories Allowed)
- **Dialectical Moves**: Objection handling, burden shifting, concessions
- **Conceptual Moves**: Distinctions, analyses, precision techniques  
- **Example Moves**: Thought experiments, cases, analogies
- **Structural Moves**: Thesis setup, scope limitation, framing
- **Literature Moves**: Positioning, extending, challenging other work

### 3. MOVE MECHANICS
- **Setup Required**: What needs to be in place for this move to work?
- **How It Works**: The logical/rhetorical mechanism
- **What It Achieves**: The philosophical work accomplished

### 4. GENERALIZABILITY
- **Transferable Pattern**: Could this move work in other philosophical contexts?
- **Domain Specificity**: Is this move specific to ethics/metaphysics/epistemology?
- **Abstraction Level**: Concrete instance vs general pattern

### 5. MOVE QUALITY
- **Effectiveness**: How well does this move advance the argument?
- **Originality**: Is this a standard move or something novel?
- **Clarity**: How clearly is the move executed?

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
      "quote": "Exact text showing the move",
      "location": "Section/paragraph reference",
      "categories": ["dialectical", "example"],
      "setup_required": "What must be established first",
      "mechanism": "How the move works",
      "achievement": "What it accomplishes",
      "transferable_pattern": "Abstract pattern that could be reused",
      "domain_specificity": "General or domain-specific",
      "effectiveness": "High/Medium/Low with explanation",
      "originality": "Standard/Variation/Novel",
      "notes": "Any additional observations"
    }
  ],
  "emerging_patterns": [
    "Patterns you notice across multiple moves"
  ]
}
```

## Extraction Guidelines:

1. **Be Generous**: Extract 5-15 moves per paper - we want rich data
2. **Quote Precisely**: Include enough context to understand the move
3. **Think Abstractly**: Look for patterns that could transfer
4. **Note Combinations**: Some moves work in sequences
5. **Flag Interesting Techniques**: Even if hard to categorize

## Examples to Look For:

### Dialectical Patterns:
- "Concession then distinction" 
- "Burden shifting to opponent"
- "Dilemma construction"
- "Recursive objection handling"

### Conceptual Patterns:
- "Precision through cases"
- "Distinction then application"
- "Concept splitting"
- "Definitional maneuvering"

### Example Patterns:
- "Intuition pump setup"
- "Counterexample to principle"
- "Parallel case reasoning"
- "Scaling up/down"

### Structural Patterns:
- "Thesis by elimination"
- "Progressive refinement"
- "Scope announcement"
- "Strategic ordering"

Remember: We're building a database of philosophical techniques, not summarizing arguments. Focus on the MOVES, not the content. 