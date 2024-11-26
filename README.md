# AI-Driven Philosophy Paper Generator

A project to generate and develop philosophy papers using AI assistance, targeting the journal Analysis.

## Overview

This pipeline uses a series of AI models to:
1. Generate potential philosophy paper topics
2. Evaluate and select promising candidates
3. Develop detailed outlines and arguments
4. Create structured paper drafts

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_key_here
   ANTHROPIC_API_KEY=your_key_here
   ```

## Project Structure

```
philosophy_pipeline/
├── config/               # Configuration files
│   └── config.yaml      # Pipeline configuration
├── src/                 # Source code
│   ├── prompts/        # Prompt management
│   │   ├── generate.py    # Topic generation prompts
│   │   ├── evaluate.py    # Topic evaluation prompts
│   │   └── development.py # Paper development prompts
│   ├── stages/         # Pipeline stages
│   │   ├── base.py       # Base stage class
│   │   ├── generate.py   # Topic generation
│   │   ├── evaluate.py   # Topic evaluation
│   │   └── development.py # Paper development
│   └── utils/          # Utility functions
│       ├── api.py        # API handling
│       └── json_utils.py # JSON processing
├── outputs/            # Generated outputs
│   ├── generated_topics.json   # Initial topics
│   ├── topics_culled.json     # Evaluated topics
│   ├── topic_analysis.json    # Detailed analysis
│   ├── topic_abstracts.json   # Generated abstracts
│   ├── detailed_outlines.json # Paper outlines
│   └── argument_development.json # Section content
└── tests/             # Test files

```

## Usage

The pipeline runs in sequential stages:

```bash
# Generate initial topics
python -m src.stages.generate

# Evaluate and cull topics
python -m src.stages.evaluate

# Develop selected topics
python -m src.stages.development
```

Each stage saves its output to JSON files in the outputs directory for inspection and further processing.

## Pipeline Stages

1. **Topic Generation**
   - Generates philosophical paper ideas
   - Considers Analysis journal requirements
   - Provides structured topic descriptions

2. **Topic Evaluation**
   - Assesses topic viability
   - Considers AI development potential
   - Categorizes topics (develop/possible/reject)

3. **Paper Development**
   - Analyzes selected topics in detail
   - Generates structured abstracts
   - Creates detailed outlines
   - Develops section content

## Development Status

Currently implemented:
- ✓ Topic generation
- ✓ Topic evaluation
- ✓ Initial development (analysis, abstracts, outlines)
- ✓ Section content generation

In progress:
- Multi-paper parallel development
- Final topic selection stage
- Complete paper assembly

## Dependencies

- OpenAI GPT-4
- Anthropic Claude
- Python packages listed in requirements.txt

## Contributing

[Contribution guidelines will go here]

## License

[License information will go here]