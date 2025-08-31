# Philosophy Pipeline - Refactor Master Plan

## Overview

This document serves as the master coordination plan for refactoring the philosophy pipeline project. Multiple agents can work on different work packages simultaneously using this plan as the coordination framework.

**Project Goal**: Transform the philosophy pipeline from a collection of 13+ individual runner scripts into a unified, professional CLI tool with clean architecture and excellent developer experience.

**Timeline**: 2 weeks (10 working days)  
**Estimated Effort**: ~12-15 days total across multiple agents

---

## Work Package Architecture

### **Dependency Chain**
```
WP1 (Structure) → WP2 (CLI Core) → WP3 (Config) → WP4 (DevTools) → WP5 (Outputs) → WP6 (Performance) → WP7 (Docs)
     ↓              ↓                ↓              ↓               ↓              ↓              ↓
   Day 1-2        Day 2-4          Day 3-5        Day 5-7         Day 6-8        Day 8-9       Day 9-10
```

### **Parallel Work Opportunities**
- **WP1 + WP3**: Structure cleanup can happen parallel to config design
- **WP4 + WP5**: DevTools and Outputs can be developed simultaneously after CLI core
- **WP6 + WP7**: Performance and Documentation can overlap

---

## Work Package Definitions

### **WP1: Project Structure Cleanup**
**Owner**: Agent A  
**Duration**: 2 days  
**Priority**: CRITICAL (blocks all other work)

#### **Deliverables**
1. **Legacy Archive** (`LEGACY_MIGRATION.md`)
   - Move `legacy/` → `archive/legacy/`
   - Document what was archived and why
   - Remove all legacy imports from current code
   
2. **Root Directory Reorganization**
   ```
   scripts/
   ├── phases/           # All run_phase_*.py files
   ├── utils/            # extract_*.py, curate_*.py
   └── dev/             # Development scripts
   ```

3. **Import Path Updates**
   - Update all import statements to reflect new structure
   - Ensure no broken imports remain
   - Update any hardcoded paths in scripts

#### **Success Criteria**
- [ ] All legacy code moved to archive
- [ ] No import errors when running current pipeline
- [ ] Clean root directory with logical organization
- [ ] LEGACY_MIGRATION.md documents all changes

#### **Output Artifacts**
- Reorganized directory structure
- `LEGACY_MIGRATION.md`
- Updated import statements across codebase

---

### **WP2: Unified CLI Core**
**Owner**: Agent B  
**Duration**: 3 days  
**Priority**: CRITICAL  
**Dependencies**: WP1 (structure cleanup)

#### **Deliverables**

1. **Main CLI Interface** (`pipeline_cli.py`)
   ```python
   # Core Commands
   python pipeline_cli.py run --full
   python pipeline_cli.py run --phase 1.1
   python pipeline_cli.py run --phase 2.1-2.4
   python pipeline_cli.py status
   python pipeline_cli.py config --validate
   ```

2. **Pipeline Runner Architecture** (`src/pipeline/`)
   ```
   src/pipeline/
   ├── __init__.py
   ├── runner.py           # PipelineRunner class
   ├── phase_registry.py   # Phase discovery and registration
   ├── execution_context.py # State and validation
   └── cli_handlers.py     # Command handlers
   ```

3. **Phase Registration System**
   - Automatic discovery of phase modules
   - Dependency validation between phases
   - Phase metadata management (duration, requirements, outputs)

#### **Technical Specifications**

**PipelineRunner Class**:
```python
class PipelineRunner:
    def __init__(self, config_path: str = None):
        pass
    
    def run_phase(self, phase_id: str, dev_mode: bool = False) -> bool:
        pass
    
    def run_phases(self, phase_range: str, dev_mode: bool = False) -> bool:
        pass
    
    def run_full_pipeline(self, dev_mode: bool = False) -> bool:
        pass
```

**PhaseRegistry Class**:
```python
class PhaseRegistry:
    def discover_phases(self) -> Dict[str, PhaseMetadata]:
        pass
    
    def validate_dependencies(self, phase_sequence: List[str]) -> bool:
        pass
    
    def get_phase_module(self, phase_id: str) -> Any:
        pass
```

