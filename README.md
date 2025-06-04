# AI-Driven Philosophy Paper Generator

A system that generates complete publishable-quality analytic philosophy papers through a structured multi-phase development pipeline.

## Project Overview

This project demonstrates that large language models can systematically develop philosophical papers suitable for academic publication. Targeting the journal Analysis (4,000-word limit), the system:

1. **Generates and evaluates** potential paper topics
2. **Develops detailed** argumentative frameworks with literature integration
3. **Creates structured** comprehensive outlines with key moves
4. **Produces complete** publication-ready draft papers
5. **Refines through** global analysis and integration

The goal is to achieve a ~20% success rate in generating publishable-quality papers while maintaining philosophical rigor and originality.

## Current Status

**🎉 COMPLETE END-TO-END PIPELINE WORKING!** 

The full pipeline now generates complete philosophy papers from topic generation through final publication-ready drafts:

- ✅ **Phase I.1** (Topic Generation): Complete
- ✅ **Phase I.2** (Literature Research): Complete - find relevant literature on the web
- ✅ **Phase II.1** (Literature Processing): Complete - uses Claude's native PDF processing
- ✅ **Phase II.2** (Framework Development): Complete - framework-driven paper development
- ✅ **Phase II.3** (Key Moves Development): Complete - sophisticated argument development
- ✅ **Phase II.4** (Detailed Outline Development): Complete - comprehensive outline with literature mapping
- ✅ **Phase II.5** (Context Consolidation): Complete - unified context for Phase III
- ✅ **Phase III.1** (Section-by-Section Writing): Complete - detailed section writing with critique and refinement
- ✅ **Phase III.2** (Global Integration): Complete - publication-ready paper with professional formatting

### Latest Achievements

- **Complete Papers**: Generated 3000+ word philosophy papers with coherent argumentation
- **Professional Quality**: Proper academic titles, structured sections, theoretical frameworks
- **Integration Pipeline**: Global analysis and refinement for publication-ready output
- **Advanced Models**: Upgraded to Claude Sonnet 4 for enhanced quality and capability
- **Real Philosophical Content**: Original arguments with case studies and objection responses

### Analysis Journal Integration (Latest)

**🎯 Enhanced Analysis Pattern Integration** - Systematic integration of Analysis journal style patterns across key phases:

- **Phase II.2** (Abstract Development): Enhanced with Analysis abstract examples and conversational tone
- **Phase II.3** (Key Moves Development): Integrated curated philosophical examples database (14 examples from 3 Analysis papers)
- **Phase II.4** (Detailed Outline Development): Enhanced with Analysis structural patterns and PDF guidance

**Key Features:**
- **Empirical Analysis Patterns**: Extracted from 4 recent Analysis papers to identify structural conventions
- **Curated Examples Database**: 14 high-quality philosophical examples (thought experiments, test cases, counterexamples)
- **Phase-Aware PDF Integration**: Different Analysis papers selected for different development phases
- **Enhanced Prompts**: XML-tagged directive guidance for Analysis style compliance

**Benefits:**
- **Compound Improvements**: Each phase builds on Analysis-aware development from previous phases
- **Journal-Specific Quality**: Output aligns with Analysis journal conventions (direct engagement, conversational voice, example-driven arguments)
- **Systematic Pattern Application**: Consistent Analysis style across framework, argument development, and structure

### Sample Output

The pipeline recently generated: **"Attention Mechanisms and the Foundations of Epistemic versus Moral Blame"** - a 2,691-word philosophy paper with:
- Coherent theoretical framework distinguishing epistemic from moral responsibility
- Case studies from medical diagnosis (Dr. Adams vs. Dr. Baker)
- Integration of cognitive science and normative theory
- Professional academic structure with objections and responses

### Architecture & Code Quality

- **Mature Codebase**: Core functionality complete with robust error handling
- **Typed Workers**: Development, Critique, and Refinement workers in `src/phases/core`
- **Hybrid Architecture**: Python orchestration with Rivet for complex AI workflows
- **Production Ready**: Full pipeline tested and working reliably

Detailed system design available in `docs/architecture-doc.md`

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

### Quick Start: Complete End-to-End Pipeline

