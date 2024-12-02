
# AI-Driven Philosophy Paper Generator

A project to generate and develop philosophy papers using AI assistance, targeting the journal *Analysis*.

## Overview

This pipeline employs a modular approach using a series of AI-assisted stages to:
1. Generate potential philosophy paper topics
2. Evaluate and select promising candidates
3. Develop detailed outlines and arguments
4. Create structured paper drafts

The project recently introduced an **Outline Development** phase to bridge topic evaluation and full paper development by generating structured outlines with detailed sections.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/philosophy_pipeline.git
   cd philosophy_pipeline
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source venv/bin/activate
     ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Create a `.env` file with your API keys:
   ```plaintext
   OPENAI_API_KEY=your_key_here
   ANTHROPIC_API_KEY=your_key_here
   ```

## Project Structure

```
philosophy_pipeline/
├── config/               # Configuration files
│   └── config.yaml      # Pipeline configuration
├── src/                 # Source code
│   ├── prompts/         # Prompt management
│   │   ├── generate.py       # Topic generation prompts
│   │   ├── evaluate.py       # Topic evaluation prompts
│   │   ├── development.py    # Paper development prompts
│   │   └── outline_development.py # Outline development prompts
│   ├── stages/          # Pipeline stages
│   │   ├── base.py          # Base stage class
│   │   ├── generate.py      # Topic generation stage
│   │   ├── evaluate.py      # Topic evaluation stage
│   │   ├── development.py   # Paper development stage
│   │   └── outline_development.py # Outline development stage
│   └── utils/           # Utility functions
│       ├── api.py           # API handling
│       └── json_utils.py    # JSON processing
├── outputs/             # Generated outputs
│   ├── generated_topics.json      # Initial topics
│   ├── topics_culled.json        # Evaluated topics
│   ├── topic_analysis.json       # Detailed analysis
│   ├── topic_abstracts.json      # Generated abstracts
│   ├── detailed_outlines.json    # Paper outlines
│   ├── argument_development.json # Section content
│   └── ...                        # Additional pipeline outputs
└── tests/              # Test files (currently empty)

```

## Usage

The pipeline is designed to be executed in sequential stages. Each stage outputs JSON files to the `outputs/` directory for inspection and further processing.

```bash
# Generate initial topics
python -m src.stages.generate

# Evaluate and cull topics
python -m src.stages.evaluate

# Develop detailed outlines for selected topics
python -m src.stages.outline_development

# Develop full sections for outlines
python -m src.stages.development
```

## Pipeline Stages

### 1. **Topic Generation**
   - Produces philosophical paper ideas with structured descriptions tailored to *Analysis* journal requirements.

### 2. **Topic Evaluation**
   - Assesses viability and categorizes topics:
     - Develop
     - Possible
     - Reject

### 3. **Outline Development** *(New!)*
   - Develops detailed outlines for selected topics, focusing on:
     - Section structure
     - Key arguments
     - Supporting details

### 4. **Paper Development**
   - Expands outlines into fully written sections, enabling draft assembly.

## Development Status

Currently implemented:
- ✓ Topic generation
- ✓ Topic evaluation
- ✓ Outline development
- ✓ Section content generation

Planned improvements:
- Multi-paper parallel development
- Final topic selection
- Complete paper assembly and refinement

## Dependencies

- OpenAI GPT-4
- Anthropic Claude
- Python packages listed in `requirements.txt`

## Contributing

[Contribution guidelines will go here]

## License

[License information will go here]

---