#### **Success Criteria**
- [ ] Single CLI entry point works for all current phases
- [ ] Backward compatibility: all existing run_phase_*.py scripts work via CLI
- [ ] Clean error handling and user feedback
- [ ] Phase dependency validation works
- [ ] Help text and usage examples are clear

#### **Output Artifacts**
- `pipeline_cli.py` (main entry point)
- `src/pipeline/` module with core classes
- Updated documentation for CLI usage

---

### **WP3: Configuration Consolidation**
**Owner**: Agent C  
**Duration**: 2 days  
**Priority**: HIGH  
**Dependencies**: WP1 (can start parallel), WP2 (for integration)

#### **Deliverables**

1. **Unified Configuration Structure**
   ```
   config/
   ├── base.yaml              # Core configuration
   ├── environments/
   │   ├── development.yaml   # Dev overrides
   │   └── production.yaml    # Production settings
   ├── schema.yaml           # Validation schema
   └── README.md             # Configuration documentation
   ```

2. **Configuration Management System** (`src/config/`)
   ```
   src/config/
   ├── __init__.py
   ├── manager.py        # ConfigManager class
   ├── validator.py      # Schema validation
   └── loader.py         # Environment-aware loading
   ```

3. **Environment Management**
   - `.env.template` with all required variables
   - Environment validation on startup
   - Clear documentation of all configuration options

#### **Technical Specifications**

**ConfigManager Class**:
```python
class ConfigManager:
    def __init__(self, environment: str = "development"):
        pass
    
    def load_config(self) -> Dict[str, Any]:
        pass
    
    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        pass
    
    def get_model_config(self, stage_name: str) -> Dict[str, Any]:
        pass
```

**Migration Strategy**:
- Merge `config/conceptual_config.yaml` with scattered hardcoded configs
- Extract all hardcoded configurations from phase scripts
- Create environment-specific overrides for dev/prod

#### **Success Criteria**
- [ ] Single source of truth for all configuration
- [ ] Environment-specific configuration works
- [ ] Configuration validation prevents invalid settings
- [ ] All phases use unified configuration system
- [ ] Clear documentation for all configuration options

#### **Output Artifacts**
- Unified configuration files in `config/`
- `src/config/` management module
- `.env.template` and configuration documentation

---

### **WP4: Developer Experience Tools**
**Owner**: Agent D  
**Duration**: 2 days  
**Priority**: HIGH  
**Dependencies**: WP2 (CLI core), WP3 (configuration)

#### **Deliverables**

1. **Development Mode Features**
   ```bash
   # Enhanced development commands
   python pipeline_cli.py run --phase 2.3 --dev --verbose
   python pipeline_cli.py validate --phase 2.1
   python pipeline_cli.py debug --phase 2.3 --step abstract_critic
   python pipeline_cli.py profile --phase 2.1-2.4
   ```

2. **Logging & Monitoring System** (`src/monitoring/`)
   ```
   src/monitoring/
   ├── __init__.py
   ├── logger.py         # Structured logging
   ├── progress.py       # Progress tracking
   ├── profiler.py       # Performance profiling
   └── cost_tracker.py   # API cost monitoring
   ```

3. **Development Utilities**
   - Phase validation without execution
   - Interactive debugging capabilities
   - Performance profiling and bottleneck identification
   - API cost tracking and budgeting

#### **Technical Specifications**

**Development Mode Features**:
- Verbose logging with structured output
- Step-by-step execution with pause points
- State inspection between phases
- Error recovery and retry mechanisms

**Monitoring Requirements**:
- Progress bars with estimated completion times
- API call cost tracking (tokens/requests/cost)
- Performance metrics collection
- Memory usage monitoring for large documents

#### **Success Criteria**
- [ ] Development mode provides rich debugging experience
- [ ] Progress tracking works across all phases
- [ ] Cost monitoring helps control API expenses
- [ ] Performance profiling identifies bottlenecks
- [ ] Clear, actionable error messages and recovery suggestions

#### **Output Artifacts**
- Enhanced CLI with development features
- `src/monitoring/` module for logging and tracking
- Development workflow documentation

---

