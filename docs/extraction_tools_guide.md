# Extraction and Analysis Tools Guide

## Overview
This guide documents the various extraction and analysis tools created to build the philosophical moves database from Analysis journal papers.

## Core Extraction Tools

### 1. `extract_pdf_text.py`
- **Purpose**: Extract text from PDF files to make them searchable
- **Usage**: `python extract_pdf_text.py <pdf_file>`
- **Output**: Plain text file in `text_extracts/` directory

### 2. `extract_more_pdfs.py`
- **Purpose**: Batch extraction of multiple PDFs
- **Usage**: `python extract_more_pdfs.py`
- **Note**: Processes all PDFs in `Analysis_papers/` directory

### 3. `extract_philosophical_moves.py`
- **Purpose**: Extract philosophical moves from Analysis papers using GPT-4
- **Output**: `philosophical_moves_database.json` with categorized moves
- **Categories**: Offensive, Defensive, Constructive, Meta

### 4. `extract_all_philosophical_moves.py`
- **Purpose**: Enhanced extraction with better prompts and validation
- **Improvements**: Self-contained context, clear categorization
- **Output**: Comprehensive moves database with metadata

## Analysis Tools

### 1. `analyze_analysis_style.py`
- **Purpose**: Analyze stylistic patterns in Analysis journal papers
- **Features**: Word frequency, sentence structure, argument patterns
- **Output**: Statistical analysis of writing style

### 2. `validate_extraction_quality.py`
- **Purpose**: Validate quality of extracted philosophical moves
- **Metrics**: Context completeness, clarity, categorization accuracy
- **Output**: Quality report with improvement suggestions

### 3. `compare_extraction_to_source.py`
- **Purpose**: Compare extracted moves to source papers
- **Usage**: Verify extraction accuracy and completeness
- **Output**: Side-by-side comparison report

## Curation Tools

### 1. `curate_philosophical_moves.py`
- **Purpose**: Curate and map moves to specific pipeline stages
- **Features**: Quality filtering, stage mapping, example selection
- **Output**: `curated_examples_database.json`

### 2. `extract_philosophical_examples.py`
- **Purpose**: Extract concrete examples from papers
- **Focus**: Real-world scenarios, thought experiments, case studies
- **Output**: Example database for injection into prompts

## Testing Tools

### 1. `compare_hajek_improvements.py`
- **Purpose**: Compare outputs before/after Hájek heuristics
- **Metrics**: Argument quality, error detection, philosophical rigor
- **Output**: Comparative analysis report

### 2. `run_phase_2_*.py`
- **Purpose**: Test individual pipeline phases with enhancements
- **Usage**: `python run_phase_2_3.py` (tests Phase II.3)
- **Output**: Log files with detailed phase outputs

## Usage Workflow

1. **Extract PDFs**: Use `extract_more_pdfs.py` to convert PDFs to text
2. **Extract Moves**: Run `extract_all_philosophical_moves.py` for comprehensive extraction
3. **Validate Quality**: Use `validate_extraction_quality.py` to check results
4. **Curate Database**: Run `curate_philosophical_moves.py` to create pipeline-ready database
5. **Test Integration**: Use `run_phase_2_*.py` scripts to test specific phases

## Database Structure

### philosophical_moves_database.json
```json
{
  "moves": [
    {
      "move_type": "category",
      "description": "what the move does",
      "example": "verbatim text",
      "source": "paper title",
      "context": "surrounding context"
    }
  ]
}
```

### curated_examples_database.json
```json
{
  "offensive_moves": [...],
  "defensive_moves": [...],
  "constructive_moves": [...],
  "meta_moves": [...],
  "usage_guide": {...}
}
```

## Best Practices

1. **Always validate** extraction quality before integration
2. **Preserve context** - moves should be self-contained
3. **Test incrementally** - verify improvements at each phase
4. **Document changes** - log what moves were added where

## Future Improvements

1. **Automated quality scoring** for extracted moves
2. **ML-based move retrieval** based on topic relevance
3. **Pattern clustering** to identify move families
4. **Citation graph analysis** for literature engagement patterns 