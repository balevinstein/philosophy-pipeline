# Prompt Engineering Overhaul Plan

## Phase-by-Phase Improvements

### Global Changes (All Phases)
1. **Add XML structure to all prompts**
   ```
   <task>
   <context>
   <requirements>
   <output_format>
   ```

2. **Implement role-based system prompts**
   - Development workers: "You are a professional philosophy researcher..."
   - Critic workers: "You are a peer reviewer for top philosophy journals..."
   - Refinement workers: "You are an expert editor specializing in academic philosophy..."

3. **Add thinking tags** for complex reasoning (especially Phase II.3, III.1)

### Phase I.2: Literature Search Enhancement
- Add search strategy prompts that generate multiple query variations
- Include instructions for identifying seminal vs recent papers
- Add citation count/impact awareness

### Phase II.1: PDF Reading Enhancement
Critical improvements for literature engagement:
- Add structured extraction prompts:
  ```xml
  <extract>
    <main_thesis>
    <key_arguments>
    <methodological_approach>
    <quotable_passages>
    <critique_points>
  </extract>
  ```
- Include "deep reading" instructions focusing on:
  - Exact page numbers for key claims
  - Direct quotes with context
  - Author's specific terminology
  - Dialectical moves and responses

### Phase II.3: Key Moves Development
- Add philosophical depth requirements:
  - "Identify at least two potential objections to each claim"
  - "Distinguish your position from at least two similar views"
  - "Explain what's at stake philosophically"

### Phase III.1: Section Writing
- Implement academic voice guidelines
- Add citation integration instructions
- Include "philosophical sophistication checkers"

## Implementation Strategy
1. Start with Phase II.1 (PDF reading) - biggest impact on literature engagement
2. Then Phase II.3 (key moves) - core argument quality
3. Then Phase III.1 (section writing) - output quality
4. Finally Phase I enhancements 