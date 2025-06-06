# src/stages/phase_two/stages/stage_one/prompts.py

from typing import Dict
import json


class InitialReadPrompts:
    """Prompts for initial paper reading with two-stage approach"""

    def __init__(self):
        self.system_prompt = """You are an expert philosophy researcher conducting deep analytical reading of academic papers. You excel at:
1. Identifying core philosophical arguments and their structure
2. Extracting quotable passages with precise citations
3. Recognizing opportunities for philosophical engagement
4. Understanding dialectical positioning within debates
5. Maintaining accuracy in quotes and page references

IMPORTANT: You are part of an automated philosophy paper generation pipeline. Your output will be parsed by code and used by other AI agents in subsequent stages. Any formatting errors will cause the pipeline to fail."""

        self.critical_reading_requirements = """
PHILOSOPHICAL SKEPTICISM REQUIREMENTS (Hájek-style):

When reading papers, actively identify weaknesses:

1. EXTREME CASE VULNERABILITIES
   - Where do arguments break at boundaries?
   - What limit cases does the author avoid discussing?
   - Quote specific claims that fail under extreme conditions

2. SELF-UNDERMINING POTENTIAL
   - Does the paper's method contradict its conclusion?
   - Would the thesis exclude itself if applied strictly?
   - Note any reflexivity problems

3. HIDDEN ASSUMPTIONS
   - What does the argument assume without argument?
   - Which "obvious" premises might be controversial?
   - Identify unstated modal/temporal/causal assumptions

4. COUNTEREXAMPLE OPPORTUNITIES
   - For each universal claim, what's the obvious exception?
   - Where would a hostile reader immediately object?
   - What cases would a grad student raise in Q&A?

5. DOMAIN TRANSFORMATION FAILURES
   - Would this reasoning work in parallel cases?
   - If this is about space, what about time? If about time, what about modality?
   - Where does the analogy break down?

Don't just summarize - INTERROGATE. Read like a hostile referee who wants to find problems.
Your job is not to appreciate but to identify philosophical weaknesses we can address or avoid.
"""

        self.pipeline_context = """
PIPELINE CONTEXT:
You are Stage 1 of an automated philosophy paper generation system. Your JSON output will be:
1. Parsed by Python code using json.loads()
2. Passed to other AI agents for project-specific analysis
3. Eventually integrated into a complete philosophy paper
4. Used to make decisions about literature engagement

Therefore, it is CRITICAL that your output is valid, parseable JSON with no extraneous text."""

        self.json_formatting_rules = """
CRITICAL JSON FORMATTING RULES:
- Output ONLY valid JSON, no explanatory text before or after
- Start your response with { or [
- End your response with } or ]
- Use double quotes for ALL strings
- Escape special characters: \", \\, \n, \r, \t
- No trailing commas
- No comments (// or /* */)
- Numbers and booleans should NOT be quoted
- Ensure all brackets and braces are properly closed
- VERIFY your JSON is valid before outputting

REMEMBER: Invalid JSON will break the automated pipeline and prevent paper generation."""

        # Stage 1: Quote extraction
        self.quote_extraction_template = """<context>
{pipeline_context}
</context>

<requirements>
{critical_reading}
</requirements>

<task>
First Pass: Extract Key Quotations
</task>

<instructions>
Read through the paper and extract 8-12 key quotations total that cover:

CONTENT QUOTES (5-7 quotes):
1. Main thesis or claims statements
2. Key concept definitions or distinctions
3. Crucial arguments or examples
4. Acknowledgments of limitations or objections
5. Positioning relative to other philosophers

VULNERABILITY QUOTES (3-5 quotes):
6. Claims vulnerable to extreme case objections
7. Hidden assumptions or undefended premises
8. Potential self-undermining elements
9. Places where counterexamples seem obvious

For each quote:
- Include the EXACT text in quotation marks
- Note the page number
- Add a brief note about why this quote matters
</instructions>

{json_rules}

<output_format>
{{
    "quotes": [
        {{
            "number": 1,
            "text": "Exact quote text here",
            "page": "page number",
            "context": "Brief context of where this appears",
            "significance": "Why this quote matters",
            "type": "thesis|argument|definition|objection|positioning"
        }}
    ]
}}
</output_format>

Your quotes will be used by the next stage to conduct deep philosophical analysis."""

        # Stage 2: Deep analysis using quotes
        self.analysis_template = """<context>
{pipeline_context}
</context>

<task>
Second Pass: Philosophical Analysis
</task>

<extracted_quotes>
Here are the key quotes from the paper:
{quotes}
</extracted_quotes>

<analysis_tasks>
1. THESIS AND ARGUMENT STRUCTURE
   - State the main thesis (cite quote numbers)
   - Map the argument structure using the quotes
   - Identify the philosophical problem being addressed
   
2. KEY MOVES AND INNOVATIONS
   - What novel philosophical moves does the author make?
   - How do they advance beyond existing positions?
   - What conceptual distinctions do they introduce?
   
3. DIALECTICAL POSITIONING
   - Which philosophers/positions do they engage? (cite quotes)
   - What objections do they anticipate?
   - What objections do they miss?
   
4. ENGAGEMENT OPPORTUNITIES
   Using specific quotes as jumping-off points:
   - Where could we push their argument further?
   - What counterexamples might challenge their view?
   - What implications haven't they explored?
   - Where might their distinctions break down?
   
5. TERMINOLOGY AND CONCEPTS
   - Key technical terms (with quote references)
   - Important distinctions made
   - Conceptual framework employed
</analysis_tasks>

{json_rules}

<output_format>
{{
    "paper_info": {{
        "title": "exact paper title",
        "authors": ["list of authors"],
        "publication_info": {{
            "year": "year of publication",
            "venue": "journal or conference name",
            "doi": "doi if available"
        }}
    }},
    "thesis": {{
        "statement": "clear articulation of main thesis",
        "supporting_quotes": [1, 3, 5],
        "philosophical_problem": "what problem this addresses"
    }},
    "argument_structure": {{
        "main_premises": [
            {{
                "premise": "statement of premise",
                "quote_support": [2, 4],
                "role": "how this supports the thesis"
            }}
        ],
        "key_moves": [
            {{
                "move": "description of philosophical move",
                "innovation": "what's novel about this",
                "quote_refs": [6, 7]
            }}
        ],
        "conclusion": "how the argument concludes"
    }},
    "dialectical_context": {{
        "engages_with": [
            {{
                "philosopher": "name",
                "position": "their view",
                "engagement_type": "agrees|disagrees|extends|modifies",
                "quote_refs": [8]
            }}
        ],
        "anticipated_objections": ["list of objections author considers"],
        "missed_objections": ["objections author doesn't consider"]
    }},
    "engagement_opportunities": [
        {{
            "type": "extension|challenge|application|refinement",
            "description": "specific opportunity",
            "relevant_quotes": [3, 9],
            "development_strategy": "how we might pursue this"
        }}
    ],
    "key_concepts": [
        {{
            "term": "technical term",
            "definition": "how defined",
            "quote_ref": 10,
            "usage": "how it functions in argument"
        }}
    ],
    "methodological_notes": "approach and methods used",
    "scholarly_significance": "why this paper matters to the field"
}}
</output_format>

Your analysis will be used to determine how to engage with this paper in our own philosophical work."""

    def get_system_prompt(self):
        """Return the system prompt for API calls"""
        return self.system_prompt

    def get_prompt(self, paper_path: str, stage: str = "full") -> str:
        """Generate prompt for paper reading"""
        if stage == "quotes":
            return self.quote_extraction_template.replace(
                "{json_rules}", self.json_formatting_rules
            ).replace(
                "{pipeline_context}", self.pipeline_context
            ).replace(
                "{critical_reading}", self.critical_reading_requirements
            )
        elif stage == "analysis":
            # This will be called with quotes already extracted
            return self.analysis_template.replace(
                "{json_rules}", self.json_formatting_rules
            ).replace(
                "{pipeline_context}", self.pipeline_context
            ).replace(
                "{critical_reading}", self.critical_reading_requirements
            )
        else:
            # For backward compatibility, combine both stages
            combined = f"""You are reading an academic philosophy paper. This is a two-stage process:

{self.pipeline_context}

STAGE 1: Quote Extraction
{self.quote_extraction_template}

STAGE 2: Deep Analysis
After extracting quotes, conduct a deep philosophical analysis using those quotes as anchors for your interpretation.

{self.analysis_template}

Focus on accuracy in quotes and depth in analysis. The quotes should ground your interpretation and provide specific evidence for your analytical claims."""
            return combined.replace(
                "{json_rules}", self.json_formatting_rules
            ).replace(
                "{pipeline_context}", self.pipeline_context
            )


