from typing import Dict, Any

from src.phases.core.base_worker import WorkerInput, WorkerOutput
from src.phases.core.worker_types import CriticWorker
from src.phases.phase_three.stages.stage_one.prompts.section_writing.section_writing_prompts import (
    SectionWritingPrompts,
)


class SectionCriticWorker(CriticWorker):
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = SectionWritingPrompts()
        self._state = {"iterations": 0, "previous_critiques": []}
        self.stage_name = "section_critic"

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        return self.construct_critic_prompt(
            writing_context=input_data.context["writing_context"],
            section_index=input_data.parameters["section_index"],
            current_content=input_data.context["current_section_content"],
            paper_overview=input_data.context["paper_overview"]
        )

    def construct_critic_prompt(self, writing_context: Dict[str, Any], section_index: int, 
                              current_content: str, paper_overview: Dict[str, Any]) -> str:
        """Generate prompt for critiquing a section"""
        
        section = writing_context["sections"][section_index]
        
        # Create section context
        previous_sections = []
        upcoming_sections = []
        
        for i, s in enumerate(writing_context["sections"]):
            if i < section_index:
                previous_sections.append(f"{i+1}. {s['section_name']}")
            elif i > section_index:
                upcoming_sections.append(f"{i+1}. {s['section_name']}")
        
        previous_context = "\n".join(previous_sections) if previous_sections else "None (this is the first section)"
        upcoming_context = "\n".join(upcoming_sections) if upcoming_sections else "None (this is the final section)"
        
        return f"""
You are a philosophy journal reviewer providing detailed critique of a paper section. Your task is to evaluate the philosophical rigor, argument structure, transitions, and overall contribution of this specific section to the paper's thesis.

PAPER OVERVIEW:
Thesis: {paper_overview['thesis']}
Target Length: {paper_overview['target_words']} words total

SECTION BEING EVALUATED:
Section {section_index + 1}: {section['section_name']}
Target Words: {section['word_target']}
Expected Content: {section['content_guidance']}

STRUCTURAL CONTEXT:
Previous Sections:
{previous_context}

Upcoming Sections:
{upcoming_context}

CURRENT SECTION CONTENT:
{current_content}

EVALUATION CRITERIA:
Your critique should assess:

1. PHILOSOPHICAL RIGOR
   - Are arguments clearly stated and well-supported?
   - Is the reasoning valid and sound?
   - Are key concepts properly defined and used consistently?
   - Are citations appropriate and sufficient?

2. STRUCTURAL INTEGRATION
   - Does the section advance the paper's main thesis?
   - Are transitions smooth from previous sections?
   - Does it set up upcoming sections effectively?
   - Is the section's role in the overall argument clear?

3. CLARITY AND PRECISION
   - Is the writing clear and accessible?
   - Are technical terms properly explained?
   - Is the argument structure easy to follow?
   - Are examples illuminating and relevant?

4. SCOPE AND FOCUS
   - Does the section stay within its intended scope?
   - Is the word count appropriate for the content?
   - Are there unnecessary tangents or missing elements?
   - Is the level of detail appropriate?

OUTPUT FORMAT:

# Scratch Work
[Your preliminary analysis and notes]

# Section Analysis

## Philosophical Content Assessment
[Evaluate argument quality, conceptual clarity, citations]

## Structural Integration Assessment  
[Evaluate how well this section fits in the paper's flow]

## Writing Quality Assessment
[Evaluate clarity, precision, accessibility]

## Scope and Focus Assessment
[Evaluate whether section achieves its intended purpose]

# Critical Issues Identified

## Major Issues
[Significant problems that undermine the section's effectiveness]

## Minor Issues  
[Areas for improvement that would strengthen the section]

## Positive Elements
[What works well in this section]

# Transition Analysis

## Opening Transition
[How well does this section connect to what came before?]

## Internal Flow
[How well do the paragraphs within this section connect?]

## Closing Transition
[How well does this section set up what comes next?]

# Improvement Recommendations

## Content Revisions
[Specific changes to strengthen arguments or clarify concepts]

## Structural Revisions
[Changes to improve integration with overall paper]

## Writing Revisions
[Changes to improve clarity and accessibility]

# Summary Assessment
[Overall judgment: MAJOR REVISION NEEDED, MINOR REFINEMENT NEEDED, or MINIMAL CHANGES NEEDED]

Be thorough in your analysis while focusing on actionable feedback that will improve the section's contribution to the overall paper.
"""

    def process_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare input for section critique"""
        section_index = state.get("section_index", 0)
        
        return WorkerInput(
            context={
                "writing_context": state["writing_context"],
                "current_section_content": state["current_section_content"],
                "paper_overview": state["writing_context"]["paper_overview"],
            },
            parameters={
                "section_index": section_index,
                "stage": "section_critic",
                "iteration": self._state["iterations"],
            },
        )

    def process_output(self, response: str) -> WorkerOutput:
        """Process critique response into structured output"""
        try:
            # Update state
            self._state["iterations"] += 1
            self._state["previous_critiques"].append(response)

            # Extract summary assessment
            summary_assessment = self._extract_summary_assessment(response)
            
            # Extract critical issues
            critical_issues = self._extract_critical_issues(response)

            return WorkerOutput(
                modifications={
                    "content": response.strip(),
                    "summary_assessment": summary_assessment,
                    "critical_issues": critical_issues,
                    "iteration": self._state["iterations"],
                },
                notes={
                    "assessment_level": summary_assessment,
                    "major_issues_count": len(critical_issues.get("major", [])),
                    "minor_issues_count": len(critical_issues.get("minor", [])),
                },
                status="completed",
            )

        except Exception as e:
            return WorkerOutput(
                modifications={},
                notes={"error": f"Failed to process critique response: {str(e)}"},
                status="failed",
            )

    def _extract_summary_assessment(self, response: str) -> str:
        """Extract the summary assessment from the critique"""
        try:
            summary_section = response.split("# Summary Assessment")[-1].strip()
            
            if "MAJOR REVISION NEEDED" in summary_section:
                return "MAJOR_REVISION"
            elif "MINOR REFINEMENT NEEDED" in summary_section:
                return "MINOR_REFINEMENT"
            elif "MINIMAL CHANGES NEEDED" in summary_section:
                return "MINIMAL_CHANGES"
            else:
                return "UNCLEAR"
        except:
            return "UNCLEAR"

    def _extract_critical_issues(self, response: str) -> Dict[str, list]:
        """Extract major and minor issues from the critique"""
        try:
            issues_section = response.split("# Critical Issues Identified")[1].split("#")[0]
            
            major_issues = []
            minor_issues = []
            
            if "## Major Issues" in issues_section:
                major_content = issues_section.split("## Major Issues")[1].split("##")[0]
                major_issues = [line.strip() for line in major_content.split("\n") if line.strip() and not line.startswith("[")]
            
            if "## Minor Issues" in issues_section:
                minor_content = issues_section.split("## Minor Issues")[1].split("##")[0]
                minor_issues = [line.strip() for line in minor_content.split("\n") if line.strip() and not line.startswith("[")]
            
            return {"major": major_issues, "minor": minor_issues}
        except:
            return {"major": [], "minor": []}

    def validate_output(self, output: WorkerOutput) -> bool:
        """Verify output meets requirements"""
        print("\nValidating section critique...")

        if not output.modifications:
            print("Failed: No modifications returned")
            return False

        content = output.modifications.get("content", "")
        if not content:
            print("Failed: No content in critique")
            return False

        # Check for required sections
        required_sections = [
            "# Scratch Work",
            "# Section Analysis", 
            "# Critical Issues Identified",
            "# Transition Analysis",
            "# Improvement Recommendations",
            "# Summary Assessment",
        ]

        missing_sections = [section for section in required_sections if section not in content]
        if missing_sections:
            print(f"Failed: Missing required sections: {missing_sections}")
            return False

        # Check for subsections within Section Analysis
        analysis_subsections = [
            "## Philosophical Content Assessment",
            "## Structural Integration Assessment",
            "## Writing Quality Assessment", 
            "## Scope and Focus Assessment",
        ]
        
        missing_analysis = [sub for sub in analysis_subsections if sub not in content]
        if missing_analysis:
            print(f"Failed: Missing analysis subsections: {missing_analysis}")
            return False

        # Verify summary assessment is valid
        summary_assessment = output.modifications.get("summary_assessment", "")
        if summary_assessment not in ["MAJOR_REVISION", "MINOR_REFINEMENT", "MINIMAL_CHANGES"]:
            print(f"Failed: Invalid summary assessment: {summary_assessment}")
            return False

        print(f"Critique validation passed! Assessment: {summary_assessment}")
        return True 