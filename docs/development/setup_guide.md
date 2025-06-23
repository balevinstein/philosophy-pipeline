# Philosophy Pipeline Setup Guide

This guide helps new collaborators set up the Philosophy Pipeline development environment.

## 🚀 Quick Setup

### 1. **Clone and Install Dependencies**
```bash
git clone [repository]
cd philosophy-pipeline
pip install -r requirements.txt
```

### 2. **Set Up Analysis Papers Directory**

The pipeline needs Analysis journal papers for style guidance and pattern extraction. Many Analysis papers are open access.

```bash
# Create the Analysis papers directory
mkdir -p Analysis_papers

# Download open access Analysis papers (examples)
# You can find these at: https://academic.oup.com/analysis
# Look for papers marked as "Open Access" or use institutional access
```

**Recommended papers to download:**
- Recent Analysis papers from 2020-2024 (any 10-20 papers will do)
- Save as PDF files with descriptive names
- Papers used in current development: `anab031.pdf`, `anab033.pdf`, `anab039.pdf`, `anae045.pdf`

### 3. **Extract Text from PDFs (Optional)**
If you've added new Analysis papers, extract text for better token efficiency:

```bash
# Run the extraction script
python scripts/extract_analysis_cache.py
```

This will:
- Extract TXT versions of PDFs from `Analysis_papers/`
- Save text extracts to `data/analysis_extracts/`
- Create paper index in `analysis_cache/paper_index.json`

**Note**: Text extracts are ~3x more token-efficient than processing PDFs directly.

## 📁 **Expected Directory Structure After Setup**

```
philosophy-pipeline/
├── Analysis_papers/          # Your downloaded PDFs (gitignored)
│   ├── anab031.pdf
│   ├── anab033.pdf
│   └── [... other Analysis papers]
├── data/                     # Curated data (already in repo)
│   ├── philosophical_moves/
│   ├── analysis_extracts/
│   └── style_guides/
├── analysis_cache/           # Generated after extraction (gitignored)
│   ├── extracted_texts/
│   └── paper_index.json
└── [... rest of pipeline]
```

## 🧪 **Testing Your Setup**

### Test Individual Phases:
```bash
# Test Phase I.1 (topic generation)
python run_phase_1_1.py

# Test Phase II.1 (requires Analysis papers)
python run_phase_2_1.py
```

### Test Complete Pipeline:
```bash
# Full pipeline run (takes ~2 hours)
python run_pipeline.py
```

## 🔧 **Development Workflow**

### **Adding New Analysis Papers:**
1. Download PDF to `Analysis_papers/`
2. Run `python scripts/extract_analysis_cache.py`
3. New extracts appear in `analysis_cache/extracted_texts/`

### **Testing Individual Components:**
- See `docs/development/testing_guide.md` for detailed testing procedures
- Each phase can be run independently for development

### **Modifying Philosophical Moves:**
- Edit `data/philosophical_moves/injectable_examples.json`
- Changes take effect immediately in Phase II.7

## 🚨 **Common Issues**

### **"Analysis_papers directory not found"**
- Create the directory: `mkdir Analysis_papers`
- Add at least a few Analysis journal PDFs

### **"No PDF files found"**
- Download PDF files from Analysis journal
- Ensure files have `.pdf` extension
- Check file permissions

### **"ModuleNotFoundError"**
- Install dependencies: `pip install -r requirements.txt`
- Check Python version (3.8+ recommended)

### **"Token limit exceeded"**
- Use TXT extracts instead of PDFs: run `scripts/extract_analysis_cache.py`
- TXT files are automatically used when available

## 📊 **Resource Requirements**

**Minimum Setup:**
- Python 3.8+
- 2GB free disk space
- OpenAI API key (set in `.env`)
- 5-10 Analysis journal PDFs

**Recommended Setup:**
- 20+ Analysis journal PDFs
- Text extracts generated
- Claude API access (for PDF processing)

## 🤝 **Collaboration Notes**

**What's in the repo:**
- ✅ All pipeline code
- ✅ Curated philosophical moves database
- ✅ TXT extracts from Analysis papers
- ✅ Style guides and examples

**What you need to add:**
- ❌ Analysis journal PDFs (not in repo due to size/copyright)
- ❌ Your `.env` file with API keys
- ❌ Generated outputs (in `outputs/`, gitignored)

**Best practices:**
- Use TXT extracts when possible (more efficient)
- Test individual phases before full pipeline runs
- Add new philosophical moves to the curated database
- Follow the documentation structure for new features 