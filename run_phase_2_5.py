import json
import os
import sys
from dotenv import load_dotenv
import requests

from run_utils import (
    check_rivet_life,
    load_developed_key_moves,
    load_final_selection,
    load_framework,
    load_key_moves,
    load_literature,
    load_outline,
)


def get_merged_context(
    framework, outline, key_moves, literature, final_selection, developed_moves
):
    try:
        load_dotenv()

        request_data = {
            "framework": framework,
            "outline": outline,
            "key_moves": key_moves,
            "literature": literature,
            "final_selection": final_selection,
            "developed_moves": developed_moves,
            "openAIKey": os.getenv("OPENAI_API_KEY"),
        }

        headers = {"Content-Type": "application/json"}

        response = requests.get(
            "http://localhost:4040/mergedContext",
            data=json.dumps(request_data),
            timeout=5000,
            headers=headers,
        )

        if response.status_code == 200:
            try:
                return response.content
            except ValueError:
                print("Failed to decode JSON")

    except Exception as e:
        print(f"\nError in calling the Rivet server: {str(e)}")
        sys.exit(1)


def run_phase_one_five():
    """Run stage  Phase II.5 in sequence"""

    try:
        print("\nStarting Phase I.5 pipelinel: Coalesce...")
        print("\nPlease make sure you started the rivet node server...")

        check_rivet_life()

        framework = load_framework()
        outline = load_outline()
        literature = load_literature()
        final_selection = load_final_selection()
        developed_moves = load_developed_key_moves()
        key_moves = load_key_moves()

        context = get_merged_context(
            framework=framework,
            outline=outline,
            literature=literature,
            final_selection=final_selection,
            developed_moves=developed_moves,
            key_moves=key_moves,
        )
        context = json.loads(context)

        with open("./outputs/phase_3_context.json", "w") as f:
            f.write(json.dumps(context, indent=2))
        return context

    except Exception as e:
        print(f"\nError in Phase II.5 pipeline: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    run_phase_one_five()
