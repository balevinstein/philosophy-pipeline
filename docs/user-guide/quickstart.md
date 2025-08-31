# Quick Start Guide

Generate your first AI philosophy paper in under 3 hours! This guide assumes you've completed the [Installation Guide](installation.md).

## 🚀 Option 1: Complete Pipeline (Recommended)

The fastest way to get a publication-ready paper using the modern CLI interface:

```bash
# Activate environment
source venv/bin/activate

# Run complete pipeline with monitoring
python pipeline_cli.py run --full --track-costs --profile
```

**Note**: This requires literature PDFs in the `papers/` directory. See [Literature Setup](#literature-setup) below.

**Duration**: ~130 minutes  
**Output**: Complete philosophy paper in `outputs/final_paper.md`

## 📚 Literature Setup

You need philosophy papers for the system to analyze and cite. Here are three options:

### Option A: Sample Papers (Fastest)
```bash
# Copy provided sample papers
cp sample_output_papers/paper_1/papers/*.pdf papers/
```

### Option B: Download Specific Papers
Download these papers to the `papers/` directory:
- Chalmers & Jackson - "Analysis and Reductive Explanation"
- Quine - "Two Dogmas of Empiricism" 
- Pritchard - "Anti-Luck Epistemology"

### Option C: Use Literature Search
```bash
# Start Rivet server (separate terminal)
cd rivet && node server.js

# Run literature search  
python pipeline_cli.py run --phase 1.2

# Check outputs/literature_research_papers.md for required papers
# Download suggested papers to papers/ directory
```

## ⚡ Option 2: Essential Phases Only

Skip topic generation and run the core pipeline:

```bash
# Essential phases for paper generation
python pipeline_cli.py run --phases 2.1-2.8,3.1,3.2
```

**Duration**: ~120 minutes  
**Requirements**: Literature PDFs in `papers/` directory

## 🎯 Option 3: Individual Phase Exploration

Run specific phases to understand the system:

```bash
# Generate and select topic
python pipeline_cli.py run --phase 1.1

# Process literature 
python pipeline_cli.py run --phase 2.1

# Develop framework
python pipeline_cli.py run --phase 2.2

# Create key arguments
python pipeline_cli.py run --phase 2.3

# Generate final paper
python pipeline_cli.py run --phases 3.1,3.2
```

## 📊 Monitor Progress

Track your pipeline execution:

```bash
# Check current status
python pipeline_cli.py status

# List available phases
python pipeline_cli.py list --detailed

# Monitor real-time metrics
python pipeline_cli.py monitor --metrics
```

## 🔍 Interactive Mode

For learning and debugging:

```bash
# Interactive execution with confirmations
python pipeline_cli.py run --full --interactive

# Debug specific phase
python pipeline_cli.py debug --phase 2.3
```

## Expected Output

After a successful run, you'll have:

### Primary Output
- **`outputs/final_paper.md`** - Publication-ready philosophy paper

### Supporting Files
```
outputs/
├── final_selection.json              # Selected topic
├── literature_synthesis.json         # Literature analysis  
├── framework_development/           # Core arguments
├── key_moves_development/           # Developed positions
├── detailed_outline/               # Comprehensive outline
├── phase_2_5_intelligent_consolidation/  # Quality analysis
├── phase_2_6_holistic_review/      # Expert review
├── phase_2_7_refined_context.json  # Refinements
├── phase_2_8_writing_context.json  # Writing aids
├── phase_3_1_draft.md              # Complete draft
└── final_paper_metadata.json       # Paper metadata
```

## Sample Generated Paper

Here's what you can expect - a recent pipeline output:

**Title**: "Distinguishing Epistemic from Moral Blame in Professional Contexts"

**Structure**:
- **Length**: 2,318 words (Analysis journal efficiency)
- **Sections**: 5 focused sections with clear argumentation
- **Style**: Conversational rigor with immediate case engagement
- **Examples**: Professional contexts (medical, legal, financial)
- **Quality**: Publication-ready with proper citations

**Key Features**:
- Immediate engagement with concrete case studies
- Systematic theoretical distinctions
- Professional application examples
- Analysis journal writing standards

## Performance Expectations

| Phase | Duration | Description |
|-------|----------|-------------|
| II.1 | ~5 min | Literature processing |
| II.2 | ~10 min | Framework development |
| II.3 | ~45 min | Key moves development |
| II.4 | ~53 min | Detailed outline |
| II.5 | ~85 sec | Quality consolidation |
| II.6 | ~90 sec | Expert review |
| II.7 | ~20 sec | Targeted refinement |
| II.8 | ~92 sec | Writing optimization |
| III.1 | ~12 min | Section writing |
| III.2 | ~2.8 min | Final integration |
| **Total** | **~130 min** | **Complete paper** |

## Quality Features

Your generated paper will include:

### 🎯 **Philosophical Rigor**
- Logically structured arguments
- Clear premises and conclusions
- Theoretical coherence

### 📖 **Literature Integration**  
- Proper citations
- Scholarly engagement
- Relevant source integration

### 🏛 **Academic Structure**
- Professional formatting
- Standard philosophical sections
- Introduction → Arguments → Objections → Conclusion

### ✨ **Analysis Journal Standards**
- Conversational tone with rigor
- Immediate engagement
- Example-driven argumentation
- "Every word earns its place" efficiency

## Cost Expectations

Typical full pipeline costs:
- **Anthropic API**: $8-12 USD
- **OpenAI API**: $2-4 USD (if used)
- **Total**: $10-16 USD per complete paper

Monitor costs in real-time:
```bash
python pipeline_cli.py cost status
python pipeline_cli.py cost report --period day
```

## Troubleshooting Quick Start

### API Rate Limits
```bash
# Pipeline automatically handles rate limits
# Just wait for completion - no action needed
```

### Missing Literature
```bash
# Check what papers are needed
ls papers/
# Should contain .pdf files

# If empty, use sample papers:
cp sample_output_papers/paper_1/papers/*.pdf papers/
```

### Memory Issues
```bash
# Monitor memory usage
python pipeline_cli.py monitor --metrics

# Close other applications if needed
```

### Validation Failures
```bash
# Check environment setup
python pipeline_cli.py validate

# Fix any failed checks before proceeding
```

## Next Steps

Once you have your first paper:

1. **[CLI Reference](cli-reference.md)** - Learn all available commands
2. **[Configuration](configuration.md)** - Customize pipeline behavior  
3. **[Advanced Usage](../examples/advanced-configuration.md)** - Complex configurations
4. **[Troubleshooting](troubleshooting.md)** - Common issues and solutions

## Getting Help

If you encounter issues:

1. **Check Status**: `python pipeline_cli.py status`
2. **Validate Environment**: `python pipeline_cli.py validate`
3. **Review Outputs**: Check `outputs/` directory for error messages
4. **Consult Troubleshooting**: [troubleshooting.md](troubleshooting.md)

Ready to dive deeper? Continue with the **[CLI Reference](cli-reference.md)** to master all available commands!