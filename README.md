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

**All Phase II stages are complete and working!** 🎉

- ✅ **Phase I.1** (Topic Generation): Complete
- ✅ **Phase I.2** (Literature Research): Complete - find relevant literature on the web
- ✅ **Phase II.1** (Literature Processing): Complete - uses Claude's native PDF processing
- ✅ **Phase II.2** (Framework Development): Complete - framework-driven paper development
- ✅ **Phase II.3** (Key Moves Development): Complete - sophisticated argument development through 3 phases
- ✅ **Phase II.4** (Detailed Outline Development): Complete - comprehensive outline with literature mapping
- ✅ **Phase II.5** (Context Consolidation): Complete - unified context for Phase III
- 🚧 **Phase III** (Paper Writing): In development

### Recent Fixes & Improvements

- Fixed critical bugs in Phase II.3 enumeration and content aggregation
- Improved content quality and proper literature integration
- Enhanced error handling and type safety
- Optimized workflow cycles and iteration management

### Architecture & Code Quality

- **Work‑in‑Progress**: You may encounter uneven patterns and non‑ideal practices throughout the codebase.
- **Refactoring Planned**: We're prioritizing feature delivery now and will undertake a comprehensive refactor once our core functionality is in place.
- **Typing Migration**: We're migrating our Development, Critique, and Refinement workers to fully‑typed definitions in src/phases/core.
- **Rivet & Python Hybrid**: Some modules (e.g. Phase II.5) use Rivet to orchestrate AI graphs alongside Python implementations.
- **Future Alignment**: Ultimately, we plan to unify all phases under a consistent, typed architecture.

Detailed system design available in `architecture-doc.md`

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js (for Rivet server)
- API Keys:
  - Anthropic API key (required for all phases)
  - OpenAI API key
  - Tavily Search API key
- [Rivet](https://rivet.ironcladapp.com/) - Download and install the Rivet IDE

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/balevinstein/philosophy-pipeline.git
cd philosophy-pipeline
```

2. **Create and activate the virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

To deactivate the virtual environment at any point:

```bash
deactivate
```

3. **Install dependencies**

In the root directory:

```bash
pip install -r requirements.txt
```

In the `rivet` directory:

```bash
cd rivet
npm install
cd ..
```

4. **Create `.env` file with API keys in the root directory**

```bash
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
TAVILY_API_KEY=your_tavily_key_here
```

5. **Start Rivet server** (required for Phase II.5)

In a separate terminal:

```bash
cd rivet
node --watch server.js
```

Keep this running while using the pipeline.

## Running the Pipeline

### Quick Start: Complete Phase II Pipeline

Once you have literature papers in the `papers/` directory, you can run the complete Phase II pipeline:

```bash
# Activate virtual environment
source venv/bin/activate

# Run complete Phase II (takes ~75 minutes)
python run_phase_2_1.py  # Literature processing
python run_phase_2_2.py  # Framework development
python run_phase_2_3.py  # Key moves development
python run_phase_2_4.py  # Detailed outline
python run_phase_2_5.py  # Context consolidation
```

### Detailed Step-by-Step Instructions

#### 1. Generate and select a topic

```bash
python run_phase_1_1.py
```

**Output**: `outputs/final_selection.json`

#### 2. Search papers for literature engagement

```bash
python run_phase_1_2.py
```

After completion, check `literature_research_papers.md` for required papers and **manually download PDFs** to the `papers/` directory.

#### 3. Process literature

**Requires**: PDFs in `papers/` directory
**Uses**: Claude for PDF processing

```bash
python run_phase_2_1.py
```

**Output**:
- `outputs/literature_synthesis.json`
- `outputs/literature_synthesis.md`

#### 4. Develop framework

```bash
python run_phase_2_2.py
```

**Output**: `outputs/framework_development/` containing abstract, outline, and key moves

#### 5. Develop Key Moves

```bash
python run_phase_2_3.py
```

**Duration**: ~45 minutes for 2 key moves
**Output**: `outputs/key_moves_development/key_moves_development/all_developed_moves.json`

#### 6. Create Detailed Outline

```bash
python run_phase_2_4.py
```

**Duration**: ~15 minutes
**Output**: `outputs/detailed_outline/detailed_outline_final.json`

#### 7. Consolidate Context

**Requires**: Rivet server running (`cd rivet && node server.js`)

```bash
python run_phase_2_5.py
```

**Output**: `outputs/phase_3_context.json` (comprehensive context for Phase III)

## Output Quality

The pipeline generates **publication-quality philosophical content**:

- **Sophisticated Arguments**: Logically structured with clear premises and conclusions
- **Literature Integration**: Proper citations and scholarly engagement
- **Academic Structure**: Professional outline suitable for journal submission
- **Philosophical Rigor**: Maintains theoretical coherence across development phases

### Sample Output Structure

```
outputs/
├── final_selection.json           # Phase I topic selection
├── literature_synthesis.json      # Phase II.1 literature analysis
├── framework_development/         # Phase II.2 core framework
├── key_moves_development/         # Phase II.3 developed arguments
├── detailed_outline/              # Phase II.4 comprehensive outline
└── phase_3_context.json          # Phase II.5 consolidated context
```

## Project Structure

```
philosophy-pipeline/
├── config/
│   └── conceptual_config.yaml     # Pipeline configuration
├── outputs/                       # Generated content (local only)
├── papers/                        # PDF literature (add manually)
├── rivet/                         # Rivet server and workflows
├── src/
│   ├── phases/
│   │   ├── core/                  # Base worker types
│   │   ├── phase_one/             # Topic generation
│   │   └── phase_two/             # Framework development
│   └── utils/                     # API and utility functions
├── run_phase_*.py                 # Execution scripts
├── architecture-doc.md            # Detailed system architecture
└── requirements.txt
```

## Configuration

Edit `config/conceptual_config.yaml` to adjust:

- **Iteration limits**: Max cycles per development phase
- **Model settings**: Provider, model, temperature per worker type
- **Content parameters**: Word counts, section allocations
- **Quality thresholds**: Assessment criteria and validation levels

## Performance Characteristics

- **Phase II.1**: ~5 minutes (literature processing)
- **Phase II.2**: ~10 minutes (framework development)
- **Phase II.3**: ~45 minutes (key moves development, 2 moves)
- **Phase II.4**: ~15 minutes (detailed outline)
- **Phase II.5**: ~2 minutes (context consolidation)
- **Total Phase II**: ~75 minutes for complete pipeline

## Troubleshooting

### Common Issues

1. **Rivet server not running**: Phase II.5 requires `node server.js` in rivet directory
2. **Missing PDFs**: Download papers to `papers/` directory before Phase II.1
3. **API rate limits**: The pipeline respects rate limits but may take longer during high usage
4. **Virtual environment**: Always activate with `source venv/bin/activate`

### Getting Help

- Check `architecture-doc.md` for detailed system design
- Review configuration in `config/conceptual_config.yaml`
- Examine outputs in `outputs/` directory for debugging

## Contributing

The project is in active development. Current priorities:

1. **Phase III Implementation**: Complete paper writing phase
2. **Prompt Engineering**: Optimize LLM prompts for better output quality
3. **Quiet Mode**: Reduce verbose logging for production use
4. **Documentation**: Improve user guides and API documentation

## License

[License information to be added]

## Academic Goals

Target: **20% publication success rate** in generating papers suitable for analytic philosophy journals through systematic quality control and comprehensive development processes.