**Note**: This assumes you already have literature papers in the `papers/` directory. For a complete from-scratch run, start with the detailed instructions below.

Once you have literature papers in the `papers/` directory, you can run the complete pipeline to generate a finished philosophy paper:

```bash
# Activate virtual environment
source venv/bin/activate

# Run complete pipeline (takes ~105 minutes)
python run_phase_2_1.py  # Literature processing
python run_phase_2_2.py  # Framework development  
python run_phase_2_3.py  # Key moves development
python run_phase_2_4.py  # Detailed outline
python run_phase_2_5.py  # Context consolidation
python run_phase_2_6.py  # Writing context preparation
python run_phase_3_1.py  # Section-by-section writing
python run_phase_3_2.py  # Global integration & final paper
```

**Final Output**: `outputs/final_paper.md` - A complete, publication-ready philosophy paper

### Detailed Step-by-Step Instructions

#### Phase I: Topic Development

##### 1. Generate and select a topic

```bash
python run_phase_1_1.py
```

**Output**: `outputs/final_selection.json`

##### 2. Search papers for literature engagement

```bash
python run_phase_1_2.py
```

After completion, check `literature_research_papers.md` for required papers and **manually download PDFs** to the `papers/` directory.

#### Phase II: Framework & Content Development

##### 3. Process literature

**Requires**: PDFs in `papers/` directory
**Uses**: Claude for PDF processing

```bash
python run_phase_2_1.py
```

**Output**:
- `outputs/literature_synthesis.json`
- `outputs/literature_synthesis.md`

##### 4. Develop framework

```bash
python run_phase_2_2.py
```

**Output**: `outputs/framework_development/` containing abstract, outline, and key moves

##### 5. Develop Key Moves

```bash
python run_phase_2_3.py
```

**Duration**: ~45 minutes for 2 key moves
**Output**: `outputs/key_moves_development/key_moves_development/all_developed_moves.json`

##### 6. Create Detailed Outline

```bash
python run_phase_2_4.py
```

**Duration**: ~15 minutes
**Output**: `outputs/detailed_outline/detailed_outline_final.json`

##### 7. Consolidate Context

**Requires**: Rivet server running (`cd rivet && node server.js`)

```bash
python run_phase_2_5.py
```

**Output**: `outputs/phase_3_context.json` (comprehensive context for Phase III)

##### 8. Prepare Writing Context

```bash
python run_phase_2_6.py
```

**Output**: `outputs/phase_3_writing_context.json` (section-specific writing guidance)

#### Phase III: Paper Writing & Integration

##### 9. Section-by-Section Writing

```bash
python run_phase_3_1.py
```

**Duration**: ~20 minutes
**Output**: 
- `outputs/phase_3_1_draft.md` (complete draft)
- `outputs/phase_3_1_progress.json` (writing metadata)

##### 10. Global Integration & Final Paper

```bash
python run_phase_3_2.py
```

**Duration**: ~5 minutes
**Output**: 
- `outputs/final_paper.md` (publication-ready paper)
- `outputs/final_paper_metadata.json` (comprehensive metadata)

## Output Quality

The pipeline generates **complete publication-ready philosophical papers**:

- **Sophisticated Arguments**: Logically structured with clear premises, development, and conclusions
- **Literature Integration**: Proper citations and scholarly engagement with relevant sources
- **Academic Structure**: Professional sections from introduction through objections to conclusion
- **Philosophical Rigor**: Maintains theoretical coherence and argumentative depth
- **Professional Formatting**: Clean markdown with proper titles, headers, and academic style
- **Original Content**: Novel philosophical positions with case studies and theoretical frameworks

### Sample Complete Paper Output

Recent pipeline output: **"Attention Mechanisms and the Foundations of Epistemic versus Moral Blame"**

**Structure**: 7 sections, 2,691 words
- Introduction with compelling case studies (Dr. Adams vs. Dr. Baker)
- Theoretical framework distinguishing cognitive mechanisms
- Cognitive foundations with neuropsychological evidence
- Case studies across medical, academic, and professional contexts
- Practical applications for institutional design
- Objections and responses addressing integration concerns
- Comprehensive conclusion with future research directions

**Quality Indicators**:
- Coherent argumentation throughout
- Integration of philosophy and cognitive science
- Original theoretical distinctions
- Real-world applications and implications

