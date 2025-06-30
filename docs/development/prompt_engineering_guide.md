# Philosophy Pipeline Prompt Engineering Guide

This guide explains the overall prompt engineering strategy for the Philosophy Pipeline without duplicating the actual prompts (which are the source of truth in the code).

## 🎯 Core Prompt Engineering Philosophy

### **Single Source of Truth**
- **Actual prompts** in `src/phases/*/prompts/*.py` are the authoritative source
- **This guide** explains the strategy and patterns, not the implementation
- **No dual maintenance** - prompts evolve, this guide explains principles

### **Journal-Specific Optimization**
- All prompts optimized for **Analysis journal** style and standards
- **Conversational rigor**: Professional but accessible philosophical writing
- **Example-driven argumentation**: Concrete cases doing real argumentative work
- **Systematic development**: Progressive refinement, not dramatic turns

## 🏗️ Prompt Architecture Patterns

### **1. Structured Prompt Format**
All prompts follow consistent structure:
```
<context>         # Pipeline context and role
<task>            # Specific task description  
<requirements>    # Output format and constraints
<guidance>        # Domain-specific instructions
<examples>        # Concrete examples when helpful
<output_format>   # JSON schema or format specs
```

**Why this works:**
- **Clear separation** of concerns
- **Easy to debug** specific prompt sections
- **Consistent experience** across all pipeline phases
- **Maintainable** - sections can be updated independently

### **2. Multi-Stage Prompt Design**
Complex phases use **multiple specialized prompts**:
- **Development prompt**: Creates initial content
- **Critic prompt**: Identifies weaknesses and issues
- **Revision prompt**: Implements improvements

**Example: Phase III.1 (Section Writing)**
- `construct_writing_prompt()`: Creates section content
- `construct_critic_prompt()`: Brutally honest critique
- `construct_revision_prompt()`: Integrates improvements

**Benefits:**
- **Cognitive load distribution**: Each prompt has focused responsibility
- **Higher quality**: Specialized prompts > single complex prompt
- **Easier debugging**: Can test each stage independently

### **3. Anti-RLHF Patterns**
Critical feature: **Philosophical boldness over safe hedging**

**Problem**: LLM training promotes:
- "Some philosophers argue..." instead of taking positions
- "On the other hand..." hedging for every claim
- Wishy-washy compromise conclusions

**Solution**: Explicit anti-RLHF instructions:
```
# TAKE A STAND (RLHF-Proofing)
- Write "I argue that X" not "One might consider whether X"
- Say "This objection fails because..." not "This objection faces challenges"
- State controversial implications clearly, don't bury them
```

**Implementation**: Included in prompts for Phases II.2-III.2

## 🎨 Content Integration Strategies

### **1. Philosophical Moves Database**
- **Location**: `data/philosophical_moves/injectable_examples.json`
- **Usage**: Phase II.7 injects curated moves into development
- **Content**: 143 examples across 5 categories (abstract_development, key_moves_development, etc.)

**Prompt Strategy:**
- Load examples dynamically based on phase needs
- Provide as `<content_bank>` in prompts
- Let LLM select relevant patterns contextually

### **2. Analysis Journal Integration**
- **PDF Integration**: Random selection of Analysis papers as style exemplars
- **Style Guides**: Embedded Analysis writing patterns in prompts
- **Pattern Recognition**: Systematic analysis of Analysis conventions

**Implementation Pattern:**
```python
def _select_analysis_exemplars(self) -> str:
    # Randomly select 2 Analysis PDFs
    # Include in prompt as style reference
    # Introduces valuable entropy while maintaining quality
```

### **3. Context Chaining**
Complex phases maintain context across multiple API calls:
- **Writing Context**: Phase II.8 → Phase III.1
- **Revision Context**: Critic output → Revision implementation
- **Integration Context**: All prior phases → Final paper

**Prompt Design:**
- Clear context sections explaining pipeline position
- Comprehensive information packaging
- Explicit transition guidance

## 🛠️ Implementation Patterns

### **1. Prompt Class Structure**
Each phase has a dedicated prompt class:
```python
class PhasePrompts:
    def __init__(self):
        self.system_prompt = "..."
        self.context = "..."
        self.requirements = "..."
    
    def construct_[purpose]_prompt(self, context: Dict) -> str:
        # Dynamic prompt construction
```

