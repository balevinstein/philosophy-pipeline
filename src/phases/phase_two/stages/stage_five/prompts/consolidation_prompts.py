from typing import Dict, List


class ConsolidationPrompts:
    """Prompts for Phase II.5 intelligent consolidation with comprehensive quality standards"""

    def __init__(self):
        self.system_prompt = """You are a senior philosophy journal editor conducting a comprehensive diagnostic review of paper materials. Your expertise includes identifying philosophical weaknesses, structural issues, and opportunities for improvement while maintaining sharp critical assessment. Your analysis will guide subsequent refinement phases."""

        # Add comprehensive quality standards from earlier phases
        self.hajek_heuristics = """
<hájek_heuristics>
Apply these philosophical rigor tests throughout your diagnostic:

1. EXTREME CASE TEST: Does each argument handle boundary cases?
2. SELF-UNDERMINING CHECK: Do any arguments defeat themselves when applied reflexively?
3. COUNTEREXAMPLE GENERATION: What obvious objection would a grad student raise?
4. HIDDEN ASSUMPTIONS: What controversial premises are smuggled in?
5. DOMAIN TRANSFER: Would this reasoning work in parallel contexts?

For each issue identified, note which heuristic revealed it.
</hájek_heuristics>"""

        self.skeptical_friend_approach = """
<skeptical_friend_approach>
Channel the "helpful asshole" reviewer approach:
- ISOLATE specific problematic claims (quote them exactly)
- ARTICULATE the strongest skeptical objections to each claim
- IDENTIFY philosophical patterns that would trigger rejection
- Be brutally critical but constructive

Remember: You're identifying what would make a hostile reviewer reject this paper.
</skeptical_friend_approach>"""

        self.analysis_journal_patterns = """
<analysis_journal_standards>
Evaluate adherence to Analysis journal conventions:

STRUCTURAL PATTERNS:
- Hook → Thesis → Roadmap structure in introduction
- Clear dialectical positioning (who you engage with and why)
- Immediate thesis statement with "I argue that..."
- Claim → Example → Analysis pattern throughout
- Concessive objection handling ("While X might object...")

STYLISTIC PATTERNS:
- Direct, clear prose without excessive hedging
- Specific philosophical terminology properly deployed
- Active voice and first-person arguments
- Precise word economy (4,000 word limit)

FLAG any sections that violate these patterns.
</analysis_journal_standards>"""

        self.anti_rlhf_standards = """
<anti_rlhf_diagnostic>
Identify where the text falls into RLHF-induced weaknesses:
- Presenting all views as equally plausible instead of defending a position
- Excessive caveats and qualifications that weaken arguments
- "Some philosophers argue..." instead of taking clear stances
- Survey-style coverage instead of focused argumentation
- Hedging language that avoids philosophical commitment

Good philosophy takes positions. Flag sections that explore rather than argue.
</anti_rlhf_diagnostic>"""

        self.philosophical_skepticism = """
<philosophical_skepticism_requirements>
Apply these critical reading standards to identify weaknesses:

1. EXTREME CASE VULNERABILITIES
   - Where do arguments break at boundaries?
   - What limit cases are avoided?
   
2. SELF-UNDERMINING POTENTIAL
   - Does any method contradict its conclusion?
   - Would the thesis exclude itself if applied strictly?
   
3. HIDDEN ASSUMPTIONS
   - What does each argument assume without argument?
   - Which "obvious" premises might be controversial?
   
4. COUNTEREXAMPLE OPPORTUNITIES
   - For each universal claim, what's the obvious exception?
   - Where would a hostile reader immediately object?
   
5. DOMAIN TRANSFORMATION FAILURES
   - Would this reasoning work in parallel cases?
   - Where do analogies break down?
</philosophical_skepticism_requirements>"""

    def construct_prompt(
        self,
        abstract: str,
        framework: Dict,
        key_moves: List[Dict],
        detailed_outline: str,
    ) -> str:
        context = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.5 (Intelligent Consolidation).
You must synthesize all outputs from previous phases into a unified diagnostic view.
The main thesis is: {framework.get('main_thesis', 'Not specified')}
The core contribution is: {framework.get('core_contribution', 'Not specified')}

Your consolidation should:
1. Create a coherent vision of the paper's philosophical project
2. Identify tensions, gaps, and redundancies across components
3. Provide specific, actionable diagnostics using all quality standards
4. Focus on medium-level improvements (not minor edits or complete rewrites)
</context>

{self.hajek_heuristics}

{self.skeptical_friend_approach}

{self.analysis_journal_patterns}

{self.anti_rlhf_standards}

{self.philosophical_skepticism}

