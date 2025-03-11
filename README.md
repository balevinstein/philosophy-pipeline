# AI-Driven Philosophy Paper Generator

A system that generates and develops publishable-quality analytic philosophy papers through a series of structured development stages.

## Project Overview

This project explores whether large language models can systematically develop philosophical papers suitable for academic publication. Targeting the journal Analysis (4,000-word limit), the system:

1. Generates and evaluates potential paper topics
2. Develops detailed argumentative frameworks
3. Creates structured paper outlines
4. Produces complete drafts

The goal is to achieve a ~20% success rate in generating publishable-quality papers while maintaining philosophical rigor and originality.

## Current Status

- Phase I.1 (Topic Generation): Complete, pending future restructuring
- Phase I.2 (Literature Research): Find relevant literature on the web
- Phase II.1 (Literature Processing): Complete, uses Claude's native PDF processing
- Phase II.2 (Framework Development): Complete, framework-driven paper development
- Phase II.3 (Key Moves Development): Complete, focusing on argument development
- Phase II.4 (Detailed Outline Development): In Progress, working on generating detailed outlines

- Detailed system design available in architecture-doc.md

## Getting Started

### Prerequisites

- Python 3.8+
- Node
- Anthropic API key
- OpenAI API key
- Tavily Search API key
- [Rivet](https://rivet.ironcladapp.com/)
  - Please download and install the Rivet IDE

### Installation

1. Clone the repository

```bash
git clone https://github.com/balevinstein/philosophy-pipeline.git
cd philosophy-pipeline
```

2. Create and activate the virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

To deactivate the virtual environment at any point, use the command below:

```bash
deactivate
```

3. Install dependencies

In the root directory:

```bash
pip install -r requirements.txt
```

In the `rivet` directory (`cd rivet`):

```bash
npm install
```

4. Create `.env` file with API keys in the root directory

```bash
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

5. Start Rivet server

```
cd rivet
node --watch server.js
```

## Running the Pipeline

### 1. Generate and select a topic

```bash
python run_phase_one_one.py
```

Output: `outputs/final_selection.json`

### 2. Search papers for literature engagement

```bash
python run_phase_two_one.py
```

After completion, check `literature_research_papers.md` for required papers and manually add them to the `papers/` directory.

### 3. Process literature

This must be done with Claude

```bash
python run_phase_two_one.py
```

Output:

- `literature_synthesis.json`
- `literature_synthesis.md`

### 4. Develop framework

```bash
python run_phase_two_two.py
```

Output:

- `outputs/framework_development`

### 5. Develop Key Moves

```bash
python run_phase_two_three.py
```

Output:

- `all_developed_moves.json`
- `all_developed_moves.md`

## Project Structure

All directories are a python package and contain a `__init__.py` file to facilitate imports and exports

- config/ (conceptual_config.yaml)

- legacy/ (Legacy scripts and tests that are not relevant anymore)

- outputs/ (local only) (Your outputs would be stored here in your local environment)

- papers/ (Scripts refer to this directory to look for literature engagement papers)

- rivet/ (Directory containing the Rivet node server)

  - node_modules/
  - package-lock.json
  - package.json
  - philosophy-pipeline.rivet-project
  - server.js

- sample_output_papers/ (Sample papers stored for future reference)

  - paper_1/
  - paper_2/

- tests (Scripts developed during testing or iteration)
- .env (Local credentials file)
- .gitignore
- .pylintrc
- architecture-doc.md (Project architecture overview)
- requirements.txt
- run_phase_one_one.py
- run_phase_one_two.py
- run_phase_two_one.py
- run_phase_two_two.py
- run_phase_two_three.py

- src/
  - utils/
    - api.py
    - json_utils.py
    - paper_utils.py
  - phases/
    - core/
      - base_worker.py
      - exceptions.py
      - worker_types.py
      - workflow.py
    - phase_one/
      - prompts/
        - conceptual_evaluate.py
        - conceptual_final_select.py
        - conceptual_generate.py
        - conceptual_topic_development.py
        - json_format.py
      - base.py
      - conceptual_evaluate.py
      - conceptual_final_select.py
      - conceptual_generate.py
      - conceptual_topic_development.py
    - phase_two/
      - base/
        - framework.py
        - registry.py
        - worker.py
      - stages/
        - stage_one/
          - lit_processor.py
          - pdf_processor.py
          - prompts.py
        - stage_two/
          - prompts/
            - abstract/
              - abstract_critic_prompts.py
              - abstract_development_prompts.py
              - abstract_prompts.py
              - abstract_refinement_prompts.py
            - key_moves/
              - key_moves_critic_prompts.py
              - key_moves_development_prompts.py
              - key_moves_prompts.py
              - key_moves_refinment_prompts.py
            - outline/
              - outline_critic_prompts.py
              - outline_development_prompts.py
              - outline_prompts.py
              - outline_refinement_prompts.py
          - workers/
            - critic/
              - abstract_critic.py
              - key_moves_critic.py
              - outline_critic.py
            - development/
              - abstract_development.py
              - key_moves_development.py
              - outline_development.py
            - refinement/
              - abstract_refinement.py
              - key_moves_refinement.py
              - outline_refinement.py
          - workflows/
            - abstract_workflow.py
            - key_moves_workflow.py
            - outline_workflow.py
        - stage_three/
          - prompts/
            - critic
              - critic_prompts.py
            - development
              - development_prompts.py
            - refinement
              - refinement_prompts.py
          - workers/
            - critic/
              - move_critic.py
            - development/
              - move_development.py
            - refinement/
              - move_refinement.py
          - workflows/
            - key_moves_dev_workflow.py
            - master_workflow.py

## Development Approach

The system:

- Uses Claude (and optionally GPT models) for development. Note that GPT outputs are buggier.
- Manages cognitive load through clear task boundaries
- Maintains framework alignment through systematic validation
- Preserves development history for inspection
- Creates clean outputs for each stage

## Documentation

- `architecture-doc.md`: Detailed system design and stage descriptions
- Sample outputs available in outputs/ directory
- Test files showing development patterns are in tests/
- Configuration settings in conceptual_config.yaml

## Contributing

Interested in contributing? Please:

- Review `architecture-doc.md` for system design
- Check current development focus (Phase II.3)
- Feel free to open issues or pull requests

## License

Currently under private development. Licensing terms to be determined when repository is made public.

## Acknowledgments

Special thanks to Claude, who helped with much of the development.