### **WP5: Output Management System**
**Owner**: Agent E  
**Duration**: 2 days  
**Priority**: MEDIUM  
**Dependencies**: WP2 (CLI core)

#### **Deliverables**

1. **Simplified Output Structure**
   ```
   outputs/
   ├── current/              # Latest pipeline run
   │   ├── phase_1/
   │   ├── phase_2/
   │   └── phase_3/
   ├── archive/              # Previous runs (timestamped)
   │   ├── 2024-01-15T10-30/
   │   └── 2024-01-14T15-45/
   ├── templates/            # Output templates and schemas
   └── analysis/             # Quality and performance reports
   ```

2. **Output Management Module** (`src/outputs/`)
   ```
   src/outputs/
   ├── __init__.py
   ├── manager.py        # OutputManager class
   ├── archiver.py       # Archive management
   └── exporter.py       # Export utilities
   ```

3. **CLI Output Commands**
   ```bash
   python pipeline_cli.py outputs --list
   python pipeline_cli.py outputs --archive 
   python pipeline_cli.py outputs --clean
   python pipeline_cli.py outputs --export-paper
   ```

#### **Technical Specifications**

**OutputManager Class**:
```python
class OutputManager:
    def __init__(self, base_path: str = "outputs"):
        pass
    
    def create_run_directory(self, run_id: str) -> Path:
        pass
    
    def archive_current_run(self) -> bool:
        pass
    
    def export_final_paper(self, format: str = "md") -> Path:
        pass
```

**Archive Strategy**:
- Automatic archiving after successful pipeline runs
- Configurable retention policy (keep last N runs)
- Compression for older archives
- Metadata tracking for each run

#### **Success Criteria**
- [ ] Clean, intuitive output directory structure
- [ ] Automatic archiving prevents output directory bloat
- [ ] Easy export of final papers in multiple formats
- [ ] Output management CLI commands work correctly
- [ ] Clear organization makes finding specific outputs easy

#### **Output Artifacts**
- Reorganized output directory structure
- `src/outputs/` management module
- Output management CLI commands

---

### **WP6: Performance & Dependency Optimization**
**Owner**: Agent F  
**Duration**: 2 days  
**Priority**: MEDIUM  
**Dependencies**: WP2 (CLI core), can run parallel with WP7

#### **Deliverables**

1. **Dependency Cleanup**
   ```
   requirements/
   ├── base.txt          # Core runtime dependencies
   ├── dev.txt           # Development tools
   └── optional.txt      # Optional features (Rivet, etc.)
   ```

2. **Performance Optimizations**
   - API call batching and intelligent caching
   - Parallel execution where safe
   - Memory optimization for large PDF processing
   - Smart retry policies with exponential backoff

3. **Resource Management** (`src/performance/`)
   ```
   src/performance/
   ├── __init__.py
   ├── api_cache.py      # API response caching
   ├── batch_processor.py # Batched operations
   └── memory_manager.py  # Memory optimization
   ```

#### **Technical Specifications**

**API Optimization**:
- Cache API responses to avoid redundant calls
- Batch multiple API calls when possible
- Implement intelligent retry with jitter
- Add request rate limiting to prevent rate limit errors

**Memory Management**:
- Stream processing for large PDF files
- Garbage collection optimization
- Memory usage monitoring and alerts

#### **Success Criteria**
- [ ] Reduced dependency footprint and faster installation
- [ ] 20%+ reduction in API costs through optimization
- [ ] Better handling of large documents without memory issues
- [ ] Improved error recovery from API failures
- [ ] Measurable performance improvements in pipeline execution

#### **Output Artifacts**
- Optimized dependency structure in `requirements/`
- `src/performance/` optimization modules
- Performance benchmarking results

---

### **WP7: Documentation & User Experience**
**Owner**: Agent G  
**Duration**: 2 days  
**Priority**: HIGH  
**Dependencies**: All other WPs for complete documentation

#### **Deliverables**

