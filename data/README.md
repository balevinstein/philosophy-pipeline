# Philosophy Pipeline Data Directory

This directory contains consolidated, curated data files used by the philosophy paper generation pipeline.

## 📁 Directory Structure

```
data/
├── README.md                          # This documentation file
├── philosophical_moves/               # Consolidated philosophical pattern database
│   ├── injectable_examples.json      # Main database used by pipeline (143 examples)
│   ├── curated_moves.json            # Additional curated moves
│   ├── categorized_moves.json        # Large categorized database
│   ├── preview.md                     # Human-readable preview
│   └── archive/                       # Historical versions for reference
│       ├── v1/                        # Original philosophical_moves_db
│       └── v2/                        # Second version philosophical_moves_db_v2
├── analysis_extracts/                 # Text extracts from Analysis journal papers
│   ├── anaa008.txt                    # TXT versions of Analysis papers
│   ├── anaa035.txt                    # (21 files total, token-efficient for LLM processing)
│   └── [... other extracts]
├── style_guides/                      # Analysis journal style documentation  
│   └── analysis_style_guide.md       # Analysis writing patterns and conventions
└── examples/                          # Extracted philosophical examples
    ├── philosophical_examples_database.json  # Main examples database
    ├── philosophical_examples_database.xml   # XML version
    └── [... paper-specific examples]
```

## 🎯 Purpose & Usage

### **Philosophical Moves Database** (`philosophical_moves/`)
- **Primary file**: `injectable_examples.json` - Used by pipeline Phases II.2-III.2
- **Content**: 143 curated philosophical moves extracted from Analysis papers
- **Categories**: abstract_development, key_moves_development, outline_development, section_writing, critics_all
- **Usage**: Referenced by workers for Analysis journal style patterns

### **Analysis Extracts** (`analysis_extracts/`)
- **Purpose**: Token-efficient TXT versions of Analysis journal papers
- **Source**: Generated from PDFs in `../Analysis_papers/` 
- **Usage**: Used instead of full PDFs in non-initial phases for better token efficiency
- **Performance**: ~3x token reduction compared to PDF processing

### **Style Guides** (`style_guides/`)
- **Content**: Documentation of Analysis journal writing conventions
- **Usage**: Referenced by prompt engineering and style optimization
- **Patterns**: Conversational rigor, immediate engagement, example-driven arguments

### **Examples** (`examples/`)
- **Content**: Structured philosophical examples with context
- **Usage**: Additional examples database for move development
- **Format**: JSON and XML versions available

## 🔄 Relationship to Other Directories

**Input Sources** (not in this directory):
- `../Analysis_papers/` - Raw PDF files (42 papers, 14MB, gitignored)
- `../papers/` - Literature papers for specific paper generation

**Generated Outputs** (not in this directory):
- `../outputs/` - All pipeline-generated content and papers

## 🚚 Migration Notes

**2025 Data Organization:**
- Consolidated from scattered locations: `outputs/curated_moves/`, `outputs/philosophical_moves_db/`, `analysis_cache/`, `text_extracts/`
- Updated pipeline references in `run_phase_2_7.py` and documentation
- Preserved historical databases in `archive/` subdirectories
- All data committed to repository (unlike raw PDFs)

## 🎯 For Developers

**Key Files to Know:**
- `philosophical_moves/injectable_examples.json` - Main database used by pipeline
- `analysis_extracts/*.txt` - Token-efficient Analysis paper content  
- `style_guides/analysis_style_guide.md` - Style patterns for prompts

**Adding New Data:**
- New philosophical moves → `philosophical_moves/injectable_examples.json`
- New Analysis extracts → `analysis_extracts/` (use extraction scripts)
- New style documentation → `style_guides/`

**Pipeline References:**
- Phase II.7: Loads `philosophical_moves/injectable_examples.json`
- Phase II.2-4: Can reference Analysis extracts for pattern guidance  
- Phase III.1-2: Uses style guides for Analysis journal integration 