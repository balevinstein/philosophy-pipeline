#!/usr/bin/env python3
from datetime import datetime
import os
import sys
import json
import yaml

from src.phases.phase_two.stages.stage_four.master_workflow import (
    DetailedOutlineDevelopmentWorkflow,
)

# Add the project root to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def load_config():
    """Load configuration from config/conceptual_config.yaml."""
    config_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "config", "conceptual_config.yaml"
    )
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config


def main():
    """Run the detailed outline development phase with the new four-phase approach."""
    print("\n===== Running Detailed Outline Development (Stage II.4) =====\n")

    # Load config
    config = load_config()

    # Prepare output directories
    output_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "outputs", "detailed_outline"
    )
    os.makedirs(output_dir, exist_ok=True)

    # Initialize the workflow with the new phases
    workflow = DetailedOutlineDevelopmentWorkflow(config)

    # Set the new development phases
    workflow.development_phases = [
        "framework_integration",
        "literature_mapping",
        "content_development",
        "structural_validation",
    ]

    print(f"Using development phases: {workflow.development_phases}")

    # Define paths to input files - using actual file locations
    framework_file = os.path.join(
        os.path.dirname(output_dir), "framework_development", "abstract_framework.json"
    )
    outline_file = os.path.join(
        os.path.dirname(output_dir), "framework_development", "outline.json"
    )
    key_moves_file = os.path.join(
        os.path.dirname(output_dir),
        "key_moves_development",
        "key_moves_development",
        "all_developed_moves.json",
    )
    literature_file = os.path.join(
        os.path.dirname(output_dir), "literature_synthesis.json"
    )

    # Add debug output
    print(f"\nChecking file paths: {framework_file}")
    print(
        f"framework_file: {framework_file} (exists: {os.path.exists(framework_file)})"
    )
    print(f"outline_file: {outline_file} (exists: {os.path.exists(outline_file)})")
    print(
        f"key_moves_file: {key_moves_file} (exists: {os.path.exists(key_moves_file)})"
    )
    print(
        f"literature_file: {literature_file} (exists: {os.path.exists(literature_file)})"
    )
    print(f"Output directory: {output_dir} (exists: {os.path.exists(output_dir)})")

    # Check if all required input files exist
    missing_files = []
    for file_path, file_desc in [
        (framework_file, "Abstract Framework"),
        (outline_file, "Outline"),
        (key_moves_file, "Developed Key Moves"),
        (literature_file, "Literature Analysis"),
    ]:
        if not os.path.exists(file_path):
            missing_files.append(f"{file_desc} ({file_path})")

    if missing_files:
        print(
            f"ERROR: The following required input files are missing: {', '.join(missing_files)}"
        )
        print("Please run the previous stages first or create sample files.")
        sys.exit(1)

    # Load the required input files
    try:
        print("\nLoading files:")

        # Load framework
        if os.path.exists(framework_file):
            print(f"Loading framework from {framework_file}")
            with open(framework_file, "r") as f:
                framework_data = json.load(f)
                # Extract the inner abstract_framework object for direct access to fields
                if "abstract_framework" in framework_data:
                    framework = framework_data["abstract_framework"]
                    print(
                        f"Successfully extracted inner abstract_framework with {len(framework)} keys"
                    )
                    print(f"Keys: {list(framework.keys())}")
                    print(f"Thesis preview: {framework.get('main_thesis', '')[:50]}...")
                else:
                    framework = framework_data
                    print(
                        "Warning: Could not find abstract_framework key in framework file"
                    )
        else:
            raise FileNotFoundError(f"Framework file not found: {framework_file}")

        # Load outline
        if os.path.exists(outline_file):
            print(f"Loading outline from {outline_file}")
            with open(outline_file, "r") as f:
                outline = json.load(f)
                print(f"Loaded outline from {outline_file}")
        else:
            raise FileNotFoundError(f"Outline file not found: {outline_file}")

        # Load key moves
        if os.path.exists(key_moves_file):
            print(f"Loading developed key moves from {key_moves_file}")
            with open(key_moves_file, "r") as f:
                developed_key_moves = json.load(f)
                print(f"Loaded developed key moves from {key_moves_file}")
        else:
            raise FileNotFoundError(
                f"Developed key moves file not found: {key_moves_file}"
            )

        # Load literature
        if os.path.exists(literature_file):
            print(f"Loading literature analysis from {literature_file}")
            with open(literature_file, "r") as f:
                literature = json.load(f)
                print(f"Loaded literature analysis from {literature_file}")
        else:
            raise FileNotFoundError(
                f"Literature analysis file not found: {literature_file}"
            )

    except Exception as e:
        print(f"Error loading input files: {e}")
        sys.exit(1)

    # Run the workflow with the new phases
    print("\nStarting detailed outline development with four-phase approach...")
    detailed_outline = workflow.execute(
        {
            "framework": framework,
            "outline": outline,
            "developed_key_moves": developed_key_moves,
            "literature": literature,
        }
    )

    # Save the final detailed outline
    final_output_file = os.path.join(output_dir, "detailed_outline_final.md")
    with open(final_output_file, "w") as f:
        f.write(detailed_outline)
    print(f"\nFinal detailed outline saved to {final_output_file}")

    # Save a JSON version of the final detailed outline
    final_json_file = os.path.join(output_dir, "detailed_outline_final.json")
    json_output = {
        "detailed_outline": detailed_outline,
        "thesis_statement": framework.get("main_thesis", ""),
        "core_contribution": framework.get("core_contribution", ""),
        "key_moves": framework.get("key_moves", []),
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "phases": workflow.development_phases,
        },
    }
    with open(final_json_file, "w") as f:
        json.dump(json_output, f, indent=2)
    print(f"JSON version saved to {final_json_file}")

    # Save each phase's output for reference
    for phase in workflow.development_phases:
        phase_output = workflow.get_phase_output(phase)
        if phase_output:
            phase_output_file = os.path.join(output_dir, f"{phase}_output.md")
            with open(phase_output_file, "w") as f:
                f.write(phase_output)
            print(f"Phase '{phase}' output saved to {phase_output_file}")

    # Save metadata about the run
    metadata = {
        "timestamp": datetime.now().isoformat(),
        "phases": workflow.development_phases,
        "iterations_per_phase": workflow.get_phase_iterations(),
        "final_output_path": final_output_file,
    }

    metadata_file = os.path.join(output_dir, "metadata.json")
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"Run metadata saved to {metadata_file}")

    print("\n===== Detailed Outline Development Complete =====\n")


if __name__ == "__main__":
    main()
