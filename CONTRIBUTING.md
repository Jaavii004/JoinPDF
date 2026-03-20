# Contributing to JoinPDF

Thank you for your interest in contributing to JoinPDF! We appreciate your help in making this tool better for everyone.

## Table of Contents
1. [Reporting Bugs](#reporting-bugs)
2. [Feature Requests](#feature-requests)
3. [Development Setup](#development-setup)
4. [Pull Request Process](#pull-request-process)
5. [Code Style](#code-style)

## Reporting Bugs
- Use the GitHub Issue Tracker to report bugs.
- Provide a clear and descriptive title.
- Describe the exact steps which reproduce the problem.
- Include information about your Windows version and any error messages shown.

## Feature Requests
- Check if the feature has already been requested.
- Explain why the feature would be useful for most users.

## Development Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Jaavii004/JoinPDF.git
   cd JoinPDF
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv JoinPDF
   source JoinPDF/Scripts/activate  # Or `JoinPDF\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```
3. Run the script:
   ```bash
   python unir_seleccion.py path/to/file1.pdf path/to/file2.pdf
   ```

## Pull Request Process
1. Fork the repository.
2. Create a new branch for your changes.
3. Keep your PRs focused on a single change.
4. Ensure the code runs correctly on Windows 10/11.
5. Update documentation if you add or change features.

## Code Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code.
- Add docstrings to new functions and classes.
- Use meaningful variable and function names.

---
By contributing, you agree that your contributions will be licensed under the project's MIT License.
