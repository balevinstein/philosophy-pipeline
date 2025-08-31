# Installation Guide

This guide will walk you through installing and setting up the Philosophy Pipeline from scratch.

## System Requirements

### Operating System
- **Linux/macOS**: Fully supported
- **Windows**: Supported via WSL2 or native Python

### Software Dependencies
- **Python 3.8+** (Python 3.9+ recommended)
- **Node.js 14+** (only needed for Phase I.2 literature search)
- **Git** for cloning the repository

### API Requirements
You'll need API keys from the following providers:

- **Anthropic API** (Required) - Primary model provider
- **OpenAI API** (Optional) - Used for specific reasoning tasks
- **Tavily Search API** (Required for Phase I.2) - Literature search

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone https://github.com/balevinstein/philosophy-pipeline.git
cd philosophy-pipeline
```

### 2. Set Up Python Environment

Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs all required packages including:
- `anthropic` - Anthropic API client
- `openai` - OpenAI API client  
- `pyyaml` - Configuration file parsing
- `requests` - HTTP requests
- `python-dotenv` - Environment variable management

### 4. Install Node.js Dependencies (Optional)

Only needed if you plan to run Phase I.2 (literature search):

```bash
cd rivet
npm install
cd ..
```

### 5. Configure API Keys

Create a `.env` file in the project root:

```bash
# Copy the template
cp .env.example .env
```

Edit `.env` with your API keys:

```bash
# Required for all phases
ANTHROPIC_API_KEY=your_anthropic_key_here

# Optional - used for complex reasoning tasks
OPENAI_API_KEY=your_openai_key_here

# Required for Phase I.2 literature search
TAVILY_API_KEY=your_tavily_key_here
```

### 6. Verify Installation

Test that everything is working:

```bash
# Check Python dependencies
python -c "import anthropic, openai, yaml; print('Python dependencies OK')"

# Test CLI interface
python pipeline_cli.py --help

# Validate environment
python pipeline_cli.py validate
```

## API Key Setup

### Getting Anthropic API Key

1. Visit [Anthropic Console](https://console.anthropic.com)
2. Sign up or sign in to your account
3. Navigate to API Keys section
4. Generate a new API key
5. Add credits to your account (recommended: $20+ for full pipeline runs)

### Getting OpenAI API Key (Optional)

1. Visit [OpenAI Platform](https://platform.openai.com)
2. Sign up or sign in
3. Go to API Keys section
4. Create new secret key
5. Add billing information and credits

### Getting Tavily Search API Key

1. Visit [Tavily](https://tavily.com)
2. Sign up for an account
3. Access your dashboard
4. Copy your API key from the dashboard

## Directory Structure

After installation, your directory should look like:

```
philosophy-pipeline/
├── .env                    # Your API keys (create this)
├── pipeline_cli.py         # Main CLI interface
├── requirements.txt        # Python dependencies
├── config/                # Configuration files
├── src/                   # Source code
├── docs/                  # Documentation
├── papers/               # Literature PDFs (you'll add these)
├── outputs/              # Generated outputs
├── rivet/                # Rivet components (optional)
└── venv/                 # Virtual environment
```

## Next Steps

1. **[Quick Start Guide](quickstart.md)** - Generate your first paper
2. **[CLI Reference](cli-reference.md)** - Learn all available commands  
3. **[Configuration](configuration.md)** - Customize pipeline behavior

## Troubleshooting Installation

### Virtual Environment Issues

```bash
# If activation fails, try:
python3 -m venv venv
source venv/bin/activate

# On Windows with PowerShell:
venv\Scripts\Activate.ps1

# Check Python version in environment
python --version  # Should be 3.8+
```

### API Key Issues

```bash
# Test API keys directly
python -c "
import os
from anthropic import Anthropic
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
print('Anthropic API key working')
"
```

### Permission Issues

On Linux/macOS, you may need to set executable permissions:

```bash
chmod +x pipeline_cli.py
```

### Node.js Issues (Phase I.2 only)

```bash
# Check Node.js version
node --version  # Should be 14+

# If npm install fails in rivet/:
rm -rf node_modules
npm cache clean --force
npm install
```

## System-Specific Notes

### macOS Users
- Use Homebrew to install Python: `brew install python@3.9`
- Use Homebrew to install Node.js: `brew install node`

### Windows Users  
- Consider using Windows Subsystem for Linux (WSL2)
- If using native Windows, ensure Python and Node.js are in PATH
- Use PowerShell for commands (not Command Prompt)

### Linux Users
- Install Python development headers: `sudo apt-get install python3-dev`
- Some systems may need: `sudo apt-get install build-essential`

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting Guide](troubleshooting.md)
2. Verify all prerequisites are installed correctly
3. Ensure API keys are valid and have sufficient credits
4. Check GitHub Issues for known problems

Ready to generate your first philosophy paper? Continue to the **[Quick Start Guide](quickstart.md)**!