# Phase II Architecture: Analysis Paper Development System

## Overview

This document describes the architecture for Phase II of the AI-driven philosophy paper generation system. Phase II takes output from Phase I (selected topic, literature requirements) and produces a detailed outline ready for Phase III (paper writing).

## Core Design Principles

1. **Intelligent Worker Management**: Leverage LLM capabilities while managing cognitive load through clear task boundaries
2. **Hierarchical Quality Control**: Local development with global oversight to maintain coherence and prevent drift
3. **Flexible Development**: Handle diverse philosophical content while maintaining systematic approach
4. **Literature Integration**: Strategic use of available sources with future enhancement path
5. **Managed Complexity**: Clear development cycles with appropriate validation stages
6. **Pragmatic Goals**: Target ~20% publication success rate through systematic development
7. **Forward Compatibility**: Design for future enhancements while maintaining MVP functionality

## Stage Architecture

### Stages Overview

1. **Phase I: Topic Generation, Selection, Literature Retrieval** [Current Implementation]

   - I.1: Topic Generations and Selection [COMPLETED]

     - Generate potential topics
     - Evaluate and select promising candidates
     - Will be restructured to match Phase II architecture in future updates

   - I.2: Literature Retrieval [IN_PROGRESS]

     - Generate potential queries to the engaging topics
     - Use search API to get relevant papers
     - User downloads pdfs for relevant searches and provides it for next step

2. **Phase II: Framework and Content Development**

   - II.1: Literature Processing & Understanding [COMPLETED]

     - Process source PDFs
     - Create structured analysis
     - Map engagement points
     - Synthesize findings

   - II.2: Framework Development [COMPLETED]

     - Abstract development with validation
     - High-level outline creation
     - Key moves identification
     - Literature engagement mapping

   - II.3: Key Moves Development [COMPLETED]

     - Full development of each move
     - Local worker/critic refinement cycles
     - Global coherence validation
     - Literature integration

   - II.4: Detailed Outline Development [COMPLETED]

     - Full structural expansion
     - Move integration
     - Section/subsection planning
     - Transition development
     - Output: `outputs/detailed_outline/detailed_outline_final.json`

   - II.5: Content Integration and Enhancement [IN_PROGRESS]
     - Input: `outputs/detailed_outline/detailed_outline_final.json` and all previous phase outputs
     - Detailed argument structure development
     - Specific literature citation integration
     - Concrete examples and thought experiments
     - Enhanced transitions and connections
     - Output: `outputs/detailed_integration/enhanced_outline_final.json`

3. **Phase III: Paper Writing**

   - III.1: Section Development

     - Section-by-section writing
     - Local refinement cycles
     - Content integration

   - III.2: Global Review and Finalization
     - Full paper review
     - Final refinements
     - Quality validation

### Worker System

The pipeline uses an actor/critic/refinement pattern:

1. Worker develops content
2. Critic evaluates
3. Refinement worker implements improvements
4. Cycles repeat until satisfactory

Key principles:

- Clear task boundaries
- Managed cognitive load
- Framework alignment
- Quality validation
- Drift prevention

### II.3: Key Moves Development

This stage takes the blueprint from II.2 and fully develops each key argumentative
move while maintaining theoretical coherence and practical feasibility.

#### Core Objectives

- Develop key moves to near-final form
- Ensure arguments are logically sound
- Integrate examples and literature effectively
- Maintain alignment with framework
- Prevent conceptual drift

#### Worker Architecture

1. LocalMoveWorker

- Purpose: Develop individual key moves to full form
- Input: Single key move + full paper context (framework, outline, literature)
- Process:
  - Core argument development
  - Example integration
  - Literature connection
  - Feasibility assessment
- Output: Fully developed move with supporting elements

2. LocalCritic

- Purpose: Evaluate individual move development
- Focus areas:
  - Argument validity
  - Example effectiveness
  - Literature integration
  - Local coherence
  - Development completeness
- Output: Specific recommendations for improvement

3. LocalRefinementWorker