### Sample Output Structure

```
outputs/
├── final_selection.json           # Phase I topic selection
├── literature_synthesis.json      # Phase II.1 literature analysis
├── framework_development/         # Phase II.2 core framework
├── key_moves_development/         # Phase II.3 developed arguments
├── detailed_outline/              # Phase II.4 comprehensive outline
├── phase_3_context.json          # Phase II.5 consolidated context
├── phase_3_writing_context.json  # Phase II.6 writing guidance
├── phase_3_1_draft.md            # Phase III.1 complete draft
├── phase_3_1_progress.json       # Phase III.1 writing metadata
├── final_paper.md                # Phase III.2 publication-ready paper
└── final_paper_metadata.json     # Phase III.2 comprehensive metadata
```

## Project Structure

```
philosophy-pipeline/
├── docs/                    # Documentation
│   ├── prompts/            # Prompt engineering guides
│   └── archive/            # Archived documentation
├── tests/                  # Test suite
├── src/                    # Source code
├── papers/                 # Literature PDFs
├── outputs/               # Generated outputs
└── config/                # Configuration files
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
- **Phase II.6**: ~3 minutes (writing context preparation)
- **Phase III.1**: ~20 minutes (section-by-section writing with critique/refinement)
- **Phase III.2**: ~5 minutes (global integration and final paper generation)
- **Total Pipeline**: ~105 minutes for complete philosophy paper generation

### Model Usage

- **Primary Models**: Claude Sonnet 4 (upgraded from 3.5 for better quality)
- **Specialized Tasks**: OpenAI o1-preview for complex reasoning (Phase II development)
- **Token Efficiency**: Optimized prompts with targeted context for cost efficiency
- **Quality Control**: Multi-stage critique and refinement at section and paper levels

## Troubleshooting

### Common Issues

1. **Rivet server not running**: Phase II.5 requires `node server.js` in rivet directory
2. **Missing PDFs**: Download papers to `papers/` directory before Phase II.1
3. **API rate limits**: The pipeline respects rate limits but may take longer during high usage
4. **Virtual environment**: Always activate with `source venv/bin/activate`
5. **Phase III.1 context missing**: Ensure Phase II.6 completed successfully before running Phase III.1
6. **Final paper quality**: Phase III.2 requires Claude Sonnet 4; check config for correct model settings

### Getting Help

- Check `architecture-doc.md` for detailed system design
- Review configuration in `config/conceptual_config.yaml`
- Examine outputs in `outputs/` directory for debugging
- Look at `debug_integration_response.txt` if Phase III.2 has issues

## Contributing

The project has achieved **core functionality completion** with a working end-to-end pipeline. Current priorities for enhancement:

1. **Citation Accuracy**: Implement fact-checking and citation verification systems
2. **Prompt Optimization**: Fine-tune prompts for even higher quality philosophical content  
3. **Length Control**: Better word count targeting for different journal requirements
4. **Multiple Topics**: Expand testing across diverse philosophical domains
5. **Quality Metrics**: Develop automated assessment of philosophical rigor and originality

## Academic Goals & Current Achievement

**Target**: 20% publication success rate in generating papers suitable for analytic philosophy journals

**Current Status**: 
- ✅ **Infrastructure Complete**: Full pipeline operational from topic to publication-ready paper
- ✅ **Quality Demonstration**: Generated coherent, structured philosophical arguments
- ✅ **Professional Output**: Academic formatting, proper structure, theoretical rigor
- 🔄 **Next Phase**: Citation accuracy and philosophical depth optimization

The pipeline demonstrates that **systematic LLM-driven philosophical research is feasible** with appropriate architecture and quality control mechanisms.

## License

[License information to be added]

### Running Tests

The test suite is located in the `tests/` directory. To run tests:

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_key_moves_worker.py
```

### Project Structure

```
philosophy-pipeline/
├── docs/                    # Documentation
│   ├── prompts/            # Prompt engineering guides
│   └── archive/            # Archived documentation
├── tests/                  # Test suite
├── src/                    # Source code
├── papers/                 # Literature PDFs
├── outputs/               # Generated outputs
└── config/                # Configuration files
```
