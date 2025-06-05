from pathlib import Path
import time

from run_utils import (
    caffeinate,
    load_framework,
    load_key_moves,
    load_literature,
    load_outline,
    setup_logging,
)
from src.phases.phase_two.stages.stage_three.workflows.master_workflow import (
    process_all_key_moves,
)
from src.utils.api import load_config


def main():
    """Main execution for Phase II.3: Key Moves Development"""
    print("Starting Phase II.3: Key Moves Development")
    print("=" * 60)
    
    # Start timing
    phase_start_time = time.time()
    
    setup_logging()

    # Prevent sleep during execution
    caffeinate()

    # Load configuration and inputs
    config = load_config()

    # Setup output directory
    key_moves_dev_dir = Path("./outputs/key_moves_development")
    key_moves_dev_dir.mkdir(exist_ok=True)

    # Load required data
    framework = load_framework()
    outline = load_outline()
    key_moves = load_key_moves()
    literature = load_literature()

    print(f"Processing {len(framework.get('key_moves', []))} key moves...")

    # Process all key moves
    developed_moves = process_all_key_moves(
        config=config,
        output_dir=key_moves_dev_dir,
        framework=framework,
        outline=outline,
        key_moves=key_moves,
        literature=literature,
    )

    # Calculate total time
    phase_end_time = time.time()
    total_duration = phase_end_time - phase_start_time

    print("=" * 60)
    print("PHASE II.3 COMPLETION SUMMARY")
    print("=" * 60)
    print(f"⏱️  Total Phase II.3 duration: {total_duration:.1f} seconds ({total_duration/60:.1f} minutes)")
    print(f"✅ Completed development of {len(developed_moves)} key moves")
    print(f"📊 Output saved to {key_moves_dev_dir}/all_developed_moves.json")
    print(f"📝 Human-readable version saved to {key_moves_dev_dir}/all_developed_moves.md")

    return


if __name__ == "__main__":
    main()
