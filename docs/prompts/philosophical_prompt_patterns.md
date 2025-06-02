# Philosophical Prompt Patterns for Pipeline Enhancement

This document contains prompt patterns from the user's personal philosophical work that will be adapted for the philosophy pipeline's critic and development workers.

## 1. Skeptical Friend Prompt

### Introduction
Academic writing benefits enormously from simulating a "skeptical friend" - someone who is simultaneously supportive of your work yet willing to critically examine your claims with intellectual rigor. This document outlines a structured approach to this process, based on the observation that it produces significantly stronger final products when systematically applied.

### Core Principles
1. **Charitable skepticism**: Approach the text with the assumption that it contains valuable ideas, but be willing to question how those ideas are presented and defended.
2. **Claim isolation**: Identify specific claims, especially bold or broad ones, rather than critiquing entire arguments at once.
3. **Steelmanning**: Articulate the strongest possible version of the skeptical position before responding to it.
4. **Implementation feasibility**: Consider practical aspects of implementing theoretical ideas.
5. **Audience perspective**: Anticipate how different readers might react to or misinterpret claims.
6. **Proportional scrutiny**: Apply more scrutiny to claims that are central to the argument or particularly novel/controversial.

### The Skeptical Process

#### Phase 1: Initial Draft Review
1. Read the text in its entirety to understand context
2. Identify the strongest, most interesting claims
3. Note any claims that seem overreaching, underspecified, or insufficiently supported

#### Phase 2: Critical Dissection
For each identified claim:
1. **Isolate the specific claim** (verbatim quotation works best)
2. **Articulate skeptical perspectives**:
   - What assumptions does this claim rely on?
   - What counterexamples might undermine it?
   - How might this be misinterpreted by readers?
   - Does the level of certainty match the evidence?
   - Are there disanalogies or category errors?
   - Does the claim extend beyond the scope of the evidence/arguments presented?
3. **Consider multiple dimensions of criticism**:
   - Theoretical validity
   - Empirical support
   - Scope appropriateness 
   - Definitional clarity
   - Practical implementation

#### Phase 3: Response Formulation
1. Determine if the skepticism reveals a fundamental flaw or merely suggests a need for refinement
2. Identify the minimal modifications needed to address legitimate concerns
3. Restate the claim with appropriate qualifications, specificity, or supporting context
4. Consider if additional evidence is needed

#### Phase 4: Integration
1. Smoothly incorporate the refined claims into the broader text
2. Ensure the modified text flows naturally with surrounding content
3. Consider if the modifications have implications for other parts of the document

### Common Patterns to Target
1. **Causality claims**: Be particularly wary of statements suggesting one thing "explains," "causes," or "determines" another.
2. **Scope generalizations**: Look for claims that apply findings beyond their demonstrated domain.
3. **Novel connections**: Scrutinize assertions of relationships between previously unconnected concepts or fields.
4. **Theoretical-empirical bridges**: Pay special attention to claims that link theoretical constructs to empirical observations.
5. **Descriptive-normative slides**: Watch for places where descriptions of what is subtly become prescriptions about what ought to be.
6. **Embedded assumptions**: Identify unstated assumptions that readers might not share.
7. **Quantification without measurement**: Question claims of "more," "less," "stronger," etc. that lack specific metrics.
8. **Single-cause explanations**: Be skeptical of attributing complex phenomena to single factors.

## 2. Philosophical Heuristics for Argument Evaluation

### Key Heuristics to Adapt:

1. **Check Extreme and Near-Extreme Cases**
   - Apply the argument's principles to edge cases or boundary conditions
   - Examine whether the argument's conclusions remain plausible in limiting scenarios
   - If extreme cases yield counterintuitive results, test with near-extreme cases
   - Use counterexamples at the extremes to identify potential weaknesses

2. **Test for Self-Undermining Views**
   - Check whether the argument's conclusion undermines its own premises
   - Look for reflexive inconsistency
   - Identify when a view falls within its own domain of application
   - Test whether the position violates its own standards

3. **Domain Transformation**
   - Transpose arguments between domains (space ↔️ time ↔️ modality)
   - Test whether parallel reasoning works in analogous contexts
   - Apply successful argument structures from one field to another

4. **Systematic Trial and Error**
   - Systematically explore possible objections and responses
   - Test whether modifications to problematic components preserve strengths
   - Consider hybrid approaches that combine elements of competing views

## 3. Key Adaptation Principles for Pipeline

### For Critic Workers:
- Use claim isolation to target specific thesis statements and key moves
- Apply proportional scrutiny based on centrality to the paper's argument
- Articulate skeptical perspectives using philosophical counterexamples
- Consider multiple reader perspectives (empiricist vs theorist, etc.)

### For Development Workers:
- Anticipate the skeptical friend's likely objections
- Build in qualifications and scope limitations proactively
- Ensure claims are proportional to available evidence

### For Refinement Workers:
- Use the "minimal modifications" approach to address concerns
- Ensure refined claims integrate smoothly with surrounding content
- Check if modifications have implications for other parts of the paper

## 4. Implementation Notes

### "Helpful Asshole" Principle
Critics need explicit permission to be harsh. Sample language:
- "Your job is to find real flaws. The pipeline depends on you catching problems that would make reviewers reject this paper."
- "Be as critical as you would be reviewing for a top journal."
- "Do not be polite or deferential. Be constructive but skeptical."

### Concrete Anchoring
Instead of abstract criteria, use specific questions:
- "Quote the most problematic claim in this section and explain why it would fail peer review"
- "Identify assumptions that a hostile reviewer would immediately challenge"
- "What would a specialist in [relevant subfield] find unconvincing?"

### Pattern Recognition Scaffolding
Use checklist format for systematic evaluation:
```
Check for these specific issues:
☐ Causality claimed without mechanism (quote the claim)
☐ Generalization beyond evidence (quote the claim)
☐ Undefined quantifiers like "many" or "often" (quote the claim)
``` 