#!/usr/bin/env python3
"""
Analysis Paper Style Extraction
Analyzes Analysis papers to extract systematic style patterns for integration into philosophy pipeline
"""

from pathlib import Path
import json
from typing import List, Dict, Any
import random

from src.utils.api import APIHandler


def analyze_analysis_style():
    """Analyze Analysis papers to extract style patterns"""
    
    # Select papers for analysis (mix of short and medium length)
    papers_dir = Path("./Analysis_papers")
    short_papers = ["anae044 (1).pdf", "anae045 (1).pdf", "anad086.pdf"]
    medium_papers = ["anae047 (1).pdf", "anae043 (1).pdf", "anad104 (1).pdf"]
    
    # Select 2 short + 1 medium for comprehensive analysis (limit for context)
    selected_papers = short_papers[:2] + medium_papers[:1]
    
    print(f"Analyzing style patterns from: {selected_papers}")
    
    # Style analysis prompt template for each paper
    analysis_prompt_template = """You are analyzing a paper from the journal Analysis to extract systematic style patterns for automated philosophy paper generation. 

This is paper {paper_index} of {total_papers} you'll analyze. Please analyze this specific paper and provide detailed observations on:

## 1. OPENING AND PROBLEM FRAMING
- How does this paper introduce the philosophical problem?
- What level of motivation vs. immediate problem statement?
- How much context before stating thesis?

## 2. ARGUMENT DEVELOPMENT PATTERNS  
- How does this paper structure individual arguments?
- Use of examples vs. purely conceptual analysis?
- Balance of intuition pumps vs. formal reasoning?

## 3. LITERATURE INTEGRATION
- How does this paper cite and engage with other work?
- Dense footnotes vs. inline citations?
- How much literature review vs. direct argumentation?

## 4. VOICE AND TONE
- Level of formality and precision in this paper
- Use of first person vs. impersonal constructions  
- Sentence length and complexity patterns

## 5. TRANSITIONS AND FLOW
- How does this paper move between sections?
- Signposting and meta-commentary patterns
- Building momentum vs. systematic coverage

## 6. OBJECTIONS AND RESPONSES
- Where this paper places objections (scattered vs. dedicated section)
- How it introduces counterarguments
- Depth of response vs. acknowledgment

## 7. CONCLUSIONS
- How this paper synthesizes and concludes
- Gesture toward future work vs. clean closure
- Final paragraph patterns

Provide specific examples and concrete guidelines from THIS PAPER that could be used to train an AI system to write in Analysis style. Focus on actionable patterns rather than general observations.

Paper title: {paper_name}"""

    # Initialize API handler
    api_handler = APIHandler()
    
    # Analyze each paper individually
    paper_analyses = []
    
    for i, paper_name in enumerate(selected_papers):
        paper_path = papers_dir / paper_name
        
        print(f"\nAnalyzing paper {i+1}/{len(selected_papers)}: {paper_name}")
        
        # Create specific prompt for this paper
        prompt = analysis_prompt_template.format(
            paper_index=i+1,
            total_papers=len(selected_papers),
            paper_name=paper_name
        )
        
        try:
            # Use the APIHandler with PDF support
            response = api_handler._call_anthropic_with_pdf(
                prompt=prompt,
                pdf_path=paper_path,
                config={
                    "model": "claude-3-5-sonnet-20241022",
                    "max_tokens": 8192,
                    "temperature": 0.3
                }
            )
            
            paper_analyses.append({
                "paper_name": paper_name,
                "analysis": response
            })
            
            print(f"✅ Completed analysis of {paper_name}")
            
        except Exception as e:
            print(f"❌ Error analyzing {paper_name}: {e}")
            continue
    
    # Create synthesis prompt to combine individual analyses
    synthesis_prompt = f"""You have analyzed {len(paper_analyses)} papers from the journal Analysis. Now please synthesize these individual analyses into a comprehensive style guide for automated philosophy paper generation.

Based on the {len(paper_analyses)} paper analyses provided, create:

## ANALYSIS JOURNAL STYLE GUIDE

### 1. OPENING PATTERNS
Synthesize the common patterns for how Analysis papers open and frame problems.

### 2. ARGUMENT STRUCTURE  
Identify the typical argument development patterns across the papers.

### 3. LITERATURE ENGAGEMENT
Describe the characteristic way Analysis papers engage with existing work.

### 4. VOICE CHARACTERISTICS
Define the distinctive voice and tone of Analysis papers.

### 5. FLOW AND TRANSITIONS
Characterize how Analysis papers manage transitions and flow.

### 6. OBJECTION HANDLING
Describe typical patterns for addressing objections.

### 7. CONCLUSION STYLES
Identify characteristic conclusion patterns.

### 8. KEY DIFFERENTIATORS
What makes Analysis papers distinctive vs. other philosophy journals?

### 9. ACTIONABLE GUIDELINES
Provide specific, concrete guidelines that could be programmed into an AI system to generate Analysis-style papers.

Provide both descriptive analysis and prescriptive guidelines. Focus on patterns that appeared across multiple papers.

INDIVIDUAL PAPER ANALYSES:
"""
    
    # Add individual analyses to synthesis prompt
    for analysis in paper_analyses:
        synthesis_prompt += f"\n\n--- {analysis['paper_name']} ---\n{analysis['analysis']}\n"
    
    print(f"\nSynthesizing {len(paper_analyses)} analyses into comprehensive style guide...")
    
    try:
        # Generate synthesis
        synthesis_response = api_handler._call_anthropic(
            prompt=synthesis_prompt,
            config={
                "model": "claude-3-5-sonnet-20241022", 
                "max_tokens": 8192,
                "temperature": 0.4
            }
        )
        
        # Save comprehensive output
        analysis_output = {
            "analyzed_papers": selected_papers,
            "individual_analyses": paper_analyses,
            "synthesized_style_guide": synthesis_response,
            "extraction_date": "2025-01-02",
            "purpose": "Analysis style integration for philosophy paper pipeline"
        }
        
        # Save to outputs
        output_dir = Path("./outputs")
        output_dir.mkdir(exist_ok=True)
        
        with open(output_dir / "analysis_style_guide.json", "w") as f:
            json.dump(analysis_output, f, indent=2)
        
        with open(output_dir / "analysis_style_guide.md", "w") as f:
            f.write("# Analysis Journal Style Guide\n\n")
            f.write(f"*Extracted from: {', '.join(selected_papers)}*\n\n")
            f.write(synthesis_response)
        
        print("\n✅ Style analysis completed!")
        print("📄 Outputs saved to:")
        print("   - outputs/analysis_style_guide.json") 
        print("   - outputs/analysis_style_guide.md")
        
        return analysis_output
        
    except Exception as e:
        print(f"❌ Error during synthesis: {e}")
        raise


if __name__ == "__main__":
    analyze_analysis_style() 