<task>
Perform comprehensive diagnostic analysis of all Phase II outputs. Apply all quality standards rigorously. Be thorough, critical, and constructive. Your diagnostic work enables effective refinement in subsequent phases.
</task>

<diagnostic_framework>
## 1. THESIS-ARGUMENT ALIGNMENT
Evaluate whether all components work together to support the main thesis.
- Do key moves directly advance the thesis or drift into tangential territory?
- Are there arguments that accidentally undermine the main claim?
- Is the thesis consistently interpreted across all sections?
- Apply the SELF-UNDERMINING CHECK: Does anything contradict the thesis?

## 2. KEY MOVE COHERENCE
Assess how well the key moves work together as a philosophical unit.
- Do moves build on each other or exist in isolation?
- Are there logical dependencies that aren't acknowledged?
- Do any moves contradict each other?
- Apply DOMAIN TRANSFER TEST: Do parallel moves use consistent reasoning?

## 3. PHILOSOPHICAL RIGOR ASSESSMENT
Apply all Hájek heuristics and skeptical friend standards:
- EXTREME CASES: Which arguments fail at boundaries?
- COUNTEREXAMPLES: What obvious objections are unaddressed?
- HIDDEN ASSUMPTIONS: Which premises need explicit defense?
- Quote specific problematic claims with exact text
- Note which Analysis journal patterns are violated

## 4. ARGUMENTATIVE GAP ANALYSIS
Identify missing links in the argumentative chain.
- What premises are assumed but not established?
- Which inferential steps need more support?
- Where would a hostile reviewer demand more justification?
- Apply PHILOSOPHICAL SKEPTICISM standards to each gap

## 5. CONCEPTUAL CLARITY EVALUATION
Assess the precision and clarity of philosophical concepts.
- Which terms are used inconsistently across sections?
- What concepts need clearer definition?
- Where is technical terminology misused or vague?
- Check for ANTI-RLHF violations: excessive hedging or qualification

## 6. EXAMPLE AND ILLUSTRATION QUALITY
Evaluate whether examples do real philosophical work.
- Do examples genuinely support their arguments?
- Are any examples merely decorative?
- Which arguments need concrete illustrations?
- Apply the CLAIM→EXAMPLE→ANALYSIS pattern test

## 7. STRUCTURAL ANALYSIS
Assess the overall architecture and flow.
- Does the structure follow Analysis journal conventions?
- Are word count allocations appropriate?
- Do sections flow logically?
- Is the Hook→Thesis→Roadmap pattern properly implemented?

## 8. LITERATURE INTEGRATION DIAGNOSTIC
Evaluate scholarly engagement quality.
- Is literature substantively engaged or merely cited?
- Are the right sources in the right places?
- Any important voices missing from the conversation?
- Check for immediate engagement vs. survey-style coverage
</diagnostic_framework>

<requirements>
1. APPLY ALL QUALITY STANDARDS
   - Use Hájek heuristics on EVERY key move and argument
   - Apply skeptical friend approach to identify rejection triggers
   - Check Analysis journal pattern compliance throughout
   - Flag all anti-RLHF violations (hedging, lack of position-taking)
   - Use philosophical skepticism to find vulnerabilities

2. BE DIAGNOSTICALLY RUTHLESS
   - Quote specific problematic passages
   - Identify claims that would embarrass the author at a conference
   - Find arguments a grad student would immediately challenge
   - Note where the paper explores rather than argues

3. FOCUS ON MEDIUM-LEVEL CHANGES
   This diagnostic should identify:
   - Arguments needing restructuring (not just polish)
   - Concepts requiring clarification (not just definition)
   - Examples needing replacement (not just tweaking)
   - Sections requiring reframing (not complete rewriting)

4. MAINTAIN PHILOSOPHICAL STANDARDS
   - Would this pass Analysis journal peer review?
   - Does each section demonstrate philosophical sophistication?
   - Are arguments at the level of professional philosophy?
   - Is the writing clear, direct, and position-taking?

5. PROVIDE ACTIONABLE DIAGNOSTICS
   For each issue identified:
   - Quote the specific problem
   - Note which quality standard it violates
   - Assess severity (minor tension → major flaw → fatal problem)
   - Indicate the type of fix needed

6. COMPLETE ALL JSON SECTIONS
   Your output MUST include ALL sections specified in the JSON template:
   - consolidated_vision: Overall paper narrative
   - key_move_assessment: Assessment of ALL 5 key moves (indices 0-4)
   - identified_issues: List of specific problems found
   - overall_assessment: Paper readiness evaluation
   - diagnostic_details: Comprehensive quality standard violations
   - priority_recommendations: Ordered list of fixes
   - redundancy_analysis: Repeated content identification
   - gap_analysis: Missing elements
   
   DO NOT skip any section. The pipeline will fail if any section is missing.
