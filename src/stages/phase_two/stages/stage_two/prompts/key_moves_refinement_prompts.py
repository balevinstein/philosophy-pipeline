from typing import Dict, Any
import json

class KeyMovesRefinementPrompts:
    """Prompts for refining key moves based on critique"""
    
    def __init__(self):
        self.CONTEXT = """You are refining key argumentative moves for an Analysis paper (4,000 word limit). Each move must:
1. Advance the paper's main thesis
2. Be concretely developable within space constraints
3. Integrate well with other moves
4. Draw appropriately on available literature

Consider each suggested change carefully, but maintain what works. You should:
- Evaluate each suggestion's merit
- Consider how changes affect move interactions
- Maintain framework alignment
- Preserve effective elements
- Ensure literature support

Remember you can only use the specific papers provided in the literature files - ensure all refinements are supported by these available sources."""




        self.OUTPUT_FORMAT = """Analyze the critique and provide refinements using this structure:

        # Scratch Work
        [Think through the changes being suggested]
        [Consider interactions and dependencies]
        [Evaluate theoretical implications]

        # Refinement Decisions
        [Overall refinement strategy]

        ## Will Implement
        1. [Change] -- [Rationale]
        2. [Change] -- [Rationale]
        ...

        ## Won't Implement
        1. [Change] -- [Rationale]
        2. [Change] -- [Rationale]
        ...

        # Updated Move Development
        [Complete refined version of each move]

        # Change Notes
        - Impact on theoretical foundations
        - Effect on move interactions 
        - Literature integration adjustments
        - Framework alignment status
        - Development feasibility within word constraints
        - Dependencies between refined moves"""
        
    def get_refinement_prompt(self,
                            current_moves: Dict[str, Any],
                            critique: Dict[str, Any],
                            framework: Dict[str, Any],
                            outline: str,
                            lit_readings: Dict[str, Any],
                            lit_synthesis: Dict[str, Any],
                            lit_narrative: str) -> str:
        """Generate prompt for key moves refinement"""
        
        return f"""
{self.CONTEXT}

Current Framework:
{json.dumps(framework, indent=2)}

Current Outline:
{outline}

Current Moves:
{json.dumps(current_moves, indent=2)}

Recent Critique:
{json.dumps(critique, indent=2)}

Literature Context:
{json.dumps(lit_synthesis, indent=2)}

{self.OUTPUT_FORMAT}

Think carefully about how each change affects the moves' ability to support the paper's thesis and their integration with the overall framework."""