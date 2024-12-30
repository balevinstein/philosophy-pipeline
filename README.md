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
- Phase I (Topic Generation): Complete, pending future restructuring
- Phase II.1 (Literature Processing): Complete, uses Claude's native PDF processing
- Phase II.2 (Framework Development): Complete, framework-driven paper development
- Phase II.3 (Key Moves Development): In Progress, focusing on argument development
- Detailed system design available in architecture-doc.md

## Getting Started

### Prerequisites
* Python 3.8+
* Anthropic API key (recommended)
* OpenAI API key (optional)

### Installation
1. Clone the repository
```bash
git clone https://github.com/balevinstein/philosophy-pipeline.git
cd philosophy-pipeline```
2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate```
3. Install dependencies
```bash
pip install -r requirements.txt```
4. Create .env file with API keys
```bash
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here  # Optional```

## Running the Pipeline

1. Generate and select topic
```bash
python run_phase_one.py```
After completion, check `outputs/final_selection.json` for required papers and manually add them to the `papers/` directory.
2. Process literature
```bash
python run_phase_two_one.py```
This must be done with Claude
3. Develop framework
```bash
python run_phase_two_two.py```

## Project Structure
```bash
philosophy_pipeline/
├── papers/                          # PDF storage for literature
├── src/
│   ├── prompts/                     # Phase I prompts
│   ├── stages/                      
│   │   ├── conceptual_generate.py   # Current Phase I implementation
│   │   ├── conceptual_evaluate.py
│   │   ├── conceptual_topic_development.py
│   │   ├── conceptual_final_select.py
│   │   └── phase_two/              # Phase II implementation
│   │       ├── base/               # Core worker system
│   │       │   ├── worker.py
│   │       │   └── registry.py
│   │       └── stages/             # Stage implementations
│   │           ├── stage_one/      # Literature processing
│   │           ├── stage_two/      # Framework development
│   │           ├── stage_three/    # Key moves development
│   │           └── stage_four/     # Detailed outline
│   └── utils/                      # Utility functions
├── config/
│   └── conceptual_config.yaml    
├── outputs/                        # Stage outputs
├── tests/                         # Test scripts
└── run_phase_*.py                 # Pipeline execution scripts
```

## Development Status 

Current focus is on Phase II.3: Key Moves Development, which involves:

- Full development of key argumentative moves	
- Integration of examples and literature
- Local and global coherence maintenance
- Quality control through worker/critic cycles

The system uses an actor/critic/refinement pattern with both local and global oversight to maintain paper quality while managing development complexity.

## Development Approach

The system:

- Uses Claude (and optionally GPT models) for development. Note that GPT outputs are buggier.
- Manages cognitive load through clear task boundaries
- Maintains framework alignment through systematic validation
- Preserves development history for inspection
- Creates clean outputs for each stage

## Documentation

- architecture-doc.md: Detailed system design and stage descriptions
- Sample outputs available in outputs/ directory
- Test files showing development patterns
- Configuration settings in conceptual_config.yaml

## Contributing

Interested in contributing? Please:

- Review architecture-doc.md for system design
- Check current development focus (Phase II.3)
- Feel free to open issues or pull requests

## License
Currently under private development. Licensing terms to be determined when repository is made public.

## Acknowledgments 
Special thanks to Claude. 