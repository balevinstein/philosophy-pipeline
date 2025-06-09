from typing import Dict, Any

from src.phases.core.base_worker import WorkerInput, WorkerOutput
from src.phases.core.worker_types import CriticWorker
from src.phases.phase_three.stages.stage_one.prompts.section_writing.section_writing_prompts import (
    SectionWritingPrompts,
)
from src.phases.phase_two.base.framework import ValidationError


class SectionCriticWorker(CriticWorker):
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = SectionWritingPrompts()
        self._state = {"iterations": 0, "previous_critiques": []}
        self.stage_name = "section_critic"

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        return self.prompts.construct_critic_prompt(
            writing_context=input_data.context["writing_context"],
            section_index=input_data.parameters["section_index"],
            current_content=input_data.context["current_section_content"],
            paper_overview=input_data.context["paper_overview"]
        )

    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.prompts.get_critic_system_prompt()

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

    def execute(self, state: Dict[str, Any]) -> WorkerOutput:
        """Execute the critic worker with proper tuple unpacking"""
        input_data = self.process_input(state)
        prompt = self._construct_prompt(input_data)
        system_prompt = self.get_system_prompt()
        
        # Make API call and unpack tuple
        response, _ = self.api_handler.make_api_call(
            stage=self.stage_name,
            prompt=prompt,
            system_prompt=system_prompt
        )
        
        output = self.process_output(response)
        if not self.validate_output(output):
            print(response)
            raise ValidationError("Worker output failed validation: ", self.stage_name)
        return output 