import json
import logging
from pathlib import Path
from datetime import datetime
import time

from src.phases.phase_two.stages.stage_eight.workers.writing_optimization_worker import WritingOptimizationWorker
from run_utils import load_config


def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('outputs/logs/phase_2_8_writing_optimization.log'),
            logging.StreamHandler()
        ]
    )


def load_refined_outputs(outputs_dir: Path) -> dict:
    """Load all refined outputs from previous phases"""
    
    refined_outputs = {}
    
    # Load refined context from Phase II.7
    refined_file = outputs_dir / "phase_2_7_refined_context.json"
    if refined_file.exists():
        with open(refined_file, 'r') as f:
            refinement_data = json.load(f)
            # Extract refined moves directly from the top level
            refined_outputs["refined_moves"] = refinement_data.get("refined_moves", [])
            # Extract thesis and contribution from revised_paper_vision
            paper_vision = refinement_data.get("revised_paper_vision", {})
            refined_outputs["revised_thesis"] = paper_vision.get("thesis", "")
            refined_outputs["revised_contribution"] = paper_vision.get("core_contribution", "")
            # Extract outline from structure
            structure = refinement_data.get("structure", {})
            refined_outputs["outline"] = structure.get("outline", {})
    else:
        print(f"Warning: No refinement output found at {refined_file}")
        refined_outputs["refined_moves"] = []
        refined_outputs["revised_thesis"] = ""
        refined_outputs["revised_contribution"] = ""
        refined_outputs["outline"] = {}
    
    # Load literature synthesis
    lit_file = outputs_dir / "literature_synthesis.json"
    if lit_file.exists():
        with open(lit_file, 'r') as f:
            refined_outputs["literature_synthesis"] = json.load(f)
    else:
        refined_outputs["literature_synthesis"] = {}
    
    # Load move examples from curated moves
    examples_dir = outputs_dir / "curated_moves"
    move_examples = {}
    if examples_dir.exists() and examples_dir.is_dir():
        for move_file in examples_dir.glob("*.json"):
            with open(move_file, 'r') as f:
                move_data = json.load(f)
                move_type = move_file.stem.replace("move_", "")
                move_examples[move_type] = move_data
    refined_outputs["move_examples"] = move_examples
    
    return refined_outputs


def save_optimized_context(optimized_context: dict, outputs_dir: Path):
    """Save the optimized writing context"""
    
    # Save main context file
    context_file = outputs_dir / "phase_2_8_writing_context.json"
    with open(context_file, 'w') as f:
        json.dump(optimized_context, f, indent=2)
    
    # Save summary file for quick reference
    summary = {
        "timestamp": datetime.now().isoformat(),
        "thesis": optimized_context.get("paper_metadata", {}).get("thesis", ""),
        "contribution": optimized_context.get("paper_metadata", {}).get("core_contribution", ""),
        "total_refined_moves": len(optimized_context.get("refined_moves", [])),
        "total_section_blueprints": len(optimized_context.get("section_blueprints", [])),
        "writing_aids_generated": list(optimized_context.get("writing_aids", {}).keys()),
        "hooks_count": len(optimized_context.get("writing_aids", {}).get("introduction_hooks", [])),
        "phrase_bank_categories": list(optimized_context.get("writing_aids", {}).get("phrase_banks", {}).keys())
    }
    
    summary_file = outputs_dir / "phase_2_8_optimization_summary.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nWriting context saved to: {context_file}")
    print(f"Summary saved to: {summary_file}")


def main():
    """Main function to run Phase II.8 writing optimization"""
    
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Configuration
    outputs_dir = Path("outputs")
    
    # Load configuration
    config = load_config()
    
    # Load refined outputs
    logger.info("Loading refined outputs from previous phases...")
    refined_outputs = load_refined_outputs(outputs_dir)
    
    if not refined_outputs.get("refined_moves"):
        logger.error("No refined moves found. Please run Phase II.7 first.")
        return
        
    logger.info(f"Loaded {len(refined_outputs['refined_moves'])} refined moves")
    logger.info(f"Thesis: {refined_outputs.get('revised_thesis', 'Not found')[:100]}...")
    
    # Initialize worker
    worker = WritingOptimizationWorker(config)
    
    # Run optimization
    start_time = time.time()
    logger.info("Starting writing context optimization...")
    
    try:
        optimized_context = worker.run(refined_outputs)
        
        duration = time.time() - start_time
        logger.info(f"Writing optimization completed in {duration:.1f} seconds")
        
        # Log summary statistics
        logger.info(f"Generated {len(optimized_context.get('writing_aids', {}).get('introduction_hooks', []))} introduction hooks")
        logger.info(f"Created {len(optimized_context.get('section_blueprints', []))} section blueprints")
        logger.info(f"Mapped {len(optimized_context.get('content_organization', {}).get('move_to_section_mapping', {}))} moves to sections")
        
        # Save results
        save_optimized_context(optimized_context, outputs_dir)
        
        # Print sample hook
        hooks = optimized_context.get('writing_aids', {}).get('introduction_hooks', [])
        if hooks:
            print("\nSample introduction hook:")
            print(f"Type: {hooks[0].get('hook_type', 'Unknown')}")
            print(f"Text: {hooks[0].get('text', 'No text')}")
            
    except Exception as e:
        logger.error(f"Error during writing optimization: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main() 