</requirements>

<analysis_examples>
Examples of diagnostic findings that demonstrate proper critical assessment:

GOOD DIAGNOSTIC (specific, actionable):
"Key Move 2 claims 'all joint actions require symmetric participation' (line 247) but this fails the EXTREME CASE TEST - consider unconscious cooperation in crowd dynamics. This universal claim needs scope restriction."

GOOD DIAGNOSTIC (pattern violation):
"Section 3.2 violates Analysis CLAIM→EXAMPLE→ANALYSIS pattern by providing three examples in sequence without analysis. Each example needs immediate philosophical unpacking."

GOOD DIAGNOSTIC (anti-RLHF):
"The introduction hedges with 'This paper explores various perspectives on...' instead of taking a clear position. Analysis requires 'I argue that...' with definite thesis commitment."

BAD DIAGNOSTIC (too vague):
"The arguments could be stronger and the examples might need work."

BAD DIAGNOSTIC (too minor):
"Consider changing 'utilize' to 'use' in paragraph 4."

GOOD DIAGNOSTIC (gap identification):
"The move from 'intentions matter' to 'collective intentions determine outcomes' (lines 412-420) assumes without argument that individual intentions aggregate linearly. A hostile referee would demand justification for this controversial premise."
</analysis_examples>

<json_formatting_rules>
CRITICAL JSON FORMATTING RULES:
1. Output ONLY valid JSON - no markdown code blocks, no explanations outside JSON
2. Use double quotes for all strings
3. Escape quotes within text using \"
4. No newlines within string values - replace with spaces
5. Ensure all brackets and braces are properly closed
6. Arrays must use square brackets []
7. The response must be parseable by json.loads()
</json_formatting_rules>