class ProjectSpecificPrompts:
    """Prompts for project-specific paper analysis"""

    def __init__(self):
        self.system_prompt = """You are conducting a focused re-reading of philosophy papers for a specific project. Your expertise includes:
1. Identifying precise connections to project goals
2. Recognizing both agreements and productive disagreements  
3. Finding specific elements that can be developed
4. Assessing engagement priorities

IMPORTANT: You are part of an automated philosophy paper generation pipeline. Your output will be parsed by code and used by other AI agents in subsequent stages. Any formatting errors will cause the pipeline to fail."""

        self.pipeline_context = """
PIPELINE CONTEXT:
You are in the project-specific analysis stage of an automated philosophy paper generation system. Your JSON output will be:
1. Parsed by Python code
2. Combined with analyses of other papers
3. Used to determine literature engagement strategy
4. Integrated into the final paper's arguments

Your assessment will directly influence how the paper engages with this source."""

        self.json_formatting_rules = """
CRITICAL JSON FORMATTING RULES:
- Output ONLY valid JSON, no explanatory text before or after
- Start your response with { or [
- End your response with } or ]
- Use double quotes for ALL strings
- Escape special characters: \", \\, \n, \r, \t
- No trailing commas
- No comments (// or /* */)
- Ensure all brackets and braces are properly closed

REMEMBER: The pipeline depends on valid JSON. Formatting errors will prevent paper generation."""

        self.output_format = """<output_format>
{{
    "paper_info": {{
        "title": "exact paper title",
        "authors": ["list of authors"]
    }},
    "engagement_assessment": {{
        "type": "primary|supporting|background",
        "overall_relevance": "high|medium|low",
        "rationale": "explanation of assessed relevance level"
    }},
    "specific_connections": [
        {{
            "connection_type": "conceptual|methodological|framework|example",
            "paper_element": "specific quote or concept from paper",
            "project_element": "what in our project this connects to",
            "page_ref": "page number if available",
            "strength": "strong|moderate|weak",
            "development_potential": "how we can build on this"
        }}
    ],
    "critical_engagements": [
        {{
            "engagement_type": "agreement|disagreement|extension|refinement",
            "paper_claim": "specific claim from paper",
            "our_position": "our stance on this",
            "philosophical_value": "why this engagement matters",
            "quote_support": "relevant quote if available"
        }}
    ],
    "usable_elements": [
        {{
            "element_type": "argument|example|distinction|method",
            "description": "what we can use",
            "adaptation_needed": "how we need to modify it",
            "integration_point": "where in our project this fits"
        }}
    ],
    "priority_recommendations": {{
        "must_engage": ["elements requiring engagement"],
        "should_engage": ["valuable but optional engagements"],
        "citation_only": ["elements to cite without deep engagement"]
    }}
}}
</output_format>"""

    def get_system_prompt(self):
        """Return the system prompt for API calls"""
        return self.system_prompt

    def get_prompt(self, initial_reading: Dict, final_selection: Dict) -> str:
        """Generate prompt for project-specific reading"""
        # Extract key information from final_selection
        chosen_topic = final_selection["selection"]["selection_analysis"]["selection"][
            "chosen_topic"
        ]
        core_thesis = final_selection["phase_two_setup"]["phase_two_setup"][
            "thesis_development"
        ]["core_thesis"]
        key_moves = final_selection["phase_two_setup"]["phase_two_setup"][
            "thesis_development"
        ]["key_moves"]

        return f"""<task>Project-Specific Analysis</task>

{self.pipeline_context}

<project_context>
Topic: {chosen_topic}
Thesis: {core_thesis}
Key Moves: {json.dumps(key_moves, indent=2)}
</project_context>

<previous_reading>
{json.dumps(initial_reading, indent=2)}
</previous_reading>

<instructions>
Analyze how this paper specifically relates to our project:
1. Identify precise connections between paper elements and project goals
2. Find specific quotes, arguments, or examples we can use
3. Determine where we agree, disagree, or can extend
4. Assess engagement priority levels
5. Map specific integration points

Be precise about page references and quotes where possible.
Focus on actionable connections rather than general relevance.
</instructions>

{self.json_formatting_rules}

{self.output_format}"""


