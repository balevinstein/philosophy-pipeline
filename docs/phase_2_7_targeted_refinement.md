# Phase II.7: Targeted Refinement

## Overview

Phase II.7 implements the revision plan from Phase II.6, performing targeted refinements on philosophical moves, thesis, and overall paper structure. This phase transforms identified issues into concrete improvements.

## Purpose

- Implement specific revisions identified in Phase II.6
- Refine or redevelop philosophical moves as needed
- Update thesis and core contribution for clarity
- Ensure all quality standards are met
- Prepare refined content for writing phase

## Refinement Process

### Move-by-Move Refinement
For each philosophical move:
1. Analyzes specific issues identified
2. Determines refinement strategy (refine, redevelop, merge, or cut)
3. Implements improvements while preserving strengths
4. Validates against quality standards

### Thesis and Contribution Updates
- Incorporates reviewer feedback
- Ensures precision and clarity
- Aligns with refined moves
- Maintains philosophical rigor

## Key Components

### Input
- Original moves from Phase II.3
- Revision plan from Phase II.6
- Holistic review feedback
- Quality standard requirements

### Refinement Strategies

1. **Refine**: Minor adjustments to existing content
   - Clarify ambiguous language
   - Add missing examples
   - Strengthen transitions
   - Fix citation issues

2. **Redevelop**: Major reconstruction
   - Complete rewrite maintaining core insight
   - New examples and argumentation
   - Different analytical approach
   - Enhanced philosophical depth

3. **Merge**: Combine related moves
   - Identify redundancies
   - Create stronger unified argument
   - Improve paper flow

4. **Cut**: Remove problematic moves
   - When fundamentally flawed
   - When redundant with other content
   - When weakening overall argument

### Output Structure

```json
{
  "revised_paper_vision": {
    "thesis": "Refined thesis statement",
    "core_contribution": "Updated contribution",
    "revision_summary": "What changed and why"
  },
  "refined_moves": [
    {
      "key_move_index": 0,
      "key_move_text": "Original move description",
      "refined_content": "Updated philosophical content",
      "status": "Retained|Redeveloped|Merged|Cut",
      "retention_notes": "Explanation of changes",
      "addressed_issues": ["List of issues fixed"]
    }
  ],
  "refinement_metadata": {
    "original_count": 5,
    "refined_count": 4,
    "redeveloped_count": 1,
    "cut_count": 1,
    "merge_count": 0
  }
}
```

## Configuration

In `config/conceptual_config.yaml`:

```yaml
models:
  phase_2_7_redevelopment:
    provider: "anthropic"
    model: "claude-sonnet-4-20250514"
    temperature: 0.5
    max_tokens: 8192
```

## Usage

```bash
python run_phase_2_7.py
```

The script will:
1. Load revision plan from Phase II.6
2. Process each move according to its refinement strategy
3. Update thesis and contribution as needed
4. Validate all refinements against quality standards
5. Save results to `outputs/phase_2_7_refined_context.json`

## Integration with Pipeline

Phase II.7 provides refined content to:
- **Phase II.8**: Uses refined moves and thesis for writing optimization
- **Phase III**: Provides clean, validated content for paper writing

## Refinement Examples

**Original Move**: 
"The systematic distinction between epistemic and moral blame challenges assumptions..."

**Issue Identified**: 
"'Systematic distinction' implies clean separation contradicted by entanglement cases"

**Refined Version**:
"Professional ignorance often involves epistemic failure without moral failure, and moral failure without epistemic failure, revealing that blame operates across distinct evaluative dimensions..."

## Quality Validation

Each refined move is checked against:
- Hájek heuristics (re-run all 5 tests)
- Analysis patterns (conversational tone, examples)
- Anti-RLHF standards (clear positions)
- Philosophical rigor (precision, coherence)

## Key Benefits

1. **Targeted Improvement**: Addresses specific identified issues
2. **Quality Assurance**: Validates all changes against standards
3. **Flexibility**: Multiple refinement strategies available
4. **Efficiency**: Focuses effort on problematic content

## Troubleshooting

Common scenarios:
- **Redevelopment loops**: If a move fails validation after refinement, consider cutting
- **Thesis drift**: Ensure refined thesis maintains paper's core insight
- **Over-refinement**: Preserve what works well - don't fix what isn't broken
- **Word count**: Monitor if refinements significantly change paper length 