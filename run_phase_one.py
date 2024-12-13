# run_phase_one.py

import sys
from pathlib import Path
from src.stages.conceptual_generate import ConceptualTopicGenerator
from src.stages.conceptual_evaluate import ConceptualTopicEvaluator
from src.stages.conceptual_topic_development import ConceptualTopicDeveloper
from src.stages.conceptual_final_select import FinalTopicSelector

def run_phase_one():
    """Run all stages of Phase I in sequence"""
    try:
        print("\nStarting Phase I pipeline...")
        
        # Run each stage in sequence
        generator = ConceptualTopicGenerator()
        topics = generator.run()
        if not topics:
            raise Exception("Topic generation failed")
            
        evaluator = ConceptualTopicEvaluator()
        evaluation = evaluator.run()
        if not evaluation:
            raise Exception("Topic evaluation failed")
            
        developer = ConceptualTopicDeveloper()
        development = developer.run()
        if not development:
            raise Exception("Topic development failed")
            
        selector = FinalTopicSelector()
        selection = selector.run()
        if not selection:
            raise Exception("Final selection failed")
            
        print("\nPhase I completed successfully!")
        return selection
        
    except Exception as e:
        print(f"\nError in Phase I pipeline: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_phase_one()