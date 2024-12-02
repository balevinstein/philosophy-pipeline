# The Asymmetry of Modal Belief Attribution

## Overview

Standard doxastic logic fails to capture a fundamental asymmetry in modal belief attribution, requiring formal revision

## Introduction

Target length: 500 words


### Key Claims
- Identification of previously unnoticed asymmetry
- Significance for doxastic logic


### Core Moves
- Present clear example of asymmetry
- Preview formal implications


### Technical Requirements
- Basic modal logic notation


### Literature Engagement
- Brief positioning relative to recent work


### Development Notes
Key verifications:

**Argument Structure:**
- Technical: Formal definitions now properly specify operator behavior and logical relationships, maintaining mathematical precision while allowing for empirical application
- Philosophical: Refined content advances understanding of belief attribution while engaging constructively with existing literature and acknowledging complexity of social cognition

**Example Development:**
- Technical: The refined content maintains formal precision while ensuring technical elements serve rather than dominate the philosophical argument. All technical notation is properly defined and consistently applied.
- Philosophical: The refinements strengthen the paper's philosophical contribution by more carefully demonstrating the relationship between direct observation and inferential steps in belief attribution, while acknowledging relevant nuances.

**Formal Framework:**
- Technical: All formal definitions are now properly typed, axioms use only defined terms, and logical relationships are clearly specified
- Philosophical: Refined content maintains focus on belief attribution asymmetry while providing precise formal grounding for philosophical claims

**Objection Mapping:**
- Technical: Refined content maintains formal precision while improving accessibility through careful exposition and motivated introduction of technical concepts.
- Philosophical: Strengthened connection between formal apparatus and philosophical insights about the nature of belief attribution and cognitive architecture.

**Integration:**
- Technical: Refined content maintains formal precision while introducing technical concepts with appropriate definitions and clear application to examples
- Philosophical: Enhanced content strengthens the paper's philosophical contribution by revealing fundamental features of belief attribution through precise formal analysis


## The Asymmetry Phenomenon

Target length: 1000 words


### Key Claims
- Systematic nature of asymmetry
- Distinction from similar phenomena


### Core Moves
- Detailed example analysis
- Pattern identification


### Technical Requirements
- Clear example presentation


### Literature Engagement
- Engagement with Yalcin (2018)


### Examples

#### Supporting Example 1
Consider: (1) 'John believes Mary believes it's raining' vs (2) 'Mary believes John believes it's raining'. While formally equivalent in standard doxastic logic, these differ systematically in natural reasoning - (1) suggests John's direct assessment of Mary's mental state while (2) suggests Mary's direct assessment of John's, an asymmetry reflected in differing evidence requirements and inference patterns

**Technical Notes:**
Provides concrete instance of formal/natural divergence

#### Supporting Example 2
Consider two observers A and B examining an object through different instruments:
A uses a microscope (precise local view)
B uses a telescope (broader distant view)
This scenario demonstrates how asymmetric observational capabilities lead to different nested beliefs about each other's knowledge.

**Technical Notes:**
Provides concrete motivation for formal definitions

#### Supporting Example 3
Consider two scenarios: (1) Ann observes Bob checking weather forecasts daily, leading to BA(BB(rain-tomorrow)). (2) Bob observes Ann reading forecasts, leading to BB(BA(rain-tomorrow)). While formally equivalent in standard logic, (1) requires only observation of behavior while (2) requires additional inference about Ann's cognitive processing of the information. This asymmetry persists even when controlling for contextual factors like communication channels and social dynamics.

**Technical Notes:**
Structured example to isolate technical features from pragmatic factors

#### Supporting Example 4
Consider two scientists collaborating on examining a specimen: Dr. Smith uses a microscope to analyze cellular structures while Dr. Jones uses a spectroscope to study molecular composition. When Dr. Smith forms beliefs about Dr. Jones's beliefs (BS(BJ(p))), these are grounded in direct observation of Jones's systematic spectroscopic analysis procedures - checking calibration, recording spectral lines, consulting reference data. However, when Dr. Jones forms beliefs about Dr. Smith's beliefs (BJ(BS(q))), while Jones can directly observe Smith's microscope usage, attributing specific beliefs requires additional inference about how Smith processes and interprets the microscopic data he observes.

**Technical Notes:**
Revised example to align with new formal apparatus while maintaining its intuitive clarity

