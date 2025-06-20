# Philosophical Moves Injection Strategy

## Core Principle
Rather than random injection, use **contextual relevance** to select which moves to show each worker.

## Implementation Plan

### Phase II.2 - Abstract Development
**Inject 2-3 framing moves** showing:
- Scope limitation techniques
- Thesis clarity patterns
- Hook development

Example injection point in `abstract_development_prompts.py`:
```python
self.philosophical_moves = """
Here are examples of effective philosophical framing from Analysis papers:

1. **Scope Limitation Pattern**: "However, even if we accept the existence of either essentialist facts... we can simply restrict (PG) to conjunctions of..." 
   - Shows how to acknowledge objections while maintaining core thesis
   
2. **Mechanism Testing**: "When mechanism M is proposed, test M across varied contexts to identify its scope and limits"
   - Demonstrates systematic exploration of philosophical proposals
"""
```

### Phase II.3 - Key Moves Development
**Inject 3-4 dialectical patterns** showing:
- Objection anticipation
- Response construction
- Counterexample handling

Example moves:
- "Inductive Plausibility Defense": Show holds for uncontroversial cases → no clear counterexamples → claim warrant
- "Alternative Principle Construction": When P faces objection O, construct weaker P+ that avoids O but preserves conclusion

### Phase II.4 - Outline Development
**Inject 2 structural patterns** showing:
- Progressive argument building
- Section interconnection

### Phase III.1 - Section Writing
**Inject 3-5 detailed examples** showing:
- Concrete case construction
- Step-by-step analysis
- Example-driven argumentation

### Critics (All Phases)
**Inject Hájek-style patterns** showing what to look for:
- Extreme case vulnerabilities
- Self-undermining potential
- Boundary condition failures

## PDF → TXT Migration Strategy

### Benefits of TXT over PDF:
- **3x more examples** in same context window (8k vs 25k tokens)
- **Faster processing** (no PDF parsing overhead)  
- **More reliable** (no extraction errors)

### Migration Plan:
1. Continue extracting remaining PDFs to TXT
2. Update literature processing to prefer TXT when available
3. Keep PDF capability for new papers not yet extracted

### Code Change Example:
```python
# In literature_processor.py
def select_papers_for_attachment(self, topic):
    # Prefer TXT files
    txt_papers = self.get_available_txt_papers(topic)
    if len(txt_papers) >= 2:
        return random.sample(txt_papers, 2)
    
    # Fall back to PDFs if needed
    return self.get_pdf_papers(topic)
```

## Quality Control

### Move Selection Criteria:
1. **Self-contained**: Must be understandable without full paper context
2. **Pattern clarity**: The philosophical technique must be evident
3. **Transferability**: Pattern should work across multiple domains
4. **Length appropriate**: 100-400 words typically

### Tracking Effectiveness:
- Monitor which patterns appear in generated papers
- Check if critics catch more sophisticated issues
- Measure improvement in dialectical depth

## Next Steps

1. **Immediate**: Update 2-3 key prompts with curated moves
2. **This Week**: Extract remaining PDFs to TXT
3. **Next Week**: Full integration across all workers
4. **Ongoing**: Expand database as we find particularly effective patterns 