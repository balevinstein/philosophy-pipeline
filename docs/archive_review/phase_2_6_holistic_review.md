# Phase II.6: Holistic Review

## Overview

Phase II.6 performs a two-stage holistic review of the consolidated content, acting as a sophisticated philosophical referee. It evaluates the paper as a whole and generates concrete revision plans to address identified issues.

## Purpose

- Provide expert philosophical critique of the entire paper concept
- Identify fatal flaws, major issues, and minor problems
- Generate specific, actionable revision guidance
- Ensure paper meets Analysis journal standards

## Two-Stage Process

### Stage 1: Holistic Review
Evaluates the paper from multiple perspectives:
- Philosophical soundness and rigor
- Argument coherence and integration
- Thesis clarity and defensibility
- Literature positioning
- Analysis journal fit

### Stage 2: Revision Planning
Generates concrete plans for improvement:
- Specific fixes for each identified issue
- Move-by-move revision guidance
- Thesis and abstract refinements
- Structural reorganization suggestions

## Key Components

### Input
- Consolidated content from Phase II.5
- Diagnostic analysis from Phase II.5
- Quality assessment results
- Priority improvements list

### Review Criteria

1. **Philosophical Quality**
   - Argument validity and soundness
   - Conceptual clarity and precision
   - Counterexample resilience
   - Theoretical contribution

2. **Hájek Test Results**
   - Reviews failures from Phase II.5
   - Suggests specific fixes
   - Identifies patterns across failures

3. **Analysis Compliance**
   - 4,000-word feasibility
   - Conversational tone
   - Example-driven argumentation
   - Clear thesis statement

4. **Integration Assessment**
   - Move coherence
   - Literature engagement
   - Internal consistency
   - Narrative flow

### Output Structure

```json
{
  "holistic_review": {
    "overall_assessment": "strong|moderate|weak",
    "philosophical_quality": {
      "strengths": [...],
      "weaknesses": [...],
      "fatal_flaws": [...]
    },
    "hajek_test_failures": [
      {
        "test": "extreme_case",
        "failure_description": "...",
        "suggested_fix": "..."
      }
    ],
    "anti_rlhf_violations": [...],
    "recommendation": "proceed|revise|reconsider"
  },
  "revision_plan": {
    "thesis_revision": {
      "current": "...",
      "suggested": "...",
      "rationale": "..."
    },
    "move_revisions": [
      {
        "move_id": "move_1",
        "issues": [...],
        "revision_strategy": "...",
        "specific_changes": [...]
      }
    ],
    "structural_changes": {...},
    "priority_order": [...]
  }
}
```

## Configuration

In `config/conceptual_config.yaml`:

```yaml
models:
  phase_2_5_review:
    provider: "anthropic"
    model: "claude-sonnet-4-20250514"
    temperature: 0.1
    max_tokens: 8192
  phase_2_5_plan:
    provider: "anthropic"
    model: "claude-sonnet-4-20250514"
    temperature: 0.5
    max_tokens: 32000
```

## Usage

```bash
python run_phase_2_6_review.py
```

The script will:
1. Load consolidated content and diagnostics from Phase II.5
2. Perform holistic philosophical review
3. Generate detailed revision plan
4. Save results to `outputs/paper_[id]/phase_2_6_holistic_review/`

## Integration with Pipeline

Phase II.6 feeds into:
- **Phase II.7**: Implements the revision plan with targeted refinements
- **Phase II.8**: Uses improved content for writing optimization

## Review Examples

From actual runs:

**Fatal Flaw Identified**:
"Extreme case test failure: Theory claims professional ignorance can have epistemic failure without moral failure, but willful ignorance cases show these are necessarily connected when harm results."

**Revision Suggestion**:
"Narrow thesis scope to 'non-willful professional ignorance' or develop framework for when epistemic-moral connections are contingent vs necessary."

## Key Benefits

1. **Expert Critique**: Applies professional philosopher perspective
2. **Actionable Guidance**: Provides specific revision strategies
3. **Quality Gateway**: Prevents weak arguments from reaching writing phase
4. **Efficiency**: Catches issues early in the pipeline

## Troubleshooting

Common issues:
- **Review harshness**: The reviewer is intentionally critical - this improves final quality
- **Long processing**: Two-stage review can take 2-3 minutes total
- **Revision complexity**: Some suggestions may require returning to earlier phases 