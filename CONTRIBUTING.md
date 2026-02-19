# Contributing to Optimizacion-de-recursos

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Branch Strategy](#branch-strategy)
- [Pull Request Process](#pull-request-process)
- [Code Standards](#code-standards)
- [Project Structure](#project-structure)

## Getting Started

1. **Fork the repository** to your GitHub account
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/Optimizacion-de-recursos.git
   cd Optimizacion-de-recursos
   ```
3. **Add the upstream remote**:
   ```bash
   git remote add upstream https://github.com/Lunaaaalj/Optimizacion-de-recursos.git
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Development Workflow

### 1. Create a Feature Branch

Always create a new branch for your work. Never commit directly to `main`.

```bash
# Update your local main branch
git checkout main
git pull upstream main

# Create a new feature branch
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features or enhancements
- `bugfix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Adding or updating tests

### 2. Make Your Changes

- Write clear, concise commit messages
- Keep commits atomic (one logical change per commit)
- Test your changes thoroughly

### 3. Commit Your Changes

```bash
git add .
git commit -m "feat: add descriptive commit message"
```

Commit message format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Formatting, missing semicolons, etc.
- `refactor:` - Code restructuring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

### 4. Keep Your Branch Updated

```bash
git fetch upstream
git rebase upstream/main
```

### 5. Push Your Changes

```bash
git push origin feature/your-feature-name
```

## Branch Strategy

### Protected Branches

- **`main`** - The main branch is protected and requires pull requests for all changes
  - Direct pushes are not allowed
  - All changes must go through the PR review process

### Merge Options

This repository supports three merge strategies:
1. **Merge commit** - Preserves all commits and creates a merge commit
2. **Squash and merge** - Combines all commits into a single commit (recommended for cleaner history)
3. **Rebase and merge** - Replays commits on top of the base branch

Choose the appropriate strategy based on your PR:
- Use **squash** for feature branches with many small commits
- Use **merge commit** for branches with well-organized commits
- Use **rebase** for simple, linear changes

## Pull Request Process

### Before Opening a PR

- [ ] Ensure your code follows the project's coding standards
- [ ] Run all tests and ensure they pass
- [ ] Update documentation if needed
- [ ] Rebase your branch on the latest `main`

### Opening a Pull Request

1. Go to the [repository](https://github.com/Lunaaaalj/Optimizacion-de-recursos)
2. Click "New Pull Request"
3. Select your feature branch
4. Fill out the PR template with:
   - **Clear title** describing the change
   - **Description** of what changed and why
   - **Related issues** (use "Closes #123" to auto-close issues)
   - **Testing performed**
   - **Screenshots** (if applicable)

### PR Review Process

- PRs require review before merging
- Address reviewer feedback promptly
- Keep the PR focused on a single concern
- Respond to comments and update your branch as needed

### After Approval

Once your PR is approved:
1. Ensure all checks pass
2. A maintainer will merge your PR
3. Your branch will be deleted (unless configured otherwise)

## Code Standards

### Python Code

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused

### LaTeX/Documentation

- Keep lines to a reasonable length
- Use consistent formatting
- Provide clear comments for complex sections

### Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Place tests in the `tests/` directory

## Project Structure

```
Optimizacion-de-recursos/
├── .github/          # GitHub configuration and workflows
├── bibliographies/   # Bibliography files
├── data/            # Data files
├── docs/            # Documentation
├── models/          # Model files
├── notebooks/       # Jupyter notebooks
├── references/      # Reference materials
├── reports/         # Generated reports
├── src/             # Source code
└── tests/           # Test files
```

## Questions?

If you have questions or need help:
- Open an issue for discussion
- Reach out to the maintainers
- Check existing issues and PRs for similar topics

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help create a welcoming environment

Thank you for contributing! 🎉