- Purpose: Implement critic recommendations
- Process:
  - Evaluate suggested changes
  - Maintain move integrity
  - Implement accepted improvements
- Output: Refined move development

4. GlobalCritic

- Purpose: Evaluate collective move development
- Focus areas:
  - Framework alignment
  - Inter-move coherence
  - Overall feasibility
  - Literature coverage
- Output: High-level recommendations

#### Development Flow

1. Initial Move Development

   - LocalMoveWorker processes each move
   - LocalCritic evaluates
   - LocalRefinement implements changes
   - Repeat until satisfactory

2. Global Review
   - GlobalCritic evaluates full set
   - LocalMoveWorker addresses issues
   - Repeat cycle if needed

#### Success Criteria

- Arguments fully developed with clear structure
- Examples effectively integrated
- Literature properly deployed
- Maintains framework alignment
- Feasible within space constraints
- Ready for outline integration

#### Quality Control

- Regular validation against framework
- Explicit tracking of changes
- Clear criteria for move completion
- Coherence checking between moves

This stage prioritizes getting core content right while maintaining manageable complexity and allowing for iteration where needed.

#### Move Type Handling

The LocalMoveWorker needs to handle diverse philosophical moves while maintaining development quality. Rather than assuming specific move types, the worker follows key principles:

Core Development Principles:

- Identify the move's fundamental argumentative goal
- Determine appropriate support needs (examples, cases, formal arguments)
- Establish clear success criteria based on move's purpose
- Select appropriate development strategy
- Maintain theoretical rigor while ensuring practical feasibility

The worker maintains flexibility through:

- Context-sensitive development approach
- Clear argument structure requirements
- Appropriate evidence selection
- Strategic literature deployment
- Regular validation against move's purpose

This approach allows handling both common move types (taxonomies, spectrums, methodologies) and novel argumentative strategies while ensuring development quality.

#### Worker Intelligence Management

The system leverages the workers' general intelligence and philosophical judgment while managing cognitive load:

Leveraging Capabilities:

- Natural understanding of argument types
- Ability to judge support needs
- Philosophical writing expertise
- Literature integration skills
- Quality assessment capacity

Managing Load:

- One move at a time
- Clear task boundaries
- Essential context only
- Explicit success criteria
- Structured review cycles

This approach allows workers to use their full capabilities while maintaining:

- Focus on specific tasks
- Framework alignment
- Development quality
- Systematic progress

### II.4: Detailed Outline Development [COMPLETED]

Takes the fully developed key moves from II.3 and creates a comprehensive structural outline that will guide Phase III writing.

#### Core Objectives

- Integrate developed moves into detailed structure
- Plan full section/subsection development
- Establish clear transitions and flow
- Maintain feasible scope

#### Worker Architecture

1. Framework Integration Worker
   - Creates the foundational structural skeleton
   - Allocates section/subsection organization
   - Assigns word counts to sections

2. Literature Mapping Worker
   - Maps literature sources to specific sections
   - Identifies primary/supporting source relationships
   - Plans literature engagement strategy

3. Content Development Worker
   - Creates generalized content guidance
   - Develops structural bullet points
   - Establishes content flow

4. Structural Validation Worker
   - Validates overall structure coherence
   - Ensures logical progression
   - Verifies key move integration

#### Success Criteria

- Comprehensive section/subsection structure
- Proper word count allocation
- Basic content guidance
- Logical structural flow
- Key move integration into structure

#### Output Files

- `outputs/detailed_outline/detailed_outline_final.md`: Human-readable outline
- `outputs/detailed_outline/detailed_outline_final.json`: Machine-readable structured outline containing:
  - Complete outline text
  - Thesis statement
  - Core contribution
  - Key moves
  - Metadata

### II.5: Content Integration and Enhancement [IN_PROGRESS]

This stage takes the structural outline from II.4 and enhances it with specific content details necessary for effective Phase III writing.

#### Core Objectives

