import json
from typing import Dict, Any, List
from src.utils.prompt_utils import load_and_combine_style_guides


class WritingOptimizationPrompts:
    """Prompts for the writing optimization worker in Phase II.8"""
    
    def __init__(self):
        style_guide = load_and_combine_style_guides()
        self.system_prompt = f"""{style_guide}

You are a master writing coach specializing in Analysis-style philosophy papers. Your role is to prepare comprehensive writing aids that make it easy for writers to produce elegant, sophisticated philosophical prose. You excel at:
- Creating memorable hooks and opening lines
- Crafting smooth transitions between ideas
- Generating conversational yet rigorous philosophical prose
- Turning complex arguments into accessible narratives
- Ensuring every writing aid follows Analysis journal conventions"""

        # Quality standards from II.5 for writing optimization
        self.hajek_heuristics = """
<hájek_heuristics_for_writing>
Ensure all writing aids support arguments that pass these tests:

1. EXTREME CASE TEST: Do suggested phrasings handle boundary cases?
2. SELF-UNDERMINING CHECK: Do any recommendations defeat themselves?
3. COUNTEREXAMPLE GENERATION: What obvious objections do the suggested approaches invite?
4. HIDDEN ASSUMPTIONS: What controversial premises do the writing patterns assume?
5. DOMAIN TRANSFER: Would these writing strategies work in parallel philosophical contexts?

All writing aids should support philosophically rigorous argumentation.
</hájek_heuristics_for_writing>"""

        self.anti_rlhf_writing = """
<anti_rlhf_writing_standards>
All writing aids must eliminate RLHF-induced weaknesses:
- NO HEDGING: Provide phrases for clear position-taking, not exploration
- NO SURVEY STYLE: Focus on original argument presentation, not literature review
- NO FALSE BALANCE: Don't provide equal phrasing for weak and strong positions
- CONTROVERSIAL IMPLICATIONS: Include bold phrasing for drawing strong conclusions
- CLEAR STANCES: Every suggested phrase should advance definite philosophical positions

Good writing aids enable intellectual courage, not diplomatic evasion.
</anti_rlhf_writing_standards>"""

        self.philosophical_moves_focus = """
<philosophical_moves_integration>
When creating writing aids, prioritize support for sophisticated philosophical moves:
- Provide phrasing that makes complex arguments accessible
- Include transitions that highlight elegant argumentative turns
- Create hooks that set up genuine philosophical problems
- Suggest conclusions that crystallize important insights
- Focus on moves that would impress Analysis journal readers

Writing aids should enable publication-quality philosophical sophistication.
</philosophical_moves_integration>"""

    def get_hooks_prompt(self, thesis: str, contribution: str) -> str:
        """Generate prompt for creating introduction hooks"""
        
        return f"""<task>
Generate 4-5 compelling introduction hooks for a philosophy paper. Each hook should draw the reader in immediately while setting up the thesis in an engaging way.
</task>

{self.hajek_heuristics}

{self.anti_rlhf_writing}

{self.philosophical_moves_focus}

<thesis>
{thesis}
</thesis>

<core_contribution>
{contribution}
</core_contribution>

<requirements>
1. Each hook should be 2-4 sentences maximum
2. Use one of these Analysis-approved patterns:
   - Striking example or case
   - Counterintuitive claim
   - Philosophical puzzle or paradox
   - Direct challenge to conventional wisdom
   - Vivid scenario that illustrates the problem
3. Avoid:
   - Generic "Since the dawn of time" openings
   - Dense technical language in the first sentence
   - Apologetic or hedging language
   - Survey-style "Various philosophers have argued..."
4. Make it conversational but intellectually engaging
5. Each hook should naturally lead to stating the thesis
</requirements>

<output_format>
{{
    "hooks": [
        {{
            "hook_type": "example | paradox | challenge | scenario | puzzle",
            "text": "The actual hook text that would open the paper.",
            "transition_to_thesis": "How this hook naturally leads to presenting the thesis."
        }}
    ]
}}
</output_format>"""

    def get_transitions_prompt(self, outline: Dict[str, Any], moves: List[Dict[str, Any]]) -> str:
        """Generate prompt for creating section transitions"""
        
        sections_summary = []
        for key, section in outline.items():
            if isinstance(section, dict) and "title" in section:
                sections_summary.append(f"- {key}: {section['title']}")
        
        return f"""<task>
Generate smooth, intellectually engaging transitions between the sections of this philosophy paper. Each transition should create narrative momentum while clearly signaling the argumentative progression.
</task>

{self.anti_rlhf_writing}

{self.philosophical_moves_focus}

<sections>
{chr(10).join(sections_summary)}
</sections>

<requirements>
1. Transitions should be 1-2 sentences that:
   - Summarize what was just established
   - Preview what's coming next
   - Show why this progression is necessary
2. Use Analysis-style transitional patterns:
   - "This raises an immediate question..."
   - "But this account faces a challenge..."
   - "To see why this matters, consider..."
   - "This suggests a deeper point..."
3. Avoid mechanical transitions like:
   - "In the next section..."
   - "Having discussed X, I now turn to Y"
   - "The remainder of this paper..."
4. Make transitions feel like natural turns in philosophical thinking
</requirements>

<output_format>
{{
    "transitions": {{
        "into_section_2": "Transition from introduction into first main section",
        "from_section_2": "Transition out of first main section",
        "into_section_3": "Transition into second main section",
        "from_section_3": "Transition out of second main section",
        "into_section_4": "Transition into third main section",
        "from_section_4": "Transition out of third main section",
        "into_conclusion": "Transition into conclusion"
    }}
}}
</output_format>"""

    def get_integration_prompt(self, moves: List[Dict[str, Any]], outline: Dict[str, Any]) -> str:
        """Generate prompt for move integration guidance"""
        
        moves_summary = []
        for i, move in enumerate(moves):
            moves_summary.append(f"Move {i}: {move.get('key_move_text', 'No description')}")
            
        return f"""<task>
For each philosophical move, provide specific guidance on how to integrate it smoothly into the paper's narrative flow. Focus on making abstract arguments concrete and memorable.
</task>

{self.hajek_heuristics}

{self.anti_rlhf_writing}

{self.philosophical_moves_focus}

<moves>
{chr(10).join(moves_summary)}
</moves>

<requirements>
For each move, provide:
1. **Setup guidance**: How to prepare the reader for this move
2. **Presentation style**: How to make the argument memorable and engaging
3. **Example suggestions**: What kind of example would best illustrate this point
4. **Rhetorical strategies**: Specific phrases or approaches that work well
5. **Common pitfalls**: What to avoid when presenting this move

Focus on Analysis journal style:
- Use concrete examples to drive abstract points
- Maintain conversational directness
- Create "aha" moments of philosophical insight
- Avoid dense technical exposition
</requirements>

<output_format>
{{
    "integration_guidance": [
        {{
            "move_index": 0,
            "setup": "How to prepare the reader for this move",
            "presentation_style": "Conversational approach to presenting the argument",
            "example_pattern": "Type of example that would work well",
            "key_phrases": ["Memorable ways to express the core insight"],
            "avoid": ["Common mistakes when presenting this type of argument"]
        }}
    ]
}}
</output_format>"""

    def get_phrase_banks_prompt(self) -> str:
        """Generate prompt for Analysis-style phrase banks"""
        
        return f"""<task>
Generate phrase banks for common philosophical moves in Analysis style. These should help writers maintain the journal's distinctive conversational yet rigorous tone.
</task>

{self.anti_rlhf_writing}

{self.philosophical_moves_focus}

<requirements>
Create phrase variations for these common moves:
1. **Introducing objections** (without hedging)
2. **Making controversial claims** (with confidence)
3. **Presenting examples** (vividly and efficiently)
4. **Drawing implications** (boldly but precisely)
5. **Acknowledging limits** (without undermining the argument)
6. **Engaging other philosophers** (respectfully but directly)

Each phrase should:
- Be direct and conversational
- Avoid hedging or apologetic language
- Sound natural when read aloud
- Advance the argument efficiently
</requirements>

<output_format>
{{
    "phrase_banks": {{
        "introducing_objections": [
            "The obvious worry is that...",
            "Critics will immediately point out that...",
            "This faces a serious challenge:..."
        ],
        "making_claims": [
            "I argue that...",
            "This shows that...",
            "The upshot is clear:..."
        ],
        "presenting_examples": [
            "Consider...",
            "Take the case of...",
            "To see why, imagine..."
        ],
        "drawing_implications": [
            "This has a striking consequence:...",
            "What follows is surprising:...",
            "This commits us to..."
        ],
        "acknowledging_limits": [
            "This argument applies specifically to...",
            "My claim is limited to...",
            "I'm not arguing that..."
        ],
        "engaging_others": [
            "Where X goes wrong is...",
            "X is right that... but misses...",
            "This improves on X's account by..."
        ]
    }}
}}
</output_format>"""

    def get_conclusion_prompt(self, thesis: str) -> str:
        """Generate prompt for conclusion options"""
        
        return f"""<task>
Generate 3-4 compelling conclusion clinchers for this philosophy paper. Each should leave the reader with a memorable final thought while reinforcing the thesis.
</task>

{self.anti_rlhf_writing}

{self.philosophical_moves_focus}

<thesis>
{thesis}
</thesis>

<requirements>
1. Each conclusion should be 2-3 sentences that:
   - Crystallize the main insight memorably
   - Suggest broader implications
   - End with intellectual punch
2. Use these Analysis-approved ending strategies:
   - Return to opening example with new understanding
   - Pose a thought-provoking question that follows from the argument
   - State a surprising implication
   - Offer a memorable reformulation of the thesis
3. Avoid:
   - "In conclusion..." or "To summarize..."
   - Mere repetition of what was argued
   - Introducing entirely new ideas
   - Apologetic qualifications
   - Calls for "further research"
</requirements>

<output_format>
{{
    "conclusion_options": [
        {{
            "strategy": "return_to_opening | provocative_question | surprising_implication | memorable_reformulation",
            "text": "The actual conclusion text.",
            "why_it_works": "Brief explanation of why this ending is effective."
        }}
    ]
}}
</output_format>"""

    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.system_prompt 