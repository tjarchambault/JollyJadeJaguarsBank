# Development Guide - JollyJadeJaguarsBank

## Getting Started

### Prerequisites
- Python 3.10+
- Git
- GitHub account

### Initial Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/tjarchambault/JollyJadeJaguarsBank.git
   cd JollyJadeJaguarsBank
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Branch Strategy

- **main** — Production branch (stable releases)
- **develop** — Integration branch (base for features)
- **feature/*** — New features (branch from develop)
- **bugfix/*** — Bug fixes (branch from develop)
- **docs/*** — Documentation updates

### Creating a Feature Branch
```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

## Commit Workflow

1. Make changes in your feature branch
2. Write clear, atomic commits
   ```bash
   git add .
   git commit -m "feat: description of feature"
   ```
3. Push to remote
   ```bash
   git push origin feature/your-feature-name
   ```
4. Open Pull Request on GitHub
5. Request team review
6. Address feedback
7. Merge after approval

## Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_transactions.py -v
```

### Run with Coverage Report
```bash
pytest tests/ --cov=src --cov-report=html
```

### Write New Tests
- Place in `/tests` directory
- Use `test_` prefix for filenames and functions
- Include docstrings explaining what is tested
- Follow pytest conventions

## Code Style

- Follow **PEP 8** guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Include inline comments for complex logic
- Aim for readability over brevity

## Module Structure

### `/src` - Source Code
Each module should have:
- Module-level docstring with course info, author, date
- Clear function/class docstrings
- Input validation
- Exception handling

### `/tests` - Unit Tests
Test files correspond to source modules:
- `test_transactions.py` — tests for transactions.py
- `test_storage.py` — tests for storage.py
- `test_summaries.py` — tests for summaries.py

### `/data` - Data Files
- `transactions.csv` — transaction records (generated)
- `categories.csv` — category list (template provided)

### `/docs` - Documentation
- Phase reports (PDF)
- Architecture diagrams
- Development guide (this file)

## Phase Checkpoints

### Phase 2 (Due Sep 13)
- Transactions module complete
- Storage/CSV layer working
- CLI skeleton for add/list transactions
- Basic unit tests
- Phase 2 report submitted

### Phase 3 (Due Sep 27)
- Reports module (summaries.py) implemented
- Exception handling throughout
- CLI reporting commands
- Comprehensive tests
- Phase 3 report submitted

### Phase 4 (Due Oct 11)
- Visualizations complete (Turtle graphics)
- Full integration testing
- Final documentation
- Final project report submitted

## Team Communication

- Use GitHub Issues to track work and bugs
- Pull Requests for code review and discussion
- Weekly sync meetings recommended
- Document blockers and questions

## AI Assistance Policy

**Allowed uses:**
- Brainstorming design ideas
- Drafting code snippets
- Debugging strategies
- Documentation templates

**Team responsibility:**
- Every AI-generated code must be reviewed
- Test all assisted code thoroughly
- Each developer explains their final code
- Document AI usage in project reports

## Troubleshooting

**Import errors?**
- Confirm virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`

**CSV file issues?**
- Check `/data` directory exists
- Verify read/write permissions
- Look for corrupted headers

**Test failures?**
- Run with verbose output: `pytest -vv`
- Check test fixtures and setup

## Questions?

Open a GitHub Issue or contact the Team Leader.