- Transform structural outline into detailed content blueprint
- Integrate specific literature citations with quotes and page numbers
- Develop explicit argument structures with clear premises and conclusions
- Create concrete examples and thought experiments
- Provide detailed methodological guidance
- Ensure comprehensive integration of previous phases' outputs

#### Input Files

- `outputs/detailed_outline/detailed_outline_final.json`: Primary structural outline
- `outputs/framework_development/abstract_framework.json`: Core thesis and contribution
- `outputs/key_moves_development/key_moves_development/all_developed_moves.json`: Fully developed moves
- `outputs/literature_synthesis.json`: Literature analysis and engagement points

#### Development Focus

1. Argument Enhancement
   - Explicit premise-conclusion structures
   - Formal argument patterns where appropriate
   - Clear inferential connections
   - Detailed objection-response pairs

2. Literature Integration
   - Specific citations with page numbers
   - Key quotes for inclusion
   - Explicit connections to framework
   - Scholar position mapping

3. Example Development
   - Concrete thought experiments
   - Real-world applications
   - Detailed case analyses
   - Illustrative scenarios

4. Methodological Specification
   - Explicit philosophical methodology
   - Analytical approach details
   - Assessment criteria
   - Evaluation frameworks

#### Expected Output

- `outputs/detailed_integration/enhanced_outline_final.json`: Comprehensive content blueprint containing:
  - Detailed arguments with premises and conclusions
  - Specific literature citations and quotes
  - Fully developed examples and thought experiments
  - Comprehensive section content guidance
  - Detailed transition plans

#### Success Criteria

- Provides specific content that Phase III writers can directly incorporate
- Offers detailed arguments that maintain logical validity
- Includes concrete examples that illustrate key points
- Features specific literature engagement with exact citations
- Maintains alignment with framework while adding substantial detail
- Enables Phase III writers to focus on expression rather than content creation

This stage fills the gap between the structural outline of II.4 and the writing needs of Phase III, ensuring writers have specific content to include rather than just structural guidance.

### Actor/Critic Methodology

- Development/critique cycles at both local and global levels
- Framework-based oversight across stages
- Critic types:
  - Local critics (move-specific evaluation)
  - Global critics (coherence and alignment)
  - Refinement validation
- Configurable iteration counts through config

## Worker System

### Base Infrastructure

- Abstract base class (PhaseIIWorker)
- Dynamic registration system
- Standardized input/output handling
- State management support

### Worker Types

1. **Development Workers**

   - LocalMoveWorker (develops individual moves)
   - OutlineWorker (structure development)
   - RefinementWorker (implements improvements)
   - GlobalWorker (maintains coherence)

2. **Critics**

   - LocalCritic (evaluates specific content)
   - GlobalCritic (checks overall alignment)
   - FeasibilityCritic (validates scope)

3. **Oversight Workers**
   - CoherenceKeeper (framework alignment)
   - QualityController (validates development)
   - StateManager (tracks progress)

## Data Management

### Storage Formats

1. **Core Development Files**

   - JSON for structured data (framework, analysis, metadata)
   - Markdown for readable content (critiques, refinements)
   - PDFs handled through Claude's native support

2. **Development History**
   - Complete cycles stored for inspection
   - Final versions passed to next stage
   - Clear separation of working/final content

### Key Data Structures

1. **Framework Components**

- Abstract/thesis/contribution
- Version tracking
- Validation status
- Change history

2. **Key Moves Development**

- Core argument structure
- Supporting elements
- Literature connections
- Development status
- Validation metrics

3. **Outline Structure**

- Section/subsection hierarchy
- Move integration points
- Development status
- Word count allocation

### Data Flow

1. **Between Stages**

- Clear input/output specifications
- Minimal necessary context
- Clean final versions

2. **Within Stage Cycles**

- Development versions
- Critique feedback
- Refinement tracking
- Progress metrics

3. **Inspection vs Forward Flow**

- Complete history saved for debugging
- Clean outputs for next stage
- Clear separation of concerns

## Quality Control Systems

### Development Control

1. **Local Development**

- Single move/section focus
- Clear success criteria
- Explicit validation steps
- Progress tracking

