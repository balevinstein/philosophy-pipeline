# AI-Driven Philosophy Paper Generator

A project to generate and develop philosophy papers using AI.

## Overview
This pipeline uses a series of AI models to:
1. Generate potential philosophy paper topics
2. Evaluate and select promising candidates
3. Develop detailed outlines and arguments
4. Create structured paper drafts

## Project Structure
```
philosophy_pipeline/
├── papers/              # PDF storage for literature
├── src/
│   ├── prompts/        # Phase I prompt management
│   ├── stages/         # Pipeline stages
│   │   ├── phase_one/  # Phase I implementation
│   │   └── phase_two/  # Phase II implementation
│   │       ├── base/   # Worker system
│   │       └── stages/ # Stage implementations
│   └── utils/          # Utility functions
└── outputs/            # Stage outputs
```

## Usage
Run the complete Phase I pipeline:
```bash
python run_phase_one.py
```

After Phase I completes:
1. Check outputs/final_selection.json for paper requirements
2. Place requested PDFs in papers/ directory
3. Run Phase II.1 literature processing:
```bash
python run_phase_two_one.py
```

This will generate:
- literature_readings.json (detailed paper analysis)
- literature_synthesis.json (structured overview)
- literature_synthesis.md (narrative synthesis)

Further Phase II stages coming soon.

## Development Status
Currently implemented:

* ✓ Phase I: Topic Generation and Selection
    * Topic generation
    * Initial evaluation
    * Development testing
    * Final selection

* ✓ Phase II.1: Literature Processing
    * PDF processing
    * Literature analysis
    * Cross-paper synthesis
    * Engagement planning

### In progress:

* Phase II.2: Framework Development
* Remaining Phase II stages
* Phase III: Paper Drafting

## Dependencies
* Python 3.8+
* Required packages in requirements.txt
* API keys for Language Models (Anthropic Claude)

## Setup
* Clone repository
* Create virtual environment
* Install dependencies: `pip install -r requirements.txt`
* Create .env file with API keys:
  ```
  ANTHROPIC_API_KEY=your_key_here
  OPENAI_API_KEY=your_key_here
  ```

## Project History
Earlier versions of this project are preserved in the `legacy/` directory for reference. Current implementation focuses on conceptual philosophical topics and uses a revised pipeline structure with worker-based architecture and systematic development approach.