<json_output>
{{
    "consolidated_vision": {{
        "paper_narrative": "Clear story of what this paper accomplishes",
        "thesis_to_conclusion_flow": "How the argument develops from intro to conclusion",
        "key_contributions": ["Main philosophical contributions"],
        "target_audience": "Who would read and cite this paper"
    }},
    "key_move_assessment": [
        {{
            "move_index": 0,
            "move_description": "Brief description of the key move",
            "supports_thesis": true/false,
            "necessity": "essential/useful/redundant",
            "overlaps_with": [indices of other moves if any],
            "recommendation": "keep/modify/eliminate",
            "reasoning": "Why this assessment"
        }}
        // REQUIRED: Include assessment for ALL 5 key moves (indices 0-4)
        // Each move must be evaluated even if recommendation is "eliminate"
    ],
    "identified_issues": [
        {{
            "issue_type": "conceptual/argumentative/structural/example/literature",
            "severity": "critical/major/moderate/minor",
            "location": {{
                "section": "Section number or name",
                "specific_area": "More specific location"
            }},
            "description": "Clear description of the issue",
            "impact": "Why this matters for the paper",
            "proposed_solutions": [
                {{
                    "solution": "Specific solution description",
                    "implementation_difficulty": "easy/medium/hard",
                    "expected_outcome": "What this would achieve"
                }}
            ],
            "priority": "high/medium/low"
        }}
    ],
    "overall_assessment": {{
        "paper_readiness": "far_from_ready/needs_work/nearly_ready",
        "main_strengths": ["What's working well"],
        "main_weaknesses": ["Primary issues to address"],
        "estimated_improvement_effort": "minor_tweaks/moderate_revision/major_work"
    }},
    "diagnostic_details": {{
        "quality_standard_violations": {{
            "hajek_failures": [
                {{
                    "heuristic": "EXTREME_CASE_TEST/SELF_UNDERMINING/etc",
                    "location": "Key Move X, paragraph Y",
                    "quote": "Exact problematic text",
                    "severity": "Minor/Major/Fatal",
                    "fix_needed": "Scope restriction/Argument revision/etc"
                }}
            ],
            "analysis_pattern_violations": [
                {{
                    "pattern": "CLAIM_EXAMPLE_ANALYSIS/HOOK_THESIS_ROADMAP/etc",
                    "location": "Section reference",
                    "issue": "Description of violation",
                    "fix_needed": "Specific correction"
                }}
            ],
            "anti_rlhf_violations": [
                {{
                    "type": "HEDGING/SURVEY_STYLE/NO_POSITION/etc",
                    "location": "Specific section",
                    "quote": "Problematic hedging language",
                    "fix_needed": "Take clear position/Remove hedging/etc"
                }}
            ]
        }},
        "thesis_support_analysis": {{
            "aligned_moves": ["List moves that effectively support thesis"],
            "problematic_moves": [
                {{
                    "move": "Move identifier",
                    "issue": "How it fails to support or contradicts thesis",
                    "severity": "Minor_Drift/Major_Tangent/Direct_Contradiction"
                }}
            ],
            "missing_support": ["Aspects of thesis not covered by any moves"]
        }},
        "argumentative_gaps": {{
            "missing_premises": [
                {{
                    "location": "Between claim X and conclusion Y",
                    "gap": "What's assumed but not established",
                    "hostile_objection": "What a referee would demand"
                }}
            ],
            "undefended_assumptions": [
                {{
                    "assumption": "Stated assumption",
                    "location": "Where it appears",
                    "controversy_level": "Widely_Accepted/Debatable/Highly_Controversial"
                }}
            ]
        }},
        "conceptual_clarity": {{
            "undefined_terms": ["List of technical terms used without definition"],
            "inconsistent_usage": [
                {{
                    "term": "Concept name",
                    "variations": ["Different uses across sections"],
                    "fix_needed": "Standardize definition"
                }}
            ],
            "clarity_problems": ["Vague or ambiguous philosophical claims"]
        }},
        "example_quality": {{
            "effective_examples": ["Examples that genuinely advance arguments"],
            "problematic_examples": [
                {{
                    "example": "Brief description",
                    "location": "Where it appears",
                    "issue": "Decorative/Repetitive/Counterproductive/Unclear",
                    "fix": "Replace/Develop/Remove"
                }}
            ],
            "missing_examples": ["Arguments that need concrete illustration"]
        }},
        "structural_issues": {{
            "flow_problems": ["Sections that don't connect logically"],
            "balance_issues": {{
                "overweight_sections": ["Sections taking disproportionate space"],
                "underdeveloped_sections": ["Sections needing expansion"]
            }},
            "redundancies": ["Content repeated across sections"]
        }},
        "literature_integration": {{
            "substantive_engagement": ["Sources properly engaged with"],
            "superficial_citations": ["Sources merely name-dropped"],
            "missing_voices": ["Important literature not included"],
            "misrepresentations": ["Sources incorrectly characterized"]
        }}
    }},
    "priority_recommendations": [
        {{
            "priority": 1,
            "action": "Most important thing to fix",
            "reason": "Why this is top priority",
            "quality_standard_violated": "Which standard this addresses"
        }}
    ],
    "redundancy_analysis": {{
        "repeated_examples": ["List of overused examples"],
        "repeated_arguments": ["Arguments that appear multiple times"],
        "consolidation_opportunities": ["Where we can merge or streamline"]
    }},
    "gap_analysis": {{
        "missing_arguments": ["Arguments we need but don't have"],
        "missing_examples": ["Types of cases we should add"],
        "missing_literature": ["Key sources we should engage"],
        "missing_objections": ["Obvious counters we haven't addressed"]
    }}
}}
</json_output>

<inputs>
ABSTRACT:
{abstract}

FRAMEWORK (with main thesis and key moves):
{framework}

DEVELOPED KEY MOVES:
{key_moves}

DETAILED OUTLINE:
{detailed_outline}
</inputs>"""

        return context

    def get_consolidation_prompt(
        self,
        literature_synthesis: str,
        abstract_framework: str,
        developed_moves: str,
        detailed_outline: str
    ) -> str:
        """
        Generate the consolidation prompt with provided data
        
        Args:
            literature_synthesis: JSON string of literature synthesis from II.1
            abstract_framework: JSON string of abstract framework from II.2
            developed_moves: JSON string of developed key moves from II.3
            detailed_outline: JSON string of detailed outline from II.4
            
        Returns:
            Complete prompt for consolidation analysis
        """
        # Parse the JSON strings to extract key information
        import json
        
        try:
            framework_data = json.loads(abstract_framework)
            abstract = framework_data.get("abstract", {}).get("content", "")
            framework = {
                "main_thesis": framework_data.get("main_thesis", ""),
                "core_contribution": framework_data.get("core_contribution", ""),
                "key_moves": framework_data.get("key_moves", [])
            }
            
            moves_data = json.loads(developed_moves)
            key_moves = moves_data.get("developed_key_moves", [])
            
        except json.JSONDecodeError:
            # Fallback if parsing fails
            abstract = ""
            framework = {"main_thesis": "", "core_contribution": "", "key_moves": []}
            key_moves = []
        
        # Use the construct_prompt method with extracted data
        return self.construct_prompt(
            abstract=abstract,
            framework=framework,
            key_moves=key_moves,
            detailed_outline=detailed_outline
        )

    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.system_prompt 