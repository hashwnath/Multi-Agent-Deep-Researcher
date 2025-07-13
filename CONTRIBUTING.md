# Contributing to Advanced Research Agent

Thank you for your interest in contributing to the Advanced Research Agent project! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### **Reporting Issues**
- Use the GitHub issue tracker to report bugs or request features
- Provide detailed information about the issue, including:
  - Steps to reproduce
  - Expected vs actual behavior
  - Environment details (OS, Python version, etc.)
  - Error messages or logs

### **Submitting Pull Requests**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Ensure all tests pass
6. Commit your changes with a clear message (`git commit -m 'Add amazing feature'`)
7. Push to your branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📋 Development Guidelines

### **Code Style**
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and concise

### **Testing**
- Add tests for new features
- Ensure existing tests pass
- Test with different research types and queries

### **Documentation**
- Update README.md if adding new features
- Add docstrings to new functions and classes
- Update example queries if relevant

## 🏗️ Project Structure

### **Adding New Research Types**
1. Add new research type to `models.py`
2. Create specialized prompts in `prompts.py`
3. Add research agent in `workflow.py`
4. Update output formatting in `main.py`

### **Adding New Agents**
1. Create agent class in appropriate module
2. Add to workflow orchestration
3. Update state management
4. Add tests

## 🔒 Security Guidelines

### **API Keys and Secrets**
- Never commit API keys or secrets
- Use environment variables for configuration
- Update `.env.example` with new variables
- Ensure `.env` is in `.gitignore`

### **Data Privacy**
- Respect user privacy and data protection
- Follow relevant regulations (GDPR, CCPA, etc.)
- Implement proper data handling practices

## 🧪 Testing

### **Running Tests**
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=src
```

### **Test Coverage**
- Aim for >80% test coverage
- Test edge cases and error conditions
- Mock external API calls

## 📝 Commit Messages

Use clear, descriptive commit messages:
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests

### **Examples**
```
Add PDF relevance scoring feature
Fix intent detection for educational queries
Update developer tools research prompts
```

## 🚀 Release Process

### **Versioning**
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Update version in `pyproject.toml`
- Create release notes

### **Release Checklist**
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version bumped
- [ ] Release notes written
- [ ] Tagged release

## 📞 Getting Help

- Open an issue for questions or problems
- Join discussions in GitHub issues
- Follow the project's code of conduct

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to making the Advanced Research Agent better! 🚀 