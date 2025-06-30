# Phase II.5: Intelligent Consolidation

## Overview

Phase II.5 performs comprehensive diagnostic analysis of all developed philosophical content, integrating multiple quality standards to identify issues before proceeding to writing. This phase replaces the old Rivet-based consolidation with an intelligent, LLM-driven approach.

## Purpose

- Consolidate all developed content (abstract, outline, key moves) into a unified context
- Apply comprehensive quality standards to identify potential issues
- Generate diagnostic insights about paper readiness
- Flag critical problems that need addressing before writing

## Key Components

### Input
- Abstract and conceptual framework from Phase II.1
- Detailed outline from Phase II.2
- Developed key moves from Phase II.3
- Literature synthesis from Phase I.4

### Quality Standards Applied

1. **Hájek Heuristics** (5 tests)
   - Extreme case test
   - Self-undermining test
   - Counterexample vulnerability
   - Hidden assumptions test
   - Domain transfer test

2. **Analysis Journal Standards**
   - Hook → Thesis → Roadmap structure
   - Claim → Example → Analysis pattern
   - Conversational yet rigorous tone
   - 4,000-word scope appropriateness

3. **Anti-RLHF Patterns**
   - Flags hedging and equivocation
   - Ensures clear position-taking
   - Identifies "both-sidesism"
   - Checks for genuine philosophical argument

4. **Philosophical Skepticism**
   - Boundary case vulnerabilities
   - Counterexample resilience
   - Conceptual precision
   - Argumentative coherence

### Output Structure

```json
{
  "consolidated_content": {
    "abstract": "...",
    "outline": {...},
    "key_moves": [...],
    "literature_context": {...}
  },
  "diagnostic_analysis": {
    "thesis_clarity": "clear|muddy|contradictory",
    "argument_coherence": "strong|moderate|weak",
    "move_integration": "seamless|workable|problematic",
    "literature_positioning": "compelling|adequate|weak"
  },
  "issues_identified": [
    {
      "issue_type": "hajek_test_failure|analysis_pattern_violation|...",
      "severity": "critical|high|medium|low",
      "description": "...",
      "affected_components": ["abstract", "move_2", ...]
    }
  ],
  "quality_assessment": {
    "hajek_test_results": {...},
    "analysis_compliance": {...},
    "anti_rlhf_check": {...},
    "philosophical_rigor": {...}
  },
  "paper_readiness": "ready|needs_work|major_issues",
  "priority_improvements": [...]
}
```

## Configuration

In `config/conceptual_config.yaml`:

```yaml
models:
  phase_2_5_consolidation:
    provider: "anthropic"
    model: "claude-sonnet-4-20250514"
    temperature: 0.3
    max_tokens: 8192
```

## Usage

```bash
python run_phase_2_5.py
```

The script will:
1. Load all outputs from previous phases
2. Apply comprehensive quality diagnostics
3. Generate consolidated context with issues identified
4. Save results to `outputs/paper_[id]/phase_2_5_intelligent_consolidation/`

## Integration with Pipeline

Phase II.5 feeds into:
- **Phase II.6**: Uses diagnostics to guide holistic review
- **Phase II.7**: Targets identified issues for refinement
- **Phase II.8**: Provides clean consolidated content for writing optimization

## Key Benefits

1. **Early Issue Detection**: Catches philosophical problems before writing begins
2. **Quality Assurance**: Applies multiple rigorous standards systematically
3. **Diagnostic Clarity**: Provides specific, actionable feedback
4. **Pipeline Efficiency**: Prevents wasted effort on fundamentally flawed content

## Example Diagnostics

From actual run:
- "Constitutive normativity defense needs clear necessity conditions"
- "Move 3 relies on undefined technical terminology"
- "Thesis contains implicit scope ambiguity"
- "Extreme case test reveals boundary vulnerability"

## Troubleshooting

Common issues:
- **Missing inputs**: Ensure all previous phases have completed
- **API timeouts**: The comprehensive analysis can take 60-90 seconds
- **JSON parsing**: Check debug output in `outputs/debug_consolidation_response.txt` 