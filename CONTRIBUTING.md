# Contributing to Philosophy Pipeline

Thank you for your interest in contributing to the Philosophy Pipeline! This guide will help you get started.

## 🚀 Quick Start for Contributors

### 1. **Setup Development Environment**
```bash
git clone [repository]
cd philosophy-pipeline
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. **Follow Setup Guide**
- See `docs/development/setup_guide.md` for complete setup instructions
- Download Analysis journal PDFs to `Analysis_papers/` directory
- Set up `.env` file with API keys

### 3. **Run Tests**
```bash
python -m pytest tests/
```

## 📋 Development Workflow

### **Before Making Changes**
1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Check current documentation in `docs/` to understand the system
3. Review `docs/CURRENT_STATUS.md` for recent changes
4. Test that the pipeline works: `python run_phase_1_1.py`

### **Making Changes**
1. **Code Changes**: Follow existing patterns in `src/`
2. **Prompt Changes**: Update corresponding files in `src/phases/*/prompts/`
3. **Documentation**: Update relevant docs in `docs/`
4. **Data Changes**: Update `data/` directory if adding philosophical moves/examples

### **Testing Changes**
1. **Individual Phases**: Test specific phases (e.g., `python run_phase_2_1.py`)
2. **Integration Testing**: Run multiple phases to ensure compatibility
3. **Documentation**: Verify setup instructions work for new contributors

### **Submitting Changes**
1. Update documentation if you've changed functionality
2. Commit with clear, descriptive messages
3. Push to your branch: `git push origin feature/your-feature-name`
4. Create pull request with detailed description

## 🎯 Types of Contributions

### **High-Impact Areas**
1. **Prompt Engineering**: Improving prompts in `src/phases/*/prompts/`
2. **Quality Control**: Enhancing validation and testing
3. **Documentation**: Making setup/usage clearer
4. **Performance**: Optimizing token usage and API calls
5. **Citation Accuracy**: Implementing fact-checking systems

### **Data Contributions**
1. **Philosophical Moves**: Add to `data/philosophical_moves/injectable_examples.json`
2. **Analysis Examples**: Curate additional Analysis journal patterns
3. **Style Guides**: Improve `data/style_guides/`
4. **Test Cases**: Add examples for testing and validation

### **Code Quality**
1. **Type Hints**: Add/improve type annotations
2. **Error Handling**: Robust error handling and logging
3. **Testing**: Unit tests and integration tests
4. **Documentation**: Inline code documentation

## 📝 Code Style Guidelines

### **Python Style**
- Follow PEP 8 style guidelines
- Use type hints for function parameters and returns
- Add docstrings for classes and public methods
- Use descriptive variable names

### **Prompt Engineering**
- Keep prompts readable with clear sections (`<context>`, `<task>`, etc.)
- Include comprehensive examples and guidance
- Use consistent formatting and structure
- Test prompts thoroughly before committing

### **Documentation**
- Update relevant documentation when changing functionality
- Use clear, concise language
- Include examples and code snippets
- Keep docs synced with actual implementation

## 🧪 Testing Guidelines

### **Manual Testing**
- Test individual phases before submitting
- Verify end-to-end pipeline functionality
- Check that new features don't break existing functionality

### **Automated Testing**
- Add unit tests for new functionality
- Test edge cases and error conditions
- Ensure tests are reproducible

### **Integration Testing**
- Test how your changes affect the overall pipeline
- Verify that phase outputs are compatible
- Check that documentation changes are accurate

## 🔧 Development Tips

### **Understanding the Pipeline**
1. Read `docs/ARCHITECTURE.md` for system design
2. Check `docs/CURRENT_STATUS.md` for recent changes
3. Review `data/README.md` for data organization
4. Study existing phases for patterns

### **Common Development Tasks**
- **Adding New Phase**: Study existing phase structure in `src/phases/`
- **Modifying Prompts**: Update both code and test thoroughly
- **Improving Quality**: Add validation and error checking
- **Optimizing Performance**: Focus on token efficiency and API usage

### **Working with API Keys**
- Never commit API keys to the repository
- Use `.env` file for local development
- Test with rate limiting in mind

## 🚨 Common Issues

### **Setup Issues**
- **Missing Analysis papers**: Download PDFs to `Analysis_papers/`
- **API key errors**: Check `.env` file configuration
- **Import errors**: Ensure virtual environment is activated

### **Development Issues**
- **Path errors**: Check that `data/` directory is properly organized
- **JSON parsing**: Ensure prompt outputs are valid JSON
- **Rate limiting**: Be mindful of API call frequency

## 📊 Pull Request Guidelines

### **PR Description Should Include**
1. **What changed**: Clear description of modifications
2. **Why**: Explanation of motivation and context
3. **Testing**: How you tested the changes
4. **Documentation**: What documentation was updated
5. **Breaking changes**: Any backwards compatibility issues

### **PR Checklist**
- [ ] Code follows project style guidelines
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] Changes are backwards compatible (or breaking changes are noted)
- [ ] Commit messages are clear and descriptive

## 🎓 Learning Resources

### **Understanding the Philosophy Pipeline**
- Study recent papers in Analysis journal for style guidance
- Review philosophical move patterns in `data/philosophical_moves/`
- Examine existing prompts for engineering patterns

### **Technical Resources**
- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Analysis Journal](https://academic.oup.com/analysis) for style guidance

## 📞 Getting Help

### **For Questions About**
- **Setup**: Check `docs/development/setup_guide.md`
- **Architecture**: Review `docs/ARCHITECTURE.md`
- **Current status**: See `docs/CURRENT_STATUS.md`
- **Data organization**: Read `data/README.md`

### **For Complex Issues**
- Create an issue with detailed description
- Include error messages and context
- Describe what you've already tried

## 🏆 Recognition

Contributors who make significant improvements to the pipeline will be acknowledged in the project documentation and any resulting publications.

Thank you for helping advance AI-driven philosophical research! 