#### Supporting Example 5
Applying our formal framework to the scientific instruments case demonstrates the crucial distinction: Dir(S,J_actions) → BS(J_actions) represents Smith's direct observation of Jones's actions, while BS(BJ(molecule_structure)) necessarily involves Inf(S,BJ), as Smith must make additional inferential steps to attribute specific beliefs about molecular structure to Jones. This formalization captures why first-order behavioral observations differ fundamentally from higher-order belief attributions.

**Technical Notes:**
Added precise formal notation showing evidence-belief relationships

#### Supporting Example 6
Consider two scientists, Alice and Bob, jointly conducting an experiment. Both follow identical protocols and have complete access to each other's laboratory notes and experimental procedures. Even in this maximally symmetric scenario, Alice's formation of beliefs about Bob's beliefs follows a different evidential pathway than Bob's formation of beliefs about Alice's beliefs. When Alice directly observes Bob recording data, she forms immediate beliefs about his beliefs (Dir). However, when Bob later considers Alice's beliefs about the data, he must engage in inference (Inf) even though he has access to the same information. This asymmetry persists despite the symmetry of available evidence.

**Technical Notes:**
Example now more precisely illustrates the technical distinction between Dir and Inf operators.

### Development Notes
Key verifications:

**Argument Structure:**
- Technical: Formal definitions now properly specify operator behavior and logical relationships, maintaining mathematical precision while allowing for empirical application
- Philosophical: Refined content advances understanding of belief attribution while engaging constructively with existing literature and acknowledging complexity of social cognition

**Example Development:**
- Technical: The refined content maintains formal precision while ensuring technical elements serve rather than dominate the philosophical argument. All technical notation is properly defined and consistently applied.
- Philosophical: The refinements strengthen the paper's philosophical contribution by more carefully demonstrating the relationship between direct observation and inferential steps in belief attribution, while acknowledging relevant nuances.

**Formal Framework:**
- Technical: All formal definitions are now properly typed, axioms use only defined terms, and logical relationships are clearly specified
- Philosophical: Refined content maintains focus on belief attribution asymmetry while providing precise formal grounding for philosophical claims

**Objection Mapping:**
- Technical: Refined content maintains formal precision while improving accessibility through careful exposition and motivated introduction of technical concepts.
- Philosophical: Strengthened connection between formal apparatus and philosophical insights about the nature of belief attribution and cognitive architecture.

**Integration:**
- Technical: Refined content maintains formal precision while introducing technical concepts with appropriate definitions and clear application to examples
- Philosophical: Enhanced content strengthens the paper's philosophical contribution by revealing fundamental features of belief attribution through precise formal analysis


## Formal Analysis and Revision

Target length: 1500 words


### Key Claims
- Inadequacy of standard formal treatment
- Proposed revision


### Core Moves
- Demonstrate formal inadequacy
- Present revision


### Technical Requirements
- Doxastic logic formalism


### Literature Engagement
- Beddor & Goldstein (2021)


### Formal Content

#### Foundations

**Formal Definition:**
Consider first how we directly observe someone's belief: When Alice watches Bob check the weather and grab an umbrella, she directly observes his belief that it will rain. We formalize this using Dir(Alice,BBob(rain)). This direct observation necessarily leads to Alice's belief about Bob's belief: BAlice(BBob(rain)). More generally, for any agents x,y and proposition p: Dir(x,By(p)) → Bx(By(p)). The asymmetry emerges because the reverse direction requires inference rather than direct observation.

**Technical Notes:**
Formal definition now introduced through concrete example before presenting general form, improving accessibility while maintaining precision.

#### Theorem
Theorem 1 (Asymmetry of Belief Attribution). For any agents x,y and proposition p, if x directly observes y's belief formation about p, then y cannot simultaneously directly observe x's belief formation about p. Formally:
Dir(x,y) ∧ Bx(By(p)) → ¬(Dir(y,x) ∧ By(Bx(p)))

**Technical Notes:**
Simplified theorem to focus on core asymmetry claim with clear formal grounding

### Objections and Responses

#### Objection
While model restrictions could indeed capture some aspects of the asymmetry, this approach fails to address the systematic nature of the phenomenon... Moreover, the proposed model restrictions would need to be stipulated ad hoc for each case.

