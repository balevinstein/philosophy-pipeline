# Analysis Journal Style Guide

*For use in the philosophy paper generation pipeline*

## Overview

This guide contains style patterns extracted from Analysis journal papers to ensure generated papers match the distinctive Analysis voice and structure.

## Core Characteristics

- **4,000 word limit** - extremely tight constraints
- **Numbered sections** (1, 2.1, 2.2) with clear hierarchy
- **Conversational but rigorous** - heavy use of "I argue", "I will show"
- **Concrete examples** introduced early and revisited throughout
- **Strategic literature** - focus on 2-3 key figures, not comprehensive review
- **Clean structure** - thesis stated by end of page 1

## Voice & Tone Guidelines

**First Person Usage:**
- "I argue that...", "I will show...", "My response is..."
- "In this paper, I develop...", "I contend that..."

**Direct Reader Engagement:**
- "Consider this case...", "You might think..."
- "Notice that...", "Suppose that..."

**Accessibility:**
- Avoid excessive jargon
- Define technical terms immediately upon introduction
- Target sentence length: 15-25 words average
- Professional but conversational tone

## Structure Patterns

### Opening Sequence (First 300 words)
1. **Abstract** (75-100 words max) - concise statement of thesis and contribution
2. **Keywords** (4-6 terms) - strategic indexing terms
3. **Problem introduction** with concrete example by second paragraph
4. **Thesis statement** clearly stated by end of page 1  
5. **Brief roadmap** ("In section 2, I will...")

### Typical Section Structure
```
Section 1: Introduction + thesis (400-600 words)
Sections 2-3: Core arguments (800-1200 words each)  
Sections 4-5: Objections & responses (600-900 words each)
Section 6: Conclusion (300-400 words)
```

## Example Usage Patterns

**Early Introduction:**
- Core example appears by second paragraph
- Concrete, everyday scenarios (walking together, committee decisions, conversations)

**Systematic Revisiting:**
- Return to same example from multiple analytical angles
- Use example to test different aspects of theory
- Examples do argumentative work, not just illustration

**Grounding Abstract Analysis:**
- Move from concrete case to general principle
- Use examples to clarify conceptual distinctions
- Test theories against intuitive cases

## Literature Engagement

**Citation Style:**
- Inline citations: (Author Year: page)
- Minimal footnotes - only for clarifications or asides

**Strategic Selection:**
- Focus on 2-3 key interlocutors rather than comprehensive review
- Cite to position argument, not demonstrate scholarship
- Literature woven throughout argument flow

**Integration Approach:**
- Brief context-setting rather than extended literature review
- Engage with specific claims, not general positions
- Use literature to sharpen own position

## Implementation in Pipeline

- Analysis papers randomly selected each run for style reference
- Patterns integrated into Phase III.1 writing prompts
- Local cache at `./analysis_cache/` (git-ignored)
- Focus on systematic development over dramatic flourishes

## Key Differentiators from Other Journals

- **Efficiency over comprehensiveness** - tight word limits drive focus
- **Accessibility over technicality** - readable by general philosophy audience  
- **Systematic over dramatic** - steady development rather than surprising turns
- **Conversational over formal** - more personal voice than typical journals
- **Example-driven** - concrete cases central to argumentation 