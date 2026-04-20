# Contributing to Escalation Detector Pipeline

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/escalation-pipeline.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate it and install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in your credentials
6. Create a new branch: `git checkout -b feature/your-feature-name`

## Development Guidelines

### Code Style

- Follow PEP 8 style guide for Python code
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose

### Commit Messages

Use clear, descriptive commit messages:
- `feat: add new endpoint for bulk escalation checks`
- `fix: resolve database connection timeout issue`
- `docs: update API documentation`
- `refactor: simplify LLM service error handling`

### Testing

Before submitting a pull request:
1. Test all API endpoints manually
2. Verify the frontend works correctly
3. Check that the health endpoint returns "healthy"
4. Ensure no errors in the console logs

### Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the CHANGELOG.md with your changes
3. Ensure your code follows the style guidelines
4. Submit your pull request with a clear description

## Areas for Contribution

### High Priority
- Add unit tests for LLM service
- Add integration tests for API endpoints
- Implement rate limiting for API calls
- Add authentication/authorization

### Medium Priority
- Add more detailed error messages
- Improve frontend UI/UX
- Add data visualization for statistics
- Implement webhook notifications for escalations

### Low Priority
- Add dark mode to frontend
- Add export functionality for logs
- Add filtering options in frontend
- Improve mobile responsiveness

## Questions?

Feel free to open an issue for any questions or suggestions!

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow
