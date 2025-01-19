# run_phase_two_two.py

import sys
import os
import yaml
from pathlib import Path
import json
import logging
from typing import Dict, Any
import subprocess

from src.phases.phase_two.stages.stage_two.workers.abstract_worker import (
    AbstractDevelopmentWorker,
)
from src.phases.phase_two.stages.stage_two.workers.abstract_critic import AbstractCritic
from src.phases.phase_two.stages.stage_two.workers.abstract_refinement_worker import (
    AbstractRefinementWorker,
)
from src.phases.phase_two.stages.stage_two.workers.outline_worker import OutlineWorker
from src.phases.phase_two.stages.stage_two.workers.outline_critic import OutlineCritic
from src.phases.phase_two.stages.stage_two.workers.outline_refinement_worker import (
    OutlineRefinementWorker,
)
from src.phases.phase_two.stages.stage_two.workers.key_moves_worker import (
    KeyMovesWorker,
)
from src.phases.phase_two.stages.stage_two.workers.key_moves_critic import (
    KeyMovesCritic,
)
from src.phases.phase_two.stages.stage_two.workers.key_moves_refinement_worker import (
    KeyMovesRefinementWorker,
)


def setup_logging():
    """Configure logging"""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def load_final_selection() -> Dict[str, Any]:
    """Load final selection from Phase I"""
    try:
        with open("./outputs/final_selection.json") as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValueError("Could not find final_selection.json. Run Phase I first.")


def load_literature() -> Dict[str, Any]:
    """Load literature analysis from Phase II.1"""
    try:
        lit_readings = json.load(open("./outputs/literature_readings.json"))
        lit_synthesis = json.load(open("./outputs/literature_synthesis.json"))
        with open("./outputs/literature_synthesis.md") as f:
            lit_narrative = f.read()
        return {
            "readings": lit_readings,
            "synthesis": lit_synthesis,
            "narrative": lit_narrative,
        }
    except FileNotFoundError as e:
        raise ValueError(f"Missing literature files. Run Phase II.1 first. Error: {e}")


def caffeinate():
    """Prevent system sleep during execution"""
    try:
        import subprocess

        subprocess.Popen(["caffeinate", "-i", "-w", str(os.getpid())])
    except Exception as e:
        print(f"Warning: Could not caffeinate process: {e}")
        print(
            "You may want to manually prevent your system from sleeping during execution."
        )


def main():
    print("Starting Phase II.2: Framework Development")
    setup_logging()

    try:
        # Prevent sleep during execution
        subprocess.Popen(["caffeinate", "-i", "-w", str(os.getpid())])
        # Load inputs
        final_selection = load_final_selection()
        literature = load_literature()

        # Load config
        config_path = "config/conceptual_config.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)

        # Create output directories
        framework_dir = Path("./outputs/framework_development")
        framework_dir.mkdir(exist_ok=True)

        # Initialize workers
        abstract_worker = AbstractDevelopmentWorker(config)
        abstract_critic = AbstractCritic(config)
        abstract_refinement = AbstractRefinementWorker(config)

        outline_worker = OutlineWorker(config)
        outline_critic = OutlineCritic(config)
        outline_refinement = OutlineRefinementWorker(config)

        key_moves_worker = KeyMovesWorker(config)
        key_moves_critic = KeyMovesCritic(config)
        key_moves_refinement = KeyMovesRefinementWorker(config)

        # Abstract Development Cycle
        print("\nStarting Abstract Development...")
        abstract_dir = framework_dir / "abstract"
        abstract_dir.mkdir(exist_ok=True)

        state = {"final_selection": final_selection, "literature": literature}

        abstract = abstract_worker.run(state)

        versions = [abstract.modifications]
        critiques = []
        refinements = []

        num_cycles = config["parameters"]["development_cycles"]["abstract_num_cycles"]

        for cycle in range(num_cycles):
            print(f"\nStarting abstract cycle {cycle + 1}/{num_cycles}")

            # Create cycle directory
            cycle_dir = abstract_dir / f"cycle_{cycle}"
            cycle_dir.mkdir(exist_ok=True)

            # Get critique
            critique = abstract_critic.run(
                {"abstract_framework": versions[-1], "literature": literature}
            )
            critiques.append(critique)

            # Save critique
            json.dump(
                {"critique": critique.modifications},
                open(cycle_dir / "critique.json", "w"),
                indent=2,
            )

            # Refine abstract
            refined = abstract_refinement.run(
                {
                    "current_framework": versions[-1],
                    "current_critique": critique.modifications,
                    "literature": literature,
                }
            )
            refinements.append(refined)
            versions.append(refined.modifications["framework_data"])

            # Save refinement
            json.dump(
                {"refinement": refined.modifications},
                open(cycle_dir / "refinement.json", "w"),
                indent=2,
            )

        # Save final abstract version for next stages
        framework = versions[-1]
        json.dump(
            {"framework": framework},
            open(framework_dir / "framework.json", "w"),
            indent=2,
        )

        # Similar cycles for outline and key moves...
        # Outline Development Cycle
        print("\nStarting Outline Development...")
        outline_dir = framework_dir / "outline"
        outline_dir.mkdir(exist_ok=True)

        state = {"framework": framework, "literature": literature}

        outline = outline_worker.run(state)

        outline_versions = [outline.modifications["outline"]]
        outline_critiques = []
        outline_refinements = []

        num_cycles = config["parameters"]["development_cycles"]["outline_num_cycles"]

        for cycle in range(num_cycles):
            print(f"\nStarting outline cycle {cycle + 1}/{num_cycles}")

            # Create cycle directory
            cycle_dir = outline_dir / f"cycle_{cycle}"
            cycle_dir.mkdir(exist_ok=True)

            # Get critique
            critique_state = {
                "outline": outline_versions[-1],
                "framework": framework,
                "literature": literature,
            }

            critique = outline_critic.run(critique_state)
            outline_critiques.append(critique)

            # Save critique
            json.dump(
                {"critique": critique.modifications},
                open(cycle_dir / "critique.json", "w"),
                indent=2,
            )

            # Refine outline
            refinement_state = {
                "outline": outline_versions[-1],
                "critique": critique.modifications,
                "framework": framework,
                "literature": literature,
            }

            refined = outline_refinement.run(refinement_state)
            outline_refinements.append(refined)
            outline_versions.append(refined.modifications["outline"])

            # Save refinement
            json.dump(
                {"refinement": refined.modifications},
                open(cycle_dir / "refinement.json", "w"),
                indent=2,
            )

        # Save final outline version
        final_outline = outline_versions[-1]
        json.dump(
            {"outline": final_outline},
            open(framework_dir / "outline.json", "w"),
            indent=2,
        )

        # Key Moves Development Cycle
        print("\nStarting Key Moves Development...")
        key_moves_dir = framework_dir / "key_moves"
        key_moves_dir.mkdir(exist_ok=True)

        state = {
            "framework": framework,
            "outline": final_outline,
            "literature": literature,
        }

        moves = key_moves_worker.run(state)

        moves_versions = [moves.modifications["content"]]
        moves_critiques = []
        moves_refinements = []

        num_cycles = config["parameters"]["development_cycles"]["key_moves_num_cycles"]

        for cycle in range(num_cycles):
            print(f"\nStarting key moves cycle {cycle + 1}/{num_cycles}")

            # Create cycle directory
            cycle_dir = key_moves_dir / f"cycle_{cycle}"
            cycle_dir.mkdir(exist_ok=True)

            # Get critique
            critique_state = {
                "key_moves_analysis": moves_versions[-1],
                "framework": framework,
                "outline": final_outline,
                "literature": literature,
            }

            critique = key_moves_critic.run(critique_state)
            moves_critiques.append(critique)

            # Save critique
            json.dump(
                {"critique": critique.modifications},
                open(cycle_dir / "critique.json", "w"),
                indent=2,
            )
            with open(cycle_dir / "critique.md", "w") as f:
                f.write(critique.modifications["content"])

            # Refine moves
            refinement_state = {
                "key_moves_analysis": moves_versions[-1],
                "critique": critique.modifications,
                "framework": framework,
                "outline": final_outline,
                "literature": literature,
            }

            refined = key_moves_refinement.run(refinement_state)
            moves_refinements.append(refined)
            moves_versions.append(refined.modifications["moves"])

            # Save refinement
            json.dump(
                {"refinement": refined.modifications},
                open(cycle_dir / "refinement.json", "w"),
                indent=2,
            )
            with open(cycle_dir / "refinement.md", "w") as f:
                f.write(refined.modifications["content"])

        # Save final versions for Phase II.3
        json.dump(
            {
                "framework": framework,
                "outline": final_outline,
                "key_moves": moves_versions[-1],
            },
            open(framework_dir / "phase_two_two_output.json", "w"),
            indent=2,
        )

        # Save complete development history
        json.dump(
            {
                "abstract": {
                    "versions": versions,
                    "critiques": [c.modifications for c in critiques],
                    "refinements": [r.modifications for r in refinements],
                },
                "outline": {
                    "versions": outline_versions,
                    "critiques": [c.modifications for c in outline_critiques],
                    "refinements": [r.modifications for r in outline_refinements],
                },
                "key_moves": {
                    "versions": moves_versions,
                    "critiques": [c.modifications for c in moves_critiques],
                    "refinements": [r.modifications for r in moves_refinements],
                },
            },
            open(framework_dir / "development_history.json", "w"),
            indent=2,
        )

        print("\nPhase II.2 completed successfully!")

        # Create readable summary
        summary_md = f"""# Phase II.2 Development Summary

        ## Framework
        {json.dumps(framework, indent=2)}

        ## Final Outline
        {final_outline}

        ## Key Moves
        {moves_versions[-1]}

        This development is ready for Phase II.3 detailed structure development."""

        # Save summary
        with open(framework_dir / "phase_two_two_summary.md", "w") as f:
            f.write(summary_md)

    except Exception as e:
        print(f"\nError during Phase II.2: {str(e)}")
        raise


if __name__ == "__main__":
    main()