**Benefits:**
- **Organized**: Related prompts grouped logically
- **Reusable**: Common elements defined once
- **Configurable**: Dynamic construction based on context

### **2. JSON Output Standardization**
All prompts specify JSON output format:
- **Consistent parsing** across pipeline
- **Structured data** for next phases
- **Error handling** for malformed responses

**Pattern:**
```json
{
    "primary_content": "Main output",
    "metadata": {"word_count": 1234},
    "analysis": "Quality assessment",
    "transitions": {"to_next": "Connection guidance"}
}
```

### **3. Quality Control Integration**
Prompts embed quality standards:
- **Hájek Heuristics**: Extreme cases, self-undermining, counterexamples
- **Analysis Patterns**: Conversational rigor, example-driven arguments
- **Philosophical Rigor**: Systematic objection handling, precision

**Implementation**: Quality standards embedded in `<guidance>` sections

## 🔍 Debugging and Optimization

### **1. Prompt Testing Strategy**
- **Individual prompts**: Test each prompt class method independently
- **Chain testing**: Verify prompt sequences work together
- **Quality validation**: Check output meets standards

### **2. Common Prompt Issues**
- **JSON parsing errors**: Ensure proper escaping in output format
- **Context overflow**: Monitor token usage with long contexts
- **Quality degradation**: Test for RLHF-induced hedging

### **3. Optimization Approaches**
- **Token efficiency**: Use TXT extracts instead of PDFs when possible
- **Cognitive load**: Split complex tasks into multiple prompts
- **Performance tracking**: Monitor API call duration and quality

## 📊 Phase-Specific Strategies

### **Phase II.1-4 (Development)**
- **Literature integration**: PDF processing with Claude
- **Framework building**: Systematic argument development
- **Iterative refinement**: Multi-round development cycles

### **Phase II.5-8 (Quality Control)**
- **Diagnostic analysis**: Comprehensive quality assessment
- **Expert review**: Philosophical referee simulation
- **Targeted improvements**: Specific revision strategies

### **Phase III.1-2 (Writing)**
- **Section-by-section**: Focused content generation
- **Analysis style**: Journal-specific writing patterns
- **Global integration**: Publication-ready formatting

## 🎯 Success Metrics

### **Quality Indicators**
- **Philosophical rigor**: Arguments survive Hájek heuristics
- **Analysis style**: Conversational but rigorous tone
- **Coherence**: Sections integrate smoothly
- **Precision**: Technical concepts clearly defined

### **Performance Metrics**
- **Token efficiency**: ~3x improvement with TXT extracts
- **Quality consistency**: Reliable output across runs
- **Error rates**: Low JSON parsing failures
- **Processing time**: Reasonable API call duration

## 🔄 Evolution and Maintenance

### **Prompt Improvement Process**
1. **Identify issues**: Track quality problems or errors
2. **Isolate causes**: Determine if prompt or model issue
3. **Test improvements**: Validate changes before deployment
4. **Document changes**: Update this guide if strategy changes

### **Best Practices**
- **Iterative improvement**: Small, testable changes
- **Quality validation**: Always test against standards
- **Documentation**: Keep this guide updated with major strategy changes
- **Collaboration**: Clear patterns for team prompt engineering

## 📚 Key Files Reference

### **Main Prompt Files**
- `src/phases/phase_two/stages/*/prompts/`: Development phase prompts
- `src/phases/phase_three/stages/*/prompts/`: Writing phase prompts  
- `src/utils/prompt_utils.py`: Shared prompt utilities

### **Supporting Data**
- `data/philosophical_moves/injectable_examples.json`: Curated philosophical patterns
- `data/style_guides/analysis_style_guide.md`: Analysis writing conventions
- `config/conceptual_config.yaml`: Prompt configuration settings

### **Quality Standards**
- Analysis journal patterns embedded in prompts
- Hájek heuristics integrated in quality control phases
- Anti-RLHF patterns throughout writing phases

This guide explains the **why** and **how** of prompt engineering without duplicating the **what** (which lives in the code). 