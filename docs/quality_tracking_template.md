# Quality Tracking System

## Purpose
Track paper quality improvements across pipeline iterations to identify what's working and what needs attention.

## Tracking Spreadsheet Structure

### Sheet 1: Run Summary
| Run ID | Date | Topic | Config Changes | Overall Quality | Submittable? | Notes |
|--------|------|-------|----------------|-----------------|--------------|-------|
| run_001 | 1/15 | Attention & Blame | Baseline | 6/10 | No | Weak citations |
| run_002 | 1/16 | Epistemic Injustice | Enhanced PDF prompts | 7/10 | No | Better engagement |

### Sheet 2: Detailed Metrics (per run)
| Metric | Score (1-10) | Evidence | Action Needed |
|--------|--------------|----------|---------------|
| **Thesis Clarity** | 8 | Clear in abstract and intro | - |
| **Argument Depth** | 5 | Surface-level engagement | Enhance Phase II.3 |
| **Literature Integration** | 4 | Only 6 sources, minimal quotes | Priority fix |
| **Philosophical Sophistication** | 6 | Some good moves but repetitive | Add variety |
| **Structure/Flow** | 7 | Decent but some repetition | - |
| **Objection Handling** | 5 | Generic objections | Need anticipation |

### Sheet 3: Literature Engagement Tracking
| Run ID | Papers Cited | Papers Quoted | Avg Quotes/Paper | Deep Engagement Count |
|--------|--------------|---------------|------------------|----------------------|
| run_001 | 6 | 2 | 1.0 | 1 |
| run_002 | 10 | 5 | 2.4 | 3 |

## How to Use

### After Each Run:
1. **Quick Assessment** (You do this as philosophy professor)
   - Read final_paper.md
   - Fill out 1-10 scores for each metric
   - Note specific evidence/problems
   
2. **Automated Counts** (Script can do this)
   - Count citations
   - Count quotations
   - Word count by section
   - Check structural elements

3. **Identify Patterns**
   - If literature integration stays low → Focus on Phase II.1
   - If argument depth is weak → Enhance Phase II.3
   - If sophistication is lacking → Improve prompts across board

## Simple Python Helper

```python
def analyze_paper(paper_path):
    """Auto-fill what we can measure programmatically"""
    with open(paper_path, 'r') as f:
        content = f.read()
    
    return {
        'word_count': len(content.split()),
        'citation_count': content.count('(19') + content.count('(20'),  # Rough
        'quote_count': content.count('"') // 2,  # Rough
        'section_count': content.count('##'),
        'has_abstract': 'Abstract' in content,
        'has_objections': 'Objection' in content or 'objection' in content
    }
```

## Target Intervention Example

If tracking shows:
- Literature integration: 4/10 across 3 runs
- Argument depth: 7/10 across 3 runs

→ Prioritize Phase II.1 PDF enhancements over other improvements 