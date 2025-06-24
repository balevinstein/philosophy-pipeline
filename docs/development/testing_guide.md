# Quick Test Guide

This guide provides options for testing the philosophy pipeline without running the full 2+ hour process.

## Option 1: Test New Quality Control Phases (Recommended)

If you have existing outputs from Phase II.1-4, you can test just the new quality control phases:

```bash
# Prerequisites: outputs from Phase II.1-4 must exist
# Total time: ~5 minutes

# Test quality control and refinement
python run_phase_2_5.py    # ~85 seconds
python run_phase_2_6_review.py  # ~90 seconds  
python run_phase_2_7.py    # ~20 seconds
python run_phase_2_8.py    # ~92 seconds

# Quick writing test (single section)
# Modify run_phase_3_1.py to process only 1 section for testing
```

## Option 2: Minimal Pipeline Test

Test core functionality with reduced iterations:

1. **Modify config** (`config/conceptual_config.yaml`):
   ```yaml
   # Reduce iterations for testing
   stages:
     phase_2_3:
       max_iterations: 1  # Instead of 3
   ```

2. **Run abbreviated pipeline**:
   ```bash
   # Use existing topic and literature
   python run_phase_2_2.py    # Framework only
   python run_phase_2_3.py    # Key moves (reduced)
   python run_phase_2_5.py    # Quality check
   ```

## Option 3: Component Testing

Test individual components in isolation:

### Test Quality Standards
```python
# test_quality_standards.py
from src.phases.phase_two.stages.stage_five.workers.consolidation_worker import ConsolidationWorker
from src.utils.api import load_config

config = load_config()
worker = ConsolidationWorker(config)

# Load sample data
test_state = {
    "abstract": "Test philosophical thesis...",
    "outline": {"sections": [...]},
    "key_moves": [{"content": "Test move..."}]
}

result = worker.execute(test_state)
print(result.data["issues_identified"])
```

### Test Writing Aids
```python
# test_writing_aids.py
from src.phases.phase_two.stages.stage_eight.workers.writing_optimization_worker import WritingOptimizationWorker

# Test hook generation
worker = WritingOptimizationWorker(config)
# ... setup test state ...
```

## Option 4: Archive Review

Review existing outputs without running anything:

```bash
# Check quality of previous runs
cat outputs/phase_2_5_consolidated_context.json | jq '.issues_identified'
cat outputs/final_paper.md | head -50
```

## Verification Checklist

After any test run, verify:

1. **Quality Standards Applied**: Check Phase II.5 output for Hájek test results
2. **Review Generated**: Phase II.6 should identify specific issues
3. **Refinements Made**: Phase II.7 should show move status changes
4. **Writing Aids Created**: Phase II.8 should have hooks and transitions
5. **No Errors**: Check logs in `outputs/logs/`

## Common Test Scenarios

### Scenario 1: Testing After Code Changes
- Run Option 1 to verify quality control still works
- Check that all JSON outputs parse correctly
- Verify API calls succeed

### Scenario 2: Testing New Topics
- Use Option 2 with reduced iterations
- Focus on Phase II.2-5 for framework validation
- Skip full writing phases initially

### Scenario 3: Debugging Issues
- Use Option 3 to isolate problematic components
- Add print statements to workers
- Check `outputs/debug_*.txt` files

## Tips for Faster Testing

1. **Use Cached Literature**: Keep PDFs in `papers/` directory
2. **Reuse Frameworks**: Copy existing Phase II.2 outputs
3. **Single Section Writing**: Modify Phase III.1 to write only introduction
4. **Skip Refinement**: Test only development workers initially
5. **Lower Token Limits**: Reduce max_tokens in config for faster responses 