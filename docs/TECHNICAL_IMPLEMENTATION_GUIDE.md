# Technical Implementation Guide

## Priority 1: Phase II.1 PDF Reading Enhancement

### Current State Analysis
Location: `src/phases/phase_two/phase_2_1_literature_reading.py`
Current approach: Basic PDF processing with simple content extraction

### Enhancement Plan

#### 1. Structured Prompt Template
```python
PDF_READING_SYSTEM_PROMPT = """You are an expert philosophy researcher conducting a deep analytical reading of academic papers. Your goal is to extract not just content, but the philosophical moves, argumentative structure, and citable insights."""

PDF_READING_TEMPLATE = """
<task>Conduct a deep philosophical analysis of this paper</task>

<extraction_requirements>
<philosophical_content>
- Main thesis (with page number)
- Core arguments (structured list with page references)  
- Key conceptual distinctions
- Methodological approach
- Philosophical tradition/school
</philosophical_content>

<quotable_material>
Extract 3-5 KEY quotes that:
- Capture the author's main claims
- Could be directly cited in our paper
- Include exact page numbers
- Preserve unique terminology
Format: "Quote text" (Author Year, p. X)
</quotable_material>

<argumentative_analysis>
- What philosophical problem does this solve?
- What are the main argumentative moves?
- What objections does the author anticipate?
- What objections does the author miss?
- How does this relate to other positions?
</argumentative_analysis>

<engagement_opportunities>
- Where can we build on this work?
- Where might we disagree?
- What gaps exist in the argument?
- What examples could extend/challenge this?
</engagement_opportunities>
</extraction_requirements>

<output_format>
{
  "thesis": {
    "statement": "...",
    "page": X
  },
  "key_arguments": [...],
  "quotes": [...],
  "engagement_points": [...]
}
</output_format>
"""
```

#### 2. Implementation Steps
```python
class EnhancedLiteratureReader:
    def __init__(self, model_config):
        self.model = model_config
        self.system_prompt = PDF_READING_SYSTEM_PROMPT
        
    def read_paper(self, pdf_path):
        # 1. Extract text with page numbers preserved
        # 2. Apply structured prompt
        # 3. Validate extraction (ensure quotes have page numbers)
        # 4. Store in enhanced format
        pass
```

### Success Metrics
- Each paper yields 3-5 quotable passages with page numbers
- Clear identification of philosophical moves
- Explicit engagement opportunities identified
- Argument structure mapped accurately

## Priority 2: Output Archiving System

### Simple Archive Implementation
```python
import os
import json
import shutil
from datetime import datetime

class PipelineArchiver:
    def __init__(self, archive_root="outputs/archive"):
        self.archive_root = archive_root
        
    def archive_run(self, run_name=None):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_name = run_name or f"run_{timestamp}"
        
        archive_path = os.path.join(self.archive_root, run_name)
        os.makedirs(archive_path, exist_ok=True)
        
        # Critical files to preserve
        files_to_archive = [
            "outputs/final_paper.md",
            "outputs/final_selection.json",
            "outputs/literature_synthesis.json",
            "outputs/key_moves_development/key_moves_development/all_developed_moves.json",
            "outputs/detailed_outline/detailed_outline_final.json"
        ]
        
        # Copy files and create metadata
        metadata = {
            "timestamp": timestamp,
            "run_name": run_name,
            "config_used": self._get_current_config(),
            "files_archived": []
        }
        
        for file_path in files_to_archive:
            if os.path.exists(file_path):
                dest = os.path.join(archive_path, os.path.basename(file_path))
                shutil.copy2(file_path, dest)
                metadata["files_archived"].append(file_path)
        
        # Save metadata
        with open(os.path.join(archive_path, "run_metadata.json"), "w") as f:
            json.dump(metadata, f, indent=2)
            
        return archive_path
```

## Priority 3: Quick Quality Assessment

### Submittability Checker
```python
class SubmittabilityChecker:
    def __init__(self):
        self.criteria = {
            "word_count": (3000, 4000),
            "min_citations": 10,
            "has_abstract": True,
            "has_objections_section": True,
            "sections_min": 5
        }
    
    def check_paper(self, paper_path):
        # Load paper
        with open(paper_path, 'r') as f:
            content = f.read()
            
        results = {
            "word_count": self._check_word_count(content),
            "citations": self._count_citations(content),
            "structure": self._check_structure(content),
            "red_flags": self._check_red_flags(content)
        }
        
        results["submittable"] = all([
            results["word_count"]["in_range"],
            results["citations"]["count"] >= self.criteria["min_citations"],
            results["structure"]["has_required_sections"],
            len(results["red_flags"]) == 0
        ])
        
        return results
```

## Testing Strategy

### Phase II.1 Testing
1. Select 3 test papers from different subfields
2. Run current vs. enhanced extraction
3. Compare:
   - Number of quotes extracted
   - Quality of argument mapping
   - Identification of engagement points
   
### Full Pipeline Testing
1. Run 5 complete pipelines with enhancements
2. Archive all outputs
3. Have professor evaluate submittability
4. Track which papers are closest to threshold

## Model-Specific Optimizations

### Claude-Specific Enhancements
```python
CLAUDE_CONFIG = {
    "system_prompt": True,
    "xml_tags": True,
    "thinking_tags": True,  # For complex reasoning
    "temperature": 0.3,     # Lower for consistency
    "max_tokens": 8192,
    "prefill_assistant": "I'll analyze this philosophical paper systematically.\n\n"
}
```

### Fallback for Other Models
```python
def adapt_prompt_for_model(prompt, model_type):
    if model_type == "openai":
        # Convert XML to markdown headers
        # Remove thinking tags
        # Adjust formatting
        pass
    return prompt
``` 