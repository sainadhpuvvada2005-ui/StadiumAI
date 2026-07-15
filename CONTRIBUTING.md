# Contributing to StadiumAI

Thank you for considering a contribution to StadiumAI! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful and constructive in all interactions. We're building a platform for everyone.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/StadiumAI.git
   cd StadiumAI
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Set up your development environment** (see README.md)

## Development Workflow

### Backend Development

```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-local.txt
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Running Tests

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm test
```

## Code Style Guidelines

### Backend (Python)

- Follow PEP 8 standards
- Use type hints for all functions
- Run `ruff` for linting:
  ```bash
  ruff check app/
  ```
- Comments should explain *why*, not *what*
- Use descriptive variable names
- Keep functions focused and small

Example:
```python
def validate_user_credentials(email: str, password: str) -> bool:
    """Validate email format and password strength."""
    return email_validator.is_valid(email) and len(password) >= 10
```

### Frontend (TypeScript/React)

- Use TypeScript for type safety
- Follow React best practices
- Component names should be PascalCase
- Use descriptive prop names
- Keep components focused
- Run ESLint:
  ```bash
  npm run lint
  ```

Example:
```typescript
interface UserCardProps {
  userId: string;
  userName: string;
  onSelect: (id: string) => void;
}

export function UserCard({ userId, userName, onSelect }: UserCardProps) {
  return (
    <div onClick={() => onSelect(userId)}>
      {userName}
    </div>
  );
}
```

## Commit Message Guidelines

Write clear, descriptive commit messages:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring without feature changes
- `test`: Adding or updating tests
- `chore`: Build process, dependencies, tools

**Examples:**
```
feat(auth): add Google OAuth integration
fix(dashboard): resolve crowd chart rendering bug
docs(readme): add installation instructions
test(api): add auth endpoint tests
```

## Creating a Pull Request

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request** on GitHub with:
   - Clear title describing the change
   - Description of what you changed and why
   - Reference to related issues (e.g., "Fixes #123")
   - Screenshots for UI changes

3. **PR Checklist:**
   - [ ] Tests pass locally
   - [ ] Code follows style guidelines
   - [ ] Documentation updated
   - [ ] No breaking changes (or documented)
   - [ ] Commits are clean and descriptive

## Testing

- **Write tests** for new features
- **Update tests** when modifying existing functionality
- **Aim for >80% code coverage**

Backend:
```bash
cd backend
pytest --cov=app tests/
```

Frontend:
```bash
cd frontend
npm test -- --coverage
```

## Documentation

- Update README.md if adding features
- Add docstrings to functions (backend and frontend)
- Comment complex logic
- Update API documentation in code comments

## Issues and Bugs

### Reporting Bugs

When reporting bugs, include:
- Description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment details (OS, browser, Python version, etc.)

### Suggesting Features

Feature suggestions should include:
- Clear description of the feature
- Use cases and benefits
- Possible implementation approach
- Any relevant mockups or examples

## Project Structure

```
StadiumAI/
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── models/      # SQLAlchemy models
│   │   ├── services/    # Business logic
│   │   ├── security/    # Auth, JWT, passwords
│   │   └── db/          # Database
│   ├── tests/           # Test files
│   └── requirements.txt
├── frontend/             # React application
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── lib/         # Utilities
│   │   └── types/       # TypeScript types
│   └── package.json
├── database/            # SQL schemas
├── ai/                  # AI/RAG assets
└── deployment/          # Docker configs
```

## Performance Considerations

- **Backend**: Keep response times under 500ms
- **Frontend**: Monitor bundle size
- **Database**: Use indexes for frequently queried fields
- **API**: Implement pagination for large datasets

## Security

- Never commit secrets or API keys
- Use environment variables for configuration
- Validate all user inputs
- Use parameterized queries (SQLAlchemy handles this)
- Follow OWASP guidelines

## Questions?

- Check existing issues and discussions
- Comment on related PRs
- Email: admin@stadiumai.example

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thanks for contributing to StadiumAI! 🎉