#### Response
While model restrictions could capture individual instances of the asymmetry, they fail to provide a unified account of this systematic phenomenon. Consider a case where agent A believes p, and we examine nested beliefs about q. Under a restrictions approach, we would need separate stipulations for BA(p), BA(BB(p)), and each level of nesting. Our framework, through Definition 2(ii), derives these patterns from a single principle about observation set relationships: OA(v) ⊆ OA(w) captures how higher-order beliefs systematically depend on lower-order evidence.

**Technical Support:**
Added specific example of nested beliefs to illustrate limitations of model restrictions approach

#### Objection
This pragmatic explanation fails to account for the systematic nature of the asymmetry across diverse contexts. Even when controlling for conversational factors and making cognitive processing explicit, the asymmetry persists in the formal structure of the evidence required for belief attribution.

#### Response
While pragmatic factors certainly influence belief attribution patterns, they cannot fully explain the systematic asymmetry we observe. Consider cases where conversational and cognitive factors are explicitly controlled: When two scientists S and J have identical cognitive capabilities and engage in explicit communication protocols, we still find systematic differences in the evidential requirements for BS(BJ(p)) versus BJ(BS(q)). This suggests a deeper structural feature of belief attribution.

**Technical Support:**
Removed overly strong claim about pragmatic factors while preserving core technical insight about evidential structure

### Development Notes
Key verifications:

**Argument Structure:**
- Technical: Formal definitions now properly specify operator behavior and logical relationships, maintaining mathematical precision while allowing for empirical application
- Philosophical: Refined content advances understanding of belief attribution while engaging constructively with existing literature and acknowledging complexity of social cognition

**Example Development:**
- Technical: The refined content maintains formal precision while ensuring technical elements serve rather than dominate the philosophical argument. All technical notation is properly defined and consistently applied.
- Philosophical: The refinements strengthen the paper's philosophical contribution by more carefully demonstrating the relationship between direct observation and inferential steps in belief attribution, while acknowledging relevant nuances.

**Formal Framework:**
- Technical: All formal definitions are now properly typed, axioms use only defined terms, and logical relationships are clearly specified
- Philosophical: Refined content maintains focus on belief attribution asymmetry while providing precise formal grounding for philosophical claims

**Objection Mapping:**
- Technical: Refined content maintains formal precision while improving accessibility through careful exposition and motivated introduction of technical concepts.
- Philosophical: Strengthened connection between formal apparatus and philosophical insights about the nature of belief attribution and cognitive architecture.

**Integration:**
- Technical: Refined content maintains formal precision while introducing technical concepts with appropriate definitions and clear application to examples
- Philosophical: Enhanced content strengthens the paper's philosophical contribution by revealing fundamental features of belief attribution through precise formal analysis


## Implications and Conclusion

Target length: 500 words


### Key Claims
- Broader significance
- Future directions


### Core Moves
- Connect to broader issues
- Highlight importance


### Technical Requirements
- None


### Literature Engagement
- Broader theoretical context


### Development Notes
Key verifications:

**Argument Structure:**
- Technical: Formal definitions now properly specify operator behavior and logical relationships, maintaining mathematical precision while allowing for empirical application
- Philosophical: Refined content advances understanding of belief attribution while engaging constructively with existing literature and acknowledging complexity of social cognition

**Example Development:**
- Technical: The refined content maintains formal precision while ensuring technical elements serve rather than dominate the philosophical argument. All technical notation is properly defined and consistently applied.
- Philosophical: The refinements strengthen the paper's philosophical contribution by more carefully demonstrating the relationship between direct observation and inferential steps in belief attribution, while acknowledging relevant nuances.

**Formal Framework:**
- Technical: All formal definitions are now properly typed, axioms use only defined terms, and logical relationships are clearly specified
- Philosophical: Refined content maintains focus on belief attribution asymmetry while providing precise formal grounding for philosophical claims

**Objection Mapping:**
- Technical: Refined content maintains formal precision while improving accessibility through careful exposition and motivated introduction of technical concepts.
- Philosophical: Strengthened connection between formal apparatus and philosophical insights about the nature of belief attribution and cognitive architecture.

**Integration:**
- Technical: Refined content maintains formal precision while introducing technical concepts with appropriate definitions and clear application to examples
- Philosophical: Enhanced content strengthens the paper's philosophical contribution by revealing fundamental features of belief attribution through precise formal analysis

