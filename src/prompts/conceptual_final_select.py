# src/prompts/conceptual_final_select.py

class FinalSelectionPrompt:
    """Manages prompts for final topic selection and Phase II setup"""
    
    def __init__(self):
        self.SELECTION_CRITERIA = """
PHILOSOPHICAL EVALUATION GUIDANCE:
You will be evaluating topics that have undergone initial development, including literature assessment, argument testing, and refinement proposals. As an experienced philosopher, consider:

1. Philosophical Promise
   - Is there a genuine philosophical insight here?
   - Does the core move feel right/promising?
   - Is there room for sophisticated development?
   - Would other philosophers find this interesting?
   - Is it novel enough?
   - Is it interesting enough?
   - Does it take a firm stand? (Edgy is okay.)

2. Development Potential
   - How well did the test arguments work in development testing?
   - Did the example cases effectively illuminate the core ideas?
   - How promising were the objection/response pairs?
   - Based on previous testing, how viable is the development pathway?
   - Do the proposed refinements strengthen the core contribution?

3. Scholarly Context
   - How well does this fit with existing literature based on assessment?
   - Is the engagement point natural?
   - Are the literature needs manageable?
   - Will this advance the conversation?

Think carefully about which topic has the strongest philosophical core and clearest development pathway, based on the testing and refinement work already done. Consider both the current state of the argument and where it could go."""

        self.PHASE_TWO_GUIDANCE = """
DEVELOPMENT GUIDANCE:
Building on the literature assessment, development testing, and refinements already completed, think as a philosopher planning the paper's development. Consider:

1. Core Development
   - Which aspects of the tested argument need deeper development?
   - Where do the example cases need strengthening or expansion?
   - Which objections from testing require more sophisticated responses?
   - What additional moves might strengthen the core contribution?

2. Literature Interface
   - What specific papers do you clearly remember that would be relevant?
   - Be honest about your memory - only list papers you specifically recall
   - For areas needing search, what kinds of work should we look for?
   - What verification might significantly impact development?

3. Development Strategy
   - Which tested aspects need special attention?
   - What refinements are most critical?
   - Where do we need flexibility in development?
   - What factors are crucial for success?

When identifying literature needs, strictly separate:
1. Papers you specifically remember reading about or seeing referenced
2. Areas where we need to search for relevant work

Do not generate hypothetical paper titles. If you remember reading about work in an area but don't recall specific papers, include this in search requirements."""

        self.SELECTION_OUTPUT_FORMAT = """
OUTPUT FORMAT FOR SELECTION:
Response must be valid JSON matching this exact structure:
{
  "selection_analysis": {
    "comparative_reasoning": {
      "steps": [
        {
          "step": "string",  # Each step in the comparison process
          "consideration": "string",  # What's being compared
          "analysis": "string"  # The actual comparison
        }
      ],
      "key_insights": ["string"]  # Important realizations from comparison
    },
    "comparison": {
      "criteria": [
        {
          "criterion": "string",  # e.g., 'Development Potential'
          "assessment": [
            {
              "topic_title": "string",
              "strength_rating": "high|medium|low",
              "key_factors": ["string"],
              "concerns": ["string"]
            }
          ]
        }
      ]
    },
    "selection": {
      "chosen_topic": "string",  # title of selected topic
      "rationale": "string",
      "key_strengths": ["string"],
      "critical_considerations": ["string"]
    }
  }
}"""

        self.SETUP_OUTPUT_FORMAT = """
OUTPUT FORMAT FOR PHASE II SETUP:
Response must be valid JSON matching this exact structure:
{
  "phase_two_setup": {
    "thesis_development": {
      "core_thesis": "string",
      "key_moves": ["string"],
      "contribution_summary": "string"
    },
    "literature_needs": {
      "remembered_papers": [
        {
          "title": "string (only if you specifically remember the title)",
          "authors": ["string (only authors you specifically remember)"],
          "confidence": {
            "title_accuracy": "high|medium|low",
            "content_memory": "high|medium|low"
          },
          "key_arguments": ["string (specific arguments you remember)"],
          "relevance": "string (how it connects to our project)"
        }
      ],
      "search_requirements": [
        {
          "area": "string (e.g., 'Formal treatments of self-defeat')",
          "key_journals": ["string"],
          "search_guidance": "string",
          "desired_findings": ["string"]
        }
      ],
      "background_knowledge": ["string"]
    },
    "development_guidance": {
      "special_attention_areas": {
        "example_development": {
          "importance": "string",
          "challenges": ["string"],
          "considerations": ["string"]
        },
        "argument_structure": {
          "importance": "string",
          "challenges": ["string"],
          "considerations": ["string"]
        },
        "literature_integration": {
          "importance": "string",
          "challenges": ["string"],
          "considerations": ["string"]
        }
      },
      "initial_structure": {
        "potential_sections": ["string"],
        "key_dependencies": ["string"],
        "flexibility_notes": ["string"]
      }
    },
    "phase_two_considerations": {
      "critical_success_factors": ["string"],
      "development_priorities": ["string"],
      "potential_challenges": ["string"]
    }
  }
}"""

        self.OUTPUT_REQUIREMENTS = """
GENERAL OUTPUT REQUIREMENTS:
1. Response must be valid JSON
2. Use simple ASCII characters only (no special quotes or unicode)
3. Keep all text fields as single-line strings (no line breaks)
4. Be explicit and specific in all assessments
5. Every string field must be a complete, well-formed sentence
6. Array items should be distinct and substantive
7. Maintain consistent detail level across topics"""

    def get_selection_prompt(self, topics_json: str) -> str:
        """Construct prompt for final topic selection"""
        return f"""You are tasked with making the final topic selection for an Analysis journal philosophy paper. Each topic has undergone initial development including literature assessment, argument testing, and refinement proposals. Choose the topic with the strongest philosophical potential based on this development work.

{self.SELECTION_CRITERIA}

{self.OUTPUT_REQUIREMENTS}

{self.SELECTION_OUTPUT_FORMAT}

Here are the developed topics for consideration:
{topics_json}

Think through the comparison systematically and provide a clear rationale for your selection."""

    def get_setup_prompt(self, selected_topic_json: str) -> str:
        """Construct prompt for Phase II setup"""
        return f"""You are preparing the selected philosophy paper topic for detailed development. Building on the existing literature assessment, development testing, and refinement work, create a comprehensive setup that provides clear guidance while maintaining appropriate flexibility for development.

{self.PHASE_TWO_GUIDANCE}

{self.OUTPUT_REQUIREMENTS}

{self.SETUP_OUTPUT_FORMAT}

Here is the selected topic with its development:
{selected_topic_json}

Focus on creating clear literature requirements for human researchers and identifying critical areas needing special attention in future development."""