1. **Unified Documentation Structure**
   ```
   docs/
   ├── README.md                    # Quick start and overview
   ├── user-guide/
   │   ├── installation.md
   │   ├── quickstart.md  
   │   ├── configuration.md
   │   ├── cli-reference.md
   │   └── troubleshooting.md
   ├── developer-guide/
   │   ├── architecture.md
   │   ├── adding-phases.md
   │   ├── api-integration.md
   │   └── contributing.md  
   ├── api/                        # Generated API docs
   └── examples/
       ├── basic-usage.md
       ├── advanced-configuration.md
       └── development-workflow.md
   ```

2. **User Experience Polish**
   - Rich CLI help text with examples
   - Progress bars and status indicators  
   - Helpful error messages with resolution suggestions
   - Interactive setup wizard for first-time users

3. **Getting Started Experience**
   - One-command installation script
   - Sample data and tutorial walkthrough
   - Configuration validation and helpful setup
   - Clear success indicators

#### **Technical Specifications**

**CLI Help System**:
- Comprehensive help text for all commands
- Usage examples for common scenarios
- Context-sensitive help based on current state
- Progressive disclosure of advanced options

**Error Handling**:
- Categorized error types with specific resolution steps
- Links to relevant documentation sections
- Recovery suggestions based on error context

#### **Success Criteria**
- [ ] New users can get started in <5 minutes
- [ ] All CLI commands have clear, helpful documentation
- [ ] Error messages provide actionable resolution steps
- [ ] Developer documentation enables easy contribution
- [ ] Professional presentation suitable for public release

#### **Output Artifacts**
- Complete documentation in `docs/`
- Enhanced CLI help and error messages
- Installation and setup scripts
- Tutorial materials and examples

---

## Integration & Coordination

### **Daily Standup Format**
Each agent reports:
1. **Yesterday**: Work package progress, blockers encountered
2. **Today**: Planned work, dependencies needed
3. **Blockers**: Waiting on other agents, technical issues

### **Integration Points**
1. **WP1 → WP2**: Clean imports and structure before CLI development
2. **WP2 → WP4**: CLI core must be stable before adding dev features
3. **WP3 → All**: Configuration system integration points
4. **WP2,3,4 → WP7**: Core functionality must work before documentation

### **Communication Protocol**
- **Shared State**: All agents commit to `refactor-branch`
- **Integration Testing**: Daily integration tests of combined work
- **Conflict Resolution**: Agent B (CLI Core) has final say on architectural decisions
- **Documentation**: Each agent documents their interfaces for others

### **Quality Gates**
Each work package must pass:
1. **Functionality**: Core features work as specified
2. **Integration**: Plays well with other work packages
3. **Documentation**: Clear interface documentation for other agents
4. **Backward Compatibility**: Existing pipeline still works

---

## Success Metrics & Validation

### **Overall Success Criteria**
- [ ] Single CLI entry point replaces all 13 runner scripts
- [ ] Backward compatibility: all existing functionality preserved
- [ ] <5 minute setup time for new developers
- [ ] Professional documentation and user experience
- [ ] Clean, maintainable codebase architecture

### **Performance Targets**
- [ ] Pipeline execution time unchanged or improved
- [ ] API costs reduced by 15-25% through optimization
- [ ] Memory usage stable for large document processing
- [ ] Installation time <2 minutes

### **User Experience Targets**
- [ ] Intuitive CLI with progressive disclosure
- [ ] Clear error messages with resolution steps
- [ ] Rich development mode for debugging
- [ ] Comprehensive but accessible documentation

---

## Risk Management

### **High-Risk Dependencies**
- **WP1 → All**: Structure changes could break everything
- **WP2**: CLI core architecture affects all subsequent work
- **WP3**: Configuration changes could break existing setups

### **Mitigation Strategies**
- **Incremental Integration**: Test integration daily, not at the end
- **Backward Compatibility**: Maintain existing script functionality during transition
- **Rollback Plan**: Keep current working version as fallback
- **Communication**: Over-communicate integration points and dependencies

### **Critical Path Monitoring**
- **Day 2**: WP1 completion unblocks WP2
- **Day 4**: WP2 completion unblocks WP4, WP5
- **Day 6**: Core functionality integration testing
- **Day 8**: Performance and documentation integration
- **Day 10**: Final integration and release preparation

---

This master plan provides the framework for coordinated refactoring while maintaining the sophisticated philosophical processing capabilities that make this pipeline unique.