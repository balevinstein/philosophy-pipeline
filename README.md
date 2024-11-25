# AI-Driven Philosophy Paper Generator

A project to generate and develop philosophy papers using AI assistance.

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
├── src/                 # Source code
│   ├── prompts/        # Prompt management
│   ├── stages/         # Pipeline stages
│   └── utils/          # Utility functions
├── outputs/            # Generated outputs
└── tests/             # Test files
```

## Usage

Generate and evaluate topics:
```bash
# Generate initial topics
python -m src.stages.generate

# Evaluate and cull topics
python -m src.stages.evaluate

## Development

[Development instructions will go here]