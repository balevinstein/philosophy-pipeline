#!/usr/bin/env python3
"""
Enhanced planning prompts for detailed outline development Phase II.4
Includes empirically-derived Analysis journal structural patterns
"""

from typing import Dict, Any, List


class DetailedOutlinePlanningPrompts:
    """Planning prompts for Phase II.4 detailed outline development with Analysis patterns"""
    
    def __init__(self):
        self.stage_name = "detailed_outline_planning"
    
    def get_system_prompt(self, phase: str, **kwargs) -> str:
        """Get system prompt for specific planning phase"""
        
        # Extract common variables with defaults
        moves_summary = kwargs.get('moves_summary', '[Key moves summary not provided]')
        topic = kwargs.get('topic', '[Topic not specified]')
        main_argument = kwargs.get('main_argument', '[Main argument not specified]')
        target_length = kwargs.get('target_length', '8000-10000')
        
        if phase == "framework_integration":
            # Enhanced with Analysis structural patterns from empirical analysis
            return f"""You are creating the structural framework for a philosophy paper targeting Analysis journal.

Your task: Transform developed key moves into a coherent paper structure following Analysis journal conventions.

<CRITICAL_REQUIREMENTS>
YOU MUST FOLLOW ANALYSIS JOURNAL PATTERNS. These are NOT suggestions but REQUIRED conventions:
</CRITICAL_REQUIREMENTS>

<ANALYSIS_PATTERNS_MANDATORY>
Based on empirical analysis of recent Analysis papers, YOU MUST implement these patterns:

<OPENING_STRUCTURE>
**REQUIRED (15-20% of paper):**
- **IMMEDIATE ENGAGEMENT**: Start directly with concrete examples, NOT abstract definitions
- **NO LONG LITERATURE REVIEWS**: Context woven throughout, never front-loaded
- **CONVERSATIONAL VOICE**: Use "Consider Sarah who..." and "More interestingly..." style
- **PROBLEM-FIRST**: Present puzzling cases before theoretical background

**EXAMPLE OPENING SENTENCE**: "Microaggressions – for example, members of racial minorities being asked 'Where are you really from?' – are common, apparently unintentional..."
</OPENING_STRUCTURE>

<ARGUMENT_ORGANIZATION>
**REQUIRED STRUCTURE:**
- **NUMBERED SECTIONS**: "1. Introduction", "2. The Meta-Question Shift", etc.
- **SUBSECTION NUMBERING**: "2.1 Ambiguity and clarity", "2.2 Wrongdoing and apology", etc.
- **CONCRETE EXAMPLES THROUGHOUT**: Named characters (Sarah, Mark, Dr. Martinez) in every section
- **CLAIM→EXAMPLE→ANALYSIS PATTERN**: Always demonstrate, then analyze

**FORBIDDEN**: Generic section titles like "Arguments" or "Literature Review"
</ARGUMENT_ORGANIZATION>

<TRANSITION_REQUIREMENTS>
**REQUIRED VOICE:**
- **CONVERSATIONAL CONNECTIVES**: "Consider", "More interestingly", "As a result", "This suggests"
- **DIRECT READER ENGAGEMENT**: "I suggest", "we seem to want", "Let us examine"
- **NATURAL FLOW**: Organic progression, NOT formal academic transitions

**FORBIDDEN**: Stiff academic transitions like "Having established X, we now turn to Y"
</TRANSITION_REQUIREMENTS>

<LITERATURE_INTEGRATION_RULES>
**REQUIRED APPROACH:**
- **INTEGRATED NOT ISOLATED**: No separate literature review section
- **DEEP NOT BROAD**: Substantial engagement with specific positions only
- **ARGUMENT-DRIVEN**: Citations support your points, don't drive structure
- **IMMEDIATE ENGAGEMENT**: "Regina Rini (2020) argues..." then immediate analysis

**FORBIDDEN**: Front-loaded literature reviews or citation-heavy surveys
</LITERATURE_INTEGRATION_RULES>

<WORD_ALLOCATION_REQUIREMENTS>
**MANDATORY DISTRIBUTION:**
- **Introduction: 15-20%** - Substantial but focused on concrete engagement
- **Main argument sections: 70-75%** - Primary philosophical work
- **Conclusion: 5-10%** - Brief synthesis, no new arguments

**SECTION BALANCE**: No single argument section should exceed 25% of total words
</WORD_ALLOCATION_REQUIREMENTS>

<DELIVERABLE_REQUIREMENTS>
You MUST provide:

**SECTION OUTLINE** with:
- Analysis-style section titles (descriptive, not generic)
- Precise word allocation per section
- Clear key move mapping to sections
- Concrete transition strategies between sections

**OPENING STRATEGY** specifying:
- Exact opening approach (example-first required)
- First paragraph blueprint with concrete case
- Direct engagement hook for Analysis readers

**ARGUMENT SEQUENCE** showing:
- Order of key moves with philosophical justification
- Integrated objection/response placement (no separate section)
- Progression toward practical conclusion

**LITERATURE PLACEMENT** detailing:
- Which authors engaged where and why
- Integration strategy (no isolated reviews)
- Balance of engagement vs. original argument development

<COMPLIANCE_CHECK>
Your framework will be evaluated on:
1. Does it open with concrete examples? (REQUIRED)
2. Does it avoid front-loaded literature review? (REQUIRED) 
3. Does it use conversational voice throughout? (REQUIRED)
4. Does it integrate rather than isolate citations? (REQUIRED)
5. Does it follow Analysis word allocation patterns? (REQUIRED)
</COMPLIANCE_CHECK>

## KEY MOVES TO STRUCTURE:
{moves_summary}

## PAPER CONTEXT:
- **Target length**: {target_length} words
- **Topic**: {topic}
- **Main thesis**: {main_argument}

Your framework must demonstrate mastery of Analysis conventions while organizing these specific philosophical moves effectively."""

        elif phase == "literature_mapping":
            return f"""You are mapping literature references to specific sections of a philosophy paper structure.

Given the framework structure and key moves, identify which scholars, papers, and theoretical positions should be engaged where.

## ANALYSIS JOURNAL LITERATURE STYLE:
- **Integrated engagement**: Weave citations naturally into argument flow
- **Deep not broad**: Substantial engagement with specific positions vs. surveys
- **Argument-driven**: Literature supports/challenges your points, doesn't drive structure

Framework: {moves_summary}
Topic: {topic}

Create a literature mapping that shows which sources to engage in each section and how."""

        elif phase == "content_development":
            return f"""You are developing detailed content guidance for each section of a philosophy paper.

Transform the structural framework into specific content directions for each section.

Framework: {moves_summary}
Topic: {topic}
Target length: {target_length}

Provide detailed guidance for developing each section's content."""

        elif phase == "structural_validation":
            return f"""You are validating the coherence and flow of the paper structure.

Review the framework for logical flow, appropriate transitions, and overall coherence.

Framework: {moves_summary}
Topic: {topic}

Identify any structural issues and recommend improvements."""

        else:
            return f"""You are working on {phase} for detailed outline development.
            
Context: {topic}
Key moves: {moves_summary}
            
Provide guidance for this phase of outline development."""

    def get_user_prompt(self, phase: str, moves_text: str, **kwargs) -> str:
        """Get user prompt for specific planning phase"""
        
        if phase == "framework_integration":
            return f"""Transform these key moves into a structural framework for an Analysis journal paper.

<ANALYSIS_COMPLIANCE_REQUIRED>
Your framework MUST demonstrate Analysis journal mastery through these specific patterns:
</ANALYSIS_COMPLIANCE_REQUIRED>

## DEVELOPED KEY MOVES:
{moves_text}

<ANALYSIS_STRUCTURAL_EXAMPLES_MANDATORY>
Follow these EXACT patterns from recent Analysis papers:

<EXAMPLE_1_DIRECT_ENGAGEMENT>
**REQUIRED Opening Style** (Analysis paper):
"Microaggressions – for example, members of racial minorities being asked 'Where are you really from?' – are common, apparently unintentional and minor remarks..."

**YOUR TASK**: Create similar immediate concrete engagement for your topic
</EXAMPLE_1_DIRECT_ENGAGEMENT>

<EXAMPLE_2_CONVERSATIONAL_FLOW>
**REQUIRED Argument Style**:
"More interestingly, what if Sarah is clear that the question 'Where are you really from?' does help sustain oppression? If so, she does not experience ambiguity in that sense..."

**YOUR TASK**: Use this conversational, case-driven approach throughout
</EXAMPLE_2_CONVERSATIONAL_FLOW>

<EXAMPLE_3_SYSTEMATIC_ORGANIZATION>
**REQUIRED Section Structure**:
"2.1 Ambiguity and clarity
2.2 Wrongdoing, apology and what matters  
2.3 Ambiguity for the wrong reasons
2.4 Bystanders"

**YOUR TASK**: Create descriptive, specific subsection titles (NOT generic ones)
</EXAMPLE_3_SYSTEMATIC_ORGANIZATION>

<EXAMPLE_4_LITERATURE_INTEGRATION>
**REQUIRED Citation Style**:
"Regina Rini (2020) has developed an account of microaggressions that focuses on the experience of victims. She argues that this avoids epistemic problems..." [then immediate engagement with the view]

**YOUR TASK**: Integrate literature naturally into argument flow, never isolate in separate section
</EXAMPLE_4_LITERATURE_INTEGRATION>
</ANALYSIS_STRUCTURAL_EXAMPLES_MANDATORY>

<FRAMEWORK_REQUIREMENTS>
Your framework output MUST include:

1. **EXAMPLE-FIRST OPENING**: Specify concrete case/scenario to open the paper
2. **NO LITERATURE REVIEW SECTION**: Literature woven throughout argument sections
3. **CONVERSATIONAL TRANSITIONS**: "Consider", "More interestingly", "This suggests" style
4. **NAMED EXAMPLES**: Specific characters/cases in multiple sections
5. **DESCRIPTIVE SECTION TITLES**: Avoid generic academic titles

**COMPLIANCE TEST**: Can you point to specific Analysis patterns implemented in your framework?
</FRAMEWORK_REQUIREMENTS>

Create a framework that captures this Analysis style while organizing your specific key moves effectively."""

        else:
            return f"""Please work on {phase} for these key moves:

{moves_text}

Provide detailed guidance for this planning phase.""" 