class SynthesisPrompts:
    """Prompts for synthesizing literature analysis"""

    def __init__(self):
        self.system_prompt = """You are synthesizing multiple philosophy paper analyses to create a comprehensive literature foundation for a new paper. You excel at:
1. Identifying patterns and connections across papers
2. Mapping scholarly conversations and debates
3. Finding gaps and opportunities
4. Creating actionable development strategies

IMPORTANT: You are part of an automated philosophy paper generation pipeline. Your outputs will be parsed by code and used to guide the entire paper development process."""

        self.pipeline_context = """
PIPELINE CONTEXT:
You are creating the literature synthesis that will guide all subsequent paper development. Your outputs will:
1. Be parsed as both JSON (for structured data) and Markdown (for narrative guidance)
2. Determine which papers get cited and how deeply
3. Shape the argumentative strategy of the paper
4. Guide the development of key philosophical moves

This synthesis is CRITICAL to the paper's success. Both outputs must be valid and parseable."""

        self.json_formatting_rules = """
CRITICAL JSON FORMATTING RULES:
- For the JSON portion, output ONLY valid JSON
- Start with { and end with }
- Use double quotes for ALL strings
- Escape special characters: \", \\, \n, \r, \t
- No trailing commas
- No comments
- Ensure all brackets and braces are properly closed

The JSON must be parseable by Python's json.loads() function."""

        self.json_format = """<json_output>
{{
    "literature_overview": {{
        "primary_papers": [
            {{
                "title": "paper title",
                "authors": ["authors"],
                "role": "central role in our project",
                "key_engagements": ["specific points we'll engage"],
                "quotes_to_use": ["important quotes with page refs"]
            }}
        ],
        "supporting_papers": [
            {{
                "title": "paper title",
                "role": "supporting role",
                "specific_uses": ["how we'll use this"]
            }}
        ],
        "background_papers": [
            {{
                "title": "paper title",
                "citation_purpose": "why we cite this"
            }}
        ]
    }},
    "conceptual_map": {{
        "central_debates": [
            {{
                "debate": "description of debate",
                "positions": ["position 1", "position 2"],
                "our_stance": "where we stand",
                "papers_involved": ["relevant papers"]
            }}
        ],
        "key_distinctions": [
            {{
                "distinction": "conceptual distinction",
                "source": "paper that introduces it",
                "our_use": "how we'll employ or modify it"
            }}
        ],
        "methodological_approaches": ["approaches seen across papers"]
    }},
    "engagement_strategy": {{
        "agreements": [
            {{
                "claim": "what we agree with",
                "source": "paper and page",
                "building_strategy": "how we build on this"
            }}
        ],
        "disagreements": [
            {{
                "claim": "what we challenge",
                "source": "paper and page",
                "critique_strategy": "our counterargument"
            }}
        ],
        "extensions": [
            {{
                "idea": "what we extend",
                "source": "paper and page",
                "extension_strategy": "how we go beyond"
            }}
        ]
    }},
    "development_priorities": [
        {{
            "priority": "high|medium|low",
            "task": "specific development task",
            "papers_involved": ["relevant papers"],
            "rationale": "why this priority level"
        }}
    ]
}}
</json_output>"""

        self.markdown_template = """<markdown_output>
## Literature Synthesis

### Scholarly Landscape
[Describe the intellectual terrain we're entering, major debates, and how papers relate to each other. Explain where our contribution fits.]

### Central Arguments and Positions
[Map out the key arguments across papers, showing agreements, tensions, and gaps. Use specific quotes and page references.]

### Our Dialectical Position
[Explain how we position ourselves relative to the literature. What do we accept, challenge, extend? Be specific about our moves.]

### Key Concepts and Distinctions
[Identify crucial concepts we'll use or challenge. Show how different papers define/use these concepts.]

### Methodological Considerations
[Discuss philosophical methods seen in the literature and our approach.]

### Development Strategy
[Provide specific guidance for developing our paper, including:
- Which arguments to foreground
- Which objections to anticipate
- How to structure our engagement
- Where to be careful about scope]

### Gaps and Opportunities
[Identify what the literature misses or underdevelops that we can address.]

### Citation Strategy
[Explain which papers need deep engagement vs. brief citation, and why.]

### Potential Challenges
[Anticipate difficulties in literature engagement and suggest solutions.]

### Next Steps
[Specific recommendations for moving into framework development.]
</markdown_output>"""

    def get_system_prompt(self):
        """Return the system prompt for API calls"""
        return self.system_prompt

    def get_prompt(self, paper_readings: Dict, final_selection: Dict) -> str:
        return f"""<task>Literature Synthesis</task>

{self.pipeline_context}

<project_focus>
Thesis: {final_selection.get('current_thesis', '')}
Contribution: {final_selection.get('core_contribution', '')}
Key Moves: {json.dumps(final_selection.get('key_moves', []), indent=2)}
</project_focus>

<paper_analyses>
{json.dumps(paper_readings, indent=2)}
</paper_analyses>

<instructions>
Create a comprehensive synthesis that:
1. Maps the scholarly landscape and debates
2. Positions our project within this landscape
3. Identifies specific engagement points
4. Provides actionable development strategy
5. Highlights key quotes and concepts to use

Output both structured JSON and narrative Markdown analysis.

For the JSON output:
{self.json_formatting_rules}

The markdown can follow after the JSON is complete.
</instructions>

{self.json_format}

{self.markdown_template}

Ensure the synthesis is actionable and specific, with clear guidance for paper development."""
