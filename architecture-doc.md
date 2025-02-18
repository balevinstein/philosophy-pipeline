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

   - II.3: Key Moves Development [IN PROGRESS]

     - Full development of each move
     - Local worker/critic refinement cycles
     - Global coherence validation
     - Literature integration

   - II.4: Detailed Outline Development

     - Full structural expansion
     - Move integration
     - Section/subsection planning
     - Transition development

   - II.5: Integration and Smoothing [OPTIONAL]
     - Final alignment check
     - Gap identification
     - Last feasibility validation

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

### II.4: Detailed Outline Development

Takes the fully developed key moves from II.3 and creates a comprehensive outline that will guide Phase III writing.

#### Core Objectives

- Integrate developed moves into detailed structure
- Plan full section/subsection development
- Establish clear transitions and flow
- Maintain feasible scope

#### Worker Architecture

[Similar local/global pattern but focused on structural development]

#### Development Flow

1. Initial structural expansion
2. Move integration
3. Transition development
4. Feasibility validation

#### Success Criteria

- Clear development path for each section
- Proper space for move deployment
- Feasible within word constraints
- Ready for Phase III writing

### II.5: Integration and Smoothing [Optional]

This stage may be used if needed to handle any remaining integration issues after II.4.

#### Potential Objectives

- Final framework alignment check
- Move-structure integration issues
- Literature coverage gaps
- Last feasibility validation

This stage might prove unnecessary if II.3 and II.4 achieve sufficient development quality.

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
   - Base worker/critic/refinement infrastructure
   - PDF handling and literature integration
   - Test infrastructure and validation

2. **In Progress**

   - II.3 design and implementation
   - Key moves development system
   - Local/global worker coordination
   - Refinement cycle management

3. **Next Steps**

   - II.3 implementation completion
   - II.4 detailed outline development
   - Potential II.5 planning if needed
   - Phase III preparation

4. **Future Enhancements**
   - Phase I restructuring
   - Enhanced literature integration
   - Vector database implementation
   - Quality improvements
