import os
import time
from pathlib import Path
import subprocess


from run_utils import (
    load_final_selection,
    load_framework,
    load_literature,
    load_outline,
    setup_logging,
)
from src.phases.phase_two.stages.stage_two.workflows.abstract_workflow import (
    create_abstract_framework_workflow,
)
from src.phases.phase_two.stages.stage_two.workflows.key_moves_workflow import (
    create_key_moves_workflow,
)
from src.phases.phase_two.stages.stage_two.workflows.outline_workflow import (
    create_outline_workflow,
)
from src.utils.api import load_config


def main():
    """Main execution for Phase 2"""
    phase_start_time = time.time()
    print("Starting Phase II.2: Framework Development")
    print("=" * 60)
    setup_logging()

    # Prevent sleep during execution
    subprocess.Popen(["caffeinate", "-i", "-w", str(os.getpid())])

    # Load configuration and inputs
    config = load_config()

    # Setup output directory
    framework_dev_dir = Path("./outputs/framework_development")
    framework_dev_dir.mkdir(exist_ok=True)

    final_selection = load_final_selection()
    literature = load_literature()

    abstract_initial_state = {
        "final_selection": final_selection,
        "literature": literature,
    }

    # Workflow 1: Abstract Framework Development
    print("\n1. Abstract Framework Development")
    print("-" * 40)
    abstract_start_time = time.time()
    
    abstract_framework_workflow = create_abstract_framework_workflow(
        config,
        output_dir=framework_dev_dir,
        workflow_name="abstract_framework",
        max_cycles=3,
    )

    abstract_framework_workflow.execute(abstract_initial_state)
    
    abstract_duration = time.time() - abstract_start_time
    print(f"⏱️  Abstract Framework completed in {abstract_duration:.1f} seconds")

    framework = load_framework()

    # Workflow 2: Outline Development
    print("\n2. Outline Development")
    print("-" * 40)
    outline_start_time = time.time()
    
    outline_initial_state = {"framework": framework, "literature": literature}
    outline_workflow = create_outline_workflow(
        config, output_dir=framework_dev_dir, workflow_name="outline", max_cycles=3
    )

    outline = outline_workflow.execute(outline_initial_state)
    
    outline_duration = time.time() - outline_start_time
    print(f"⏱️  Outline Development completed in {outline_duration:.1f} seconds")

    outline = load_outline()

    # Workflow 3: Key Moves Identification
    print("\n3. Key Moves Identification")
    print("-" * 40)
    key_moves_start_time = time.time()
    
    key_moves_initial_state = {
        "outline": outline,
        "framework": framework,
        "literature": literature,
    }

    key_moves_workflow = create_key_moves_workflow(
        config, output_dir=framework_dev_dir, workflow_name="key_moves", max_cycles=3
    )

    key_moves_workflow.execute(key_moves_initial_state)
    
    key_moves_duration = time.time() - key_moves_start_time
    print(f"⏱️  Key Moves Identification completed in {key_moves_duration:.1f} seconds")

    # Phase summary
    total_duration = time.time() - phase_start_time
    print("\n" + "=" * 60)
    print("PHASE II.2 COMPLETION SUMMARY")
    print("=" * 60)
    print(f"⏱️  Total Phase II.2 duration: {total_duration:.1f} seconds ({total_duration/60:.1f} minutes)")
    print(f"📊 Breakdown:")
    print(f"   Abstract Framework: {abstract_duration:.1f}s")
    print(f"   Outline Development: {outline_duration:.1f}s") 
    print(f"   Key Moves: {key_moves_duration:.1f}s")
    print("✅ Phase II.2: Framework Development completed successfully")

    return


if __name__ == "__main__":
    main()
