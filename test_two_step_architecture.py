#!/usr/bin/env python3
"""
Test script demonstrating the two-step II.5 architecture prototype
"""

import json
from src.phases.phase_two.stages.stage_five.workers.synthesis_worker import SynthesisWorker
from src.phases.phase_two.stages.stage_five.workers.quality_audit_worker import QualityAuditWorker
from src.utils.config import Config

def test_two_step_architecture():
    """Test the two-step architecture with mock data"""
    
    print("=" * 60)
    print("TESTING TWO-STEP II.5 ARCHITECTURE")
    print("=" * 60)
    
    # Load config
    config = Config.load_config()
    
    # Mock state data (simplified for testing)
    mock_state = {
        "abstract_framework": {
            "main_thesis": "Epistemic and moral blame for ignorance involve distinct normative criteria",
            "core_contribution": "Systematic criteria for distinguishing epistemic from moral violations",
            "abstract": {
                "content": "Professional contexts require responsibility judgments about ignorance but current approaches conflate distinct normative considerations..."
            }
        },
        "developed_moves": {
            "developed_key_moves": [
                {"key_move_index": 0, "key_move_text": "Establish conflation problem"},
                {"key_move_index": 1, "key_move_text": "Develop systematic criteria"},
                {"key_move_index": 2, "key_move_text": "Demonstrate genuine normative difference"},
                {"key_move_index": 3, "key_move_text": "Show framework illuminates puzzling features"},
                {"key_move_index": 4, "key_move_text": "Address boundary problem"}
            ]
        },
        "detailed_outline": {
            "introduction": {"word_target": 700, "content_guidance": "Establish professional responsibility problem"},
            "section_2": {"title": "Framework Development", "word_target": 2000},
            "section_3": {"title": "Normative Difference", "word_target": 1400},
            "section_4": {"title": "Literature Integration", "word_target": 1000},
            "section_5": {"title": "Boundary Problems", "word_target": 800},
            "conclusion": {"word_target": 400}
        }
    }
    
    print("\n" + "=" * 40)
    print("STEP 1: QUICK SYNTHESIS (II.5a)")
    print("=" * 40)
    print("Focus: Big picture coherence, major issues only")
    print("Cognitive load: Manageable - 3 simple checks")
    print("Output: Simple JSON with priorities")
    
    # Initialize synthesis worker
    synthesis_worker = SynthesisWorker(config)
    
    # Show what synthesis worker would focus on
    print("\nSynthesis worker focuses on:")
    print("- Do thesis/moves/outline work together?")
    print("- What are the 3-5 most serious issues?")
    print("- What should refinement stages prioritize?")
    print("- NOT: Detailed critique, specific citations, quality standards")
    
    # Mock synthesis results (what II.5a would produce)
    mock_synthesis_results = {
        "coherence_assessment": {
            "overall_coherence": "acceptable",
            "main_story": "Paper distinguishes epistemic from moral blame through systematic criteria",
            "thesis_move_alignment": "Moves generally support thesis but some drift",
            "major_contradictions": []
        },
        "priority_issues": [
            {
                "issue": "Literature integration appears superficial",
                "severity": "major",
                "impact": "Would trigger reviewer rejection",
                "urgency": "fix_first"
            },
            {
                "issue": "Key Move 4 lacks concrete examples",
                "severity": "major", 
                "impact": "Weakens practical applicability claims",
                "urgency": "fix_first"
            },
            {
                "issue": "Boundary section too theoretical",
                "severity": "moderate",
                "impact": "Limits practical relevance",
                "urgency": "address_soon"
            }
        ],
        "refinement_guidance": {
            "immediate_priorities": [
                "Strengthen literature engagement",
                "Add concrete examples to Move 4",
                "Make boundary section more practical"
            ],
            "paper_readiness": "needs_work",
            "main_strengths": [
                "Clear thesis and framework",
                "Good philosophical structure",
                "Relevant professional focus"
            ]
        }
    }
    
    print(f"\nSynthesis results:")
    print(f"- Overall coherence: {mock_synthesis_results['coherence_assessment']['overall_coherence']}")
    print(f"- Priority issues: {len(mock_synthesis_results['priority_issues'])}")
    print(f"- Paper readiness: {mock_synthesis_results['refinement_guidance']['paper_readiness']}")
    
    print("\n" + "=" * 40)
    print("STEP 2: TARGETED QUALITY AUDIT (II.5b)")
    print("=" * 40)
    print("Focus: Apply quality standards to priority issues only")
    print("Cognitive load: Focused - work on specific problems")
    print("Output: Actionable remediation guidance")
    
    # Add synthesis results to state
    mock_state["synthesis_results"] = mock_synthesis_results
    
    # Initialize quality audit worker
    audit_worker = QualityAuditWorker(config)
    
    print("\nQuality audit worker focuses on:")
    print("- Apply Hájek/Anti-RLHF/Analysis standards to priority issues")
    print("- Generate specific fixes for each problem")
    print("- Create roadmap for II.6-8 stages")
    print("- NOT: Comprehensive audit of everything")
    
    # Mock quality audit results (what II.5b would produce)
    mock_audit_results = {
        "priority_analysis": [
            {
                "issue_from_synthesis": "Literature integration appears superficial",
                "quality_violations": [
                    {
                        "standard": "ANALYSIS_STYLE",
                        "specific_problem": "Section 4 cites sources without substantive engagement",
                        "violation_type": "Name-dropping instead of argument development",
                        "severity": "major"
                    }
                ],
                "targeted_fixes": [
                    {
                        "fix_description": "Replace citations with substantive engagement",
                        "implementation_stage": "II.7_refinement",
                        "priority": "urgent"
                    }
                ]
            }
        ],
        "refinement_roadmap": {
            "stage_6_planning_focus": [
                "Plan deeper literature engagement strategy",
                "Identify specific sources for substantive interaction"
            ],
            "stage_7_refinement_targets": [
                "Rewrite Section 4 with genuine engagement",
                "Add concrete examples to Move 4"
            ],
            "stage_8_writing_optimization": [
                "Optimize transitions between literature and arguments"
            ],
            "overall_difficulty": "moderate"
        }
    }
    
    print(f"\nAudit results:")
    print(f"- Priority issues analyzed: {len(mock_audit_results['priority_analysis'])}")
    print(f"- Refinement difficulty: {mock_audit_results['refinement_roadmap']['overall_difficulty']}")
    print(f"- Clear guidance for II.6-8 stages")
    
    print("\n" + "=" * 60)
    print("COMPARISON: TWO-STEP vs CURRENT SINGLE-STEP")
    print("=" * 60)
    
    print("\nCURRENT II.5 (Single Step):")
    print("❌ Cognitive overload - 15+ tasks simultaneously")
    print("❌ Massive JSON output - high failure risk")
    print("❌ Apply ALL quality standards to EVERYTHING")
    print("❌ Context window explosion (~80KB inputs)")
    print("❌ No clear success criteria")
    print("❌ Tries to be comprehensive diagnostic + synthesis + planning")
    
    print("\nNEW II.5 (Two Step):")
    print("✅ Manageable cognitive load - focused tasks")
    print("✅ Simple JSON outputs - lower failure risk")
    print("✅ Apply quality standards to priority issues only")
    print("✅ Smaller context windows per step")
    print("✅ Clear success criteria for each step")
    print("✅ Synthesis THEN audit - logical progression")
    
    print("\n" + "=" * 60)
    print("BENEFITS OF TWO-STEP ARCHITECTURE")
    print("=" * 60)
    
    print("\n1. COGNITIVE MANAGEABILITY")
    print("   - Each step has 3-4 focused tasks")
    print("   - Clear priorities and success criteria")
    print("   - No parallelization anxiety")
    
    print("\n2. BETTER QUALITY")
    print("   - Smaller context windows = better attention")
    print("   - Focused quality standards application")
    print("   - Actionable remediation guidance")
    
    print("\n3. MATCHES VISION")
    print("   - Polish/refinement, not reconstruction")
    print("   - Avoids II.3-4 complexity")
    print("   - Still linear workers, not multi-cycle")
    
    print("\n4. CLEAR WORKFLOW")
    print("   - II.5a: 'What needs fixing?'")
    print("   - II.5b: 'How do we fix it?'")
    print("   - II.6-8: 'Execute the fixes'")
    
    print("\n" + "=" * 60)
    print("PROTOTYPE COMPLETE - READY FOR IMPLEMENTATION")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    test_two_step_architecture() 