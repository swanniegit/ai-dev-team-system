# Contributing to Agentic Agile System

Thank you for your interest in contributing! We welcome all contributions—bug reports, feature requests, documentation, and code.

## Getting Started

1. **Fork the repository** and clone your fork.
2. **Create a new branch** for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Install dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. **Run tests** to ensure your environment is working:
   ```bash
   pytest
   ```

## Coding Standards
- Follow [PEP8](https://www.python.org/dev/peps/pep-0008/) for Python code.
- Write clear, concise commit messages (use [Conventional Commits](https://www.conventionalcommits.org/)).
- Add or update docstrings for all public functions and classes.
- Include or update tests for new features and bug fixes.

### Conventional Commits
We use [Conventional Commits](https://www.conventionalcommits.org/) for automated changelog generation. Format your commit messages as:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools

**Examples:**
```
feat(api): add new wellness checkin endpoint
fix(agents): resolve PM agent registration issue
docs(readme): update installation instructions
test(wellness): add unit tests for checkin creation
```

## Pull Request Process
1. Ensure your branch is up to date with `main`.
2. Open a pull request (PR) against the `main` branch.
3. Fill out the PR template and describe your changes.
4. Ensure all CI checks pass (tests, lint, security, coverage).
5. Address any review comments.
6. Once approved, your PR will be merged by a maintainer.

## Community Guidelines
- Be respectful and inclusive.
- Use GitHub Issues for bugs, feature requests, and questions.
- For security issues, see [SECURITY.md](.github/SECURITY.md).

## Need Help?
- See the [README.md](README.md) for setup and usage.
- Check the [FAQ](README.md#getting-help--faq) section.
- Open a GitHub Issue if you’re stuck.

Happy contributing! 🚀 