2. **Global Oversight**

- Framework alignment checking
- Inter-move coherence
- Scope management
- Drift prevention

### Cognitive Load Management

1. **Task Boundaries**

- One primary focus per worker
- Essential context only
- Clear task definition
- Explicit success criteria

2. **Context Management**

- Relevant framework elements
- Required literature context
- Development history as needed
- Minimal overhead

### Drift Prevention

1. **Framework Alignment**

- Regular checking against abstract
- Core thesis maintenance
- Key move coherence
- Development path validation

2. **Quality Metrics**

- Argument strength
- Example effectiveness
- Literature integration
- Practical feasibility

### Failure Mode Prevention

1. **Development Risks**

- Scope creep monitoring
- Complexity management
- Dependency tracking
- Resource constraints

2. **Content Quality**

- Argument validity
- Support adequacy
- Framework alignment
- Literature engagement

3. **System Management**

- Worker coordination
- State tracking
- Error handling
- Progress monitoring

## Implementation Considerations

### MVP Requirements

1. **Essential Features**

- Worker/critic/refinement cycle system
- Framework development and tracking
- Key moves development
- Quality monitoring
- Basic literature integration

2. **Core Functionality**

- Argument development
- Example integration
- Structure creation
- Coherence maintenance

3. **Basic Infrastructure**

- File management
- State tracking
- Error handling
- Progress monitoring

### Future Enhancements

1. **Literature Integration**

- Enhanced source database
- Better citation coverage
- More sophisticated integration
- Vector database potential

2. **Quality Improvements**

- Specialized workers
- Enhanced validation
- More refined prompts
- Better coordination

3. **System Extensions**

- Phase I restructuring
- Enhanced monitoring
- Better state management
- More sophisticated error handling

### Success Criteria

1. **Paper Quality**

- Clear philosophical contribution
- Strong argumentation
- Appropriate scope
- ~20% publication ready

2. **System Performance**

- Reliable execution
- Clear development path
- Effective error handling
- Maintainable state

3. **Development Process**

- Modular components
- Clear interfaces
- Testable outputs
- Manageable complexity

## Project Organization

### Directory Structure

```
philosophy_pipeline/
├── papers/                          # PDF storage for literature
├── src/
│   ├── prompts/                     # Phase I prompts
│   ├── stages/
│   │   ├── conceptual_generate.py   # Current Phase I implementation
│   │   ├── conceptual_evaluate.py
│   │   ├── conceptual_topic_development.py
│   │   ├── conceptual_final_select.py
│   │   └── phase_two/              # Phase II implementation
│   │       ├── base/               # Core worker system
│   │       │   ├── worker.py
│   │       │   └── registry.py
│   │       └── stages/             # Stage implementations
│   │           ├── stage_one/      # Literature processing
│   │           ├── stage_two/      # Framework development
│   │           ├── stage_three/    # Key moves development
│   │           └── stage_four/     # Detailed outline
│   └── utils/                      # Utility functions
├── config/
│   └── conceptual_config.yaml
├── outputs/                        # Stage outputs
├── tests/                         # Test scripts
└── run_scripts/
    ├── run_phase_one.py
    ├── run_phase_two_one.py
    └── run_phase_two_two.py
```

### Configuration

- API settings for PDF processing
- Stage parameters
- Worker settings
- Quality thresholds
- Development cycles

## Current Status

1. **Completed**

   - II.1: Literature processing and synthesis
   - II.2: Framework development (abstract, outline, key moves)
   - II.3: Key moves development
   - Base worker/critic/refinement infrastructure
   - PDF handling and literature integration
   - Test infrastructure and validation

2. **In Progress**

   - II.4 design and implementation
   - Detailed outline development system
   - Local/global worker coordination
   - Refinement cycle management

3. **Next Steps**

   - II.4 implementation completion
   - Potential II.5 planning if needed
   - Phase III preparation

4. **Future Enhancements**
   - Phase I restructuring
   - Enhanced literature integration
   - Vector database implementation
   - Quality improvements
