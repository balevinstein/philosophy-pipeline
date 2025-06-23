# Phase II.8: Writing Context Optimization

## Overview

Phase II.8 prepares comprehensive writing aids and optimized context for Phase III, transforming refined philosophical content into writing-ready materials. This phase generates hooks, transitions, phrase banks, and integration guidance to ensure smooth, professional paper writing.

## Purpose

- Generate multiple introduction hooks for engaging openings
- Create smooth transitions between all sections
- Build Analysis-style phrase banks for philosophical writing
- Provide move integration guidance for narrative flow
- Map content to paper structure optimally
- Prepare all materials needed for efficient writing

## Writing Aid Components

### 1. Introduction Hooks
Generates 4-5 compelling openings using:
- Striking examples or cases
- Counterintuitive claims
- Philosophical puzzles or paradoxes
- Direct challenges to conventional wisdom
- Vivid scenarios illustrating the problem

### 2. Section Transitions
Creates smooth connections:
- Summary of what was established
- Preview of what's coming next
- Explanation of progression necessity
- Natural philosophical flow

### 3. Phrase Banks
Analysis-style phrases for:
- Introducing objections (without hedging)
- Making controversial claims (with confidence)
- Presenting examples (vividly and efficiently)
- Drawing implications (boldly but precisely)
- Acknowledging limits (without undermining)
- Engaging other philosophers (respectfully but directly)

### 4. Move Integration Guidance
For each philosophical move:
- Setup guidance for preparing readers
- Presentation style recommendations
- Example pattern suggestions
- Key phrases for expressing insights
- Common pitfalls to avoid

### 5. Section Blueprints
Detailed plans including:
- Word targets
- Content guidance
- Transition points
- Suggested moves
- Integration strategies

## Output Structure

```json
{
  "paper_metadata": {
    "thesis": "Final refined thesis",
    "core_contribution": "Final contribution statement",
    "target_journal": "Analysis",
    "word_target": 4000
  },
  "writing_aids": {
    "introduction_hooks": [
      {
        "hook_type": "example|paradox|challenge|scenario|puzzle",
        "text": "The actual hook text",
        "transition_to_thesis": "How it leads to thesis"
      }
    ],
    "section_transitions": {
      "into_section_2": "Transition text",
      "from_section_2": "Transition text"
    },
    "phrase_banks": {
      "introducing_objections": ["The obvious worry is...", ...],
      "making_claims": ["I argue that...", ...],
      "presenting_examples": ["Consider...", ...]
    },
    "conclusion_clinchers": [...]
  },
  "content_organization": {
    "move_to_section_mapping": {
      "section_2": [0, 1],
      "section_3": [2, 3]
    },
    "move_integration_guidance": [...],
    "citation_placement": {...}
  },
  "section_blueprints": [
    {
      "section_key": "introduction",
      "title": "Introduction",
      "word_target": 400,
      "content_guidance": "...",
      "transition_in": null,
      "transition_out": "...",
      "suggested_moves": []
    }
  ]
}
```

## Configuration

In `config/conceptual_config.yaml`:

```yaml
models:
  phase_2_8_hooks:
    provider: "anthropic"
    model: "claude-sonnet-4-20250514"
    temperature: 0.7
    max_tokens: 4096
  phase_2_8_transitions:
    provider: "anthropic"
    model: "claude-sonnet-4-20250514"
    temperature: 0.5
    max_tokens: 4096
  phase_2_8_integration:
    provider: "anthropic"
    model: "claude-sonnet-4-20250514"
    temperature: 0.5
    max_tokens: 8192
  phase_2_8_phrases:
    provider: "anthropic"
    model: "claude-sonnet-4-20250514"
    temperature: 0.6
    max_tokens: 4096
  phase_2_8_conclusion:
    provider: "anthropic"
    model: "claude-sonnet-4-20250514"
    temperature: 0.7
    max_tokens: 4096
```

## Usage

```bash
python run_phase_2_8.py
```

The script will:
1. Load refined content from Phase II.7
2. Generate all writing aids (hooks, transitions, phrases)
3. Create move integration guidance
4. Build section blueprints
5. Save comprehensive context to `outputs/phase_2_8_writing_context.json`

## Integration with Pipeline

Phase II.8 provides writing context to:
- **Phase III.1**: Section-by-section writing with all aids available
- **Phase III.2**: Final integration with smooth transitions

## Example Outputs

**Hook Example**:
```json
{
  "hook_type": "scenario",
  "text": "Dr. Martinez, an emergency physician, fails to consider domestic violence when treating suspicious injuries—not because she doesn't care, but because her training systematically overlooked this diagnostic category.",
  "transition_to_thesis": "This case reveals how professional ignorance can involve epistemic failure without moral failure, challenging unified accounts of blame."
}
```

**Phrase Bank Sample**:
```json
"introducing_objections": [
  "The obvious worry is that...",
  "Critics will immediately point out that...",
  "This faces a serious challenge:...",
  "One might reasonably object that...",
  "The natural response is to argue..."
]
```

## Key Benefits

1. **Writing Efficiency**: All materials prepared in advance
2. **Style Consistency**: Maintains Analysis journal tone throughout
3. **Smooth Flow**: Pre-planned transitions ensure coherence
4. **Professional Polish**: Publication-ready phrasing
5. **Flexibility**: Multiple options for each component

## Troubleshooting

Common issues:
- **API timeouts**: Multiple API calls can take 90+ seconds total
- **Hook quality**: Regenerate if hooks are too generic
- **Transition mismatch**: Ensure sections align with Phase II structure
- **Phrase repetition**: The system avoids redundant suggestions 