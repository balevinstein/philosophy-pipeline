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
│   ├── prompts/        # Prompt management
│   ├── stages/         # Pipeline stages
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
3. Proceed with Phase II (coming soon)

## Development Status
Currently implemented:

* ✓ Phase I: Topic Generation and Selection
    * Topic generation
    * Initial evaluation
    * Development testing
    * Final selection



### In progress:

* Phase II: Detailed Outline Development
* Phase III: Paper Drafting

## Dependencies

* Python 3.8+
* Required packages in requirements.txt
* API keys for Language Models

## Setup

* Clone repository
* Create virtual environment
* Install dependencies
* Create .env file with API keys

## Project History
Earlier versions of this project are preserved in the `legacy/` directory for reference. Current implementation focuses on conceptual philosophical topics and uses a revised pipeline structure.
