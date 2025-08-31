# Troubleshooting Guide

This guide covers common issues you may encounter when using the Philosophy Pipeline and how to resolve them.

## Quick Diagnostics

Start with these basic diagnostic commands:

```bash
# Check environment setup
python pipeline_cli.py validate

# Check current status
python pipeline_cli.py status

# Test API connectivity
python -c "
import os
from anthropic import Anthropic
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
print('Anthropic API: OK')
"
```

## Installation Issues

### Virtual Environment Problems

**Problem**: Virtual environment activation fails
```bash
# Error: command not found: source
```

**Solution**:
```bash
# Try these alternatives:
python3 -m venv venv
source venv/bin/activate

# On Windows PowerShell:
venv\Scripts\Activate.ps1

# On Windows Command Prompt:
venv\Scripts\activate.bat
```

### Dependency Installation Failures

**Problem**: `pip install -r requirements.txt` fails

**Solution**:
```bash
# Upgrade pip first
pip install --upgrade pip

# Install with verbose output to see errors
pip install -r requirements.txt -v

# On macOS, may need:
pip install --upgrade setuptools wheel

# On Linux, may need development headers:
sudo apt-get install python3-dev build-essential
```

### Permission Issues

**Problem**: Permission denied errors

**Solution**:
```bash
# On Linux/macOS:
chmod +x pipeline_cli.py

# Check file permissions
ls -la pipeline_cli.py

# Ensure you own the directory
sudo chown -R $USER:$USER /path/to/philosophy-pipeline
```

## API Configuration Issues

### Missing API Keys

**Problem**: 
```
Error: No API key found for Anthropic
```

**Solution**:
```bash
# Check .env file exists
ls -la .env

# Check .env contents (without exposing keys)
grep -c "ANTHROPIC_API_KEY" .env

# Create .env if missing
cp .env.example .env
# Then edit .env with your actual API keys
```

### Invalid API Keys

**Problem**:
```
Error: Invalid API key or insufficient credits
```

**Solution**:
1. **Verify API Key Format**:
   ```bash
   # Anthropic keys start with 'sk-ant-'
   # OpenAI keys start with 'sk-'
   ```

2. **Check Account Status**:
   - Visit [Anthropic Console](https://console.anthropic.com)
   - Verify account has sufficient credits
   - Check API key is active and not expired

3. **Test API Key Manually**:
   ```python
   import os
   from anthropic import Anthropic
   
   client = Anthropic(api_key="your-key-here")
   response = client.messages.create(
       model="claude-sonnet-4",
       max_tokens=100,
       messages=[{"role": "user", "content": "Hello"}]
   )
   print("API key works:", response.content)
   ```

### Rate Limiting

**Problem**:
```
Error: Rate limit exceeded
```

**Solution**:
```bash
# The pipeline handles rate limits automatically
# Just wait and retry - no action needed

# For persistent issues, adjust rate limits in config:
```
```yaml
# config/conceptual_config.yaml
api:
  anthropic:
    max_requests_per_minute: 30  # Reduce from default 50
    retry_delay: 2.0             # Increase delay
```

## Pipeline Execution Issues

### Phase Dependencies

**Problem**:
```
Error: Phase 2.2 requires outputs from phase 2.1
```

**Solution**:
```bash
# Run phases in correct order
python pipeline_cli.py run --phases 2.1,2.2,2.3

# Or check what's missing
python pipeline_cli.py status
ls -la outputs/
```

### Missing Literature Files

**Problem**:
```
Error: No PDF files found in papers/ directory
```

**Solution**:
```bash
# Check papers directory
ls -la papers/

# Use sample papers
cp sample_output_papers/paper_1/papers/*.pdf papers/

# Or download specific papers manually:
# 1. Run literature search: python pipeline_cli.py run --phase 1.2
# 2. Check outputs/literature_research_papers.md
# 3. Download suggested papers to papers/ directory
```

### Memory Issues

**Problem**:
```
Error: Memory allocation failed
```

**Solution**:
```bash
# Monitor memory usage
python pipeline_cli.py monitor --metrics

# Use lighter configuration
python pipeline_cli.py --config config/environments/development.yaml run --full

# Close other applications
# Or increase swap space on Linux:
sudo swapon --show
```

### Disk Space Issues

**Problem**:
```
Error: No space left on device
```

**Solution**:
```bash
# Check disk space
df -h

# Clean old outputs
python pipeline_cli.py outputs --clean 2

# Check output directory size
du -sh outputs/
```

## Configuration Issues

### Invalid Configuration

**Problem**:
```
Error: Configuration validation failed
```

**Solution**:
```bash
# Validate configuration syntax
python -c "
import yaml
try:
    with open('config/conceptual_config.yaml') as f:
        config = yaml.safe_load(f)
    print('Configuration YAML syntax: OK')
except Exception as e:
    print('Configuration error:', e)
"

# Use default configuration
python pipeline_cli.py --config config/base.yaml validate
```

### Model Configuration Issues

**Problem**:
```
Error: Model 'claude-sonnet-5' not found
```

**Solution**:
```bash
# Check available models in your API account
# Update configuration to use supported models:
```
```yaml
models:
  default:
    model: "claude-sonnet-4"  # Use known working model
```

## Phase-Specific Issues

### Phase I.2 (Literature Search)

**Problem**:
```
Error: Rivet server not responding
```

**Solution**:
```bash
# Check Rivet server status
cd rivet
ps aux | grep node

# Start Rivet server
node server.js

# In separate terminal, check connection
curl -X GET http://localhost:3000/health
```

**Problem**: Tavily API errors

**Solution**:
```bash
# Verify Tavily API key
echo $TAVILY_API_KEY

# Test Tavily API directly
curl -X POST "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d '{"api_key": "your_key", "query": "philosophy", "max_results": 1}'
```

### Phase II.1 (Literature Processing)

**Problem**:
```
Error: Failed to process PDF
```

**Solution**:
```bash
# Check PDF files are readable
file papers/*.pdf

# Test PDF processing manually
python -c "
import PyPDF2
with open('papers/example.pdf', 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    print(f'Pages: {len(reader.pages)}')
    print(f'First page text: {reader.pages[0].extract_text()[:100]}')
"

# If PDFs are corrupted, re-download them
```

### Phase II.2-2.4 (Framework Development)

**Problem**: Phases taking too long

**Solution**:
```bash
# Use development configuration for faster execution
python pipeline_cli.py --config config/environments/development.yaml run --phases 2.2-2.4

# Monitor progress
python pipeline_cli.py monitor --metrics

# Or reduce iteration cycles:
```
```yaml
phases:
  phase_2:
    framework:
      max_cycles: 2  # Reduce from default 3
```

### Phase II.5-2.8 (Quality Control)

**Problem**:
```
Error: Hájek heuristics validation failed
```

**Solution**:
```bash
# Check if quality inputs exist
ls -la outputs/framework_development/
ls -la outputs/key_moves_development/

# Disable problematic heuristics temporarily:
```
```yaml
quality:
  heuristics:
    tests:
      extreme_case: { enabled: false }  # Disable if causing issues
```

### Phase III.1-3.2 (Writing)

**Problem**:
```
Error: Writing context not found
```

**Solution**:
```bash
# Ensure Phase II.8 completed successfully
python pipeline_cli.py status
ls -la outputs/phase_2_8_writing_context.json

# Re-run Phase II.8 if needed
python pipeline_cli.py run --phase 2.8
```

**Problem**: Generated paper too short/long

**Solution**:
```yaml
# Adjust word targets in configuration
phases:
  phase_3:
    writing:
      target_words: 4000  # Adjust as needed
      section_weights:
        introduction: 0.15
        main_argument: 0.65  # Increase for longer papers
        objections: 0.15
        conclusion: 0.05
```

## Performance Issues

### Slow Execution

**Problem**: Pipeline runs slower than expected

**Diagnosis**:
```bash
# Profile execution
python pipeline_cli.py profile --full

# Monitor resource usage
python pipeline_cli.py monitor --metrics
```

**Solutions**:
1. **Use Faster Models**:
   ```yaml
   models:
     default:
       model: "claude-sonnet-3.5"  # Faster than Sonnet 4
   ```

2. **Reduce Iterations**:
   ```yaml
   phases:
     phase_2:
       framework: { max_cycles: 2 }
       key_moves: { moves_count: 2 }
   ```

3. **Enable Caching**:
   ```yaml
   models:
     default:
       use_caching: true
   ```

### High API Costs

**Problem**: Unexpectedly high API costs

**Diagnosis**:
```bash
# Check cost breakdown
python pipeline_cli.py cost report --period day

# Monitor costs during execution
python pipeline_cli.py run --full --track-costs --budget 20.0
```

**Solutions**:
1. **Set Budget Limits**:
   ```bash
   python pipeline_cli.py cost budget --set 50.0
   ```

2. **Use Cheaper Models**:
   ```yaml
   models:
     default:
       model: "claude-sonnet-3.5"
       temperature: 0.5
   ```

3. **Optimize Prompt Length**:
   ```yaml
   phases:
     phase_2:
       key_moves:
         examples_per_move: 1  # Reduce from 2
   ```

## Output Issues

### Missing Output Files

**Problem**: Expected output files don't exist

**Diagnosis**:
```bash
# Check what outputs exist
python pipeline_cli.py outputs --list

# Check specific phase outputs
ls -la outputs/framework_development/
ls -la outputs/key_moves_development/
```

**Solutions**:
1. **Re-run Failed Phases**:
   ```bash
   python pipeline_cli.py status  # Check which phases failed
   python pipeline_cli.py run --phase 2.X  # Re-run specific phase
   ```

2. **Check Error Messages**:
   ```bash
   # Enable debug mode to see detailed errors
   python pipeline_cli.py --debug run --phase 2.X
   ```

### Corrupted Output Files

**Problem**: JSON files are corrupted or empty

**Solution**:
```bash
# Validate JSON files
python -c "
import json
import sys
try:
    with open(sys.argv[1]) as f:
        data = json.load(f)
    print('Valid JSON')
except Exception as e:
    print('Invalid JSON:', e)
" outputs/final_selection.json

# Remove corrupted files and re-run
rm outputs/corrupted_file.json
python pipeline_cli.py run --phase X.X
```

## Debugging Strategies

### Enable Debug Mode

```bash
# Maximum debugging information
python pipeline_cli.py --debug --verbose run --phase 2.3
```

### Step-by-Step Execution

```bash
# Interactive mode with confirmations
python pipeline_cli.py run --full --interactive

# Debug specific phase
python pipeline_cli.py debug --phase 2.3
```

### Check Logs

```bash
# Enable file logging
python pipeline_cli.py --log-dir logs run --full

# Review logs
tail -f logs/pipeline.log
grep ERROR logs/pipeline.log
```

### Isolate Issues

```bash
# Run single phase to isolate problems
python pipeline_cli.py run --phase 2.1

# Use minimal configuration
python pipeline_cli.py --config config/environments/development.yaml run --phase 2.1
```

## Getting Additional Help

### Check System Status
```bash
# Complete system validation
python pipeline_cli.py validate

# Check all requirements
python -c "
import sys
print('Python version:', sys.version)
"

# Check package versions
pip list | grep -E "(anthropic|openai|yaml)"
```

### Collect Debug Information

Before reporting issues, collect this information:

```bash
# System information
python --version
uname -a  # Linux/macOS
pip list > installed_packages.txt

# Pipeline status
python pipeline_cli.py status --json > pipeline_status.json
python pipeline_cli.py validate > validation_results.txt

# Configuration
cp config/conceptual_config.yaml debug_config.yaml
```

### Common Log Locations

- **Console Output**: Use `--verbose` and `--debug` flags
- **File Logs**: Use `--log-dir logs` option
- **Cost Tracking**: `outputs/cost_tracking/`
- **Profiling Data**: `outputs/profiling/`
- **Error Outputs**: Check individual phase output files

### Community Resources

1. **GitHub Issues**: Search existing issues first
2. **Documentation**: Check [Architecture Guide](../developer-guide/architecture.md)
3. **Examples**: Review [Examples Directory](../examples/)
4. **Configuration**: See [Configuration Guide](configuration.md)

### Report New Issues

When reporting issues, include:

1. **Error Message**: Full error output with stack trace
2. **System Info**: Python version, OS, package versions
3. **Configuration**: Relevant configuration sections
4. **Steps to Reproduce**: Minimal example that triggers the issue
5. **Expected vs Actual**: What you expected vs what happened

Most issues can be resolved by:
1. Checking API keys and credits
2. Verifying all dependencies are installed
3. Running validation checks
4. Using debug mode to get detailed error information
5. Reviewing configuration for typos or invalid values