# JollyJadeJaguarsBank - Personal Finance Tracker

**Course**: MSMIS 2028  
**Team**: JollyJadeJaguars  
**Repo**: tjarchambault/JollyJadeJaguarsBank

## 📋 Team Members

- **Team Leader**: Tom Archambault (tjarchambault@tamu.edu)
- **Developer 1**: Eric Bartkowski (eric.bartkowski@tamu.edu)
- **Developer 2**: Lucero Lopez (lucero.lopez02@tamu.edu)
- **Developer 3**: [TBD]
- **Developer 4**: [TBD]
- **Tester/Documenter**: [TBD]

## 🎯 Project Overview

A modular Python application to help users record, categorize, summarize, and visualize personal financial transactions (income, expenses, savings).

**See Project Proposal for full details and timeline.**

## 📁 Project Structure

```
JollyJadeJaguarsBank/
├── src/                           # Source code modules
│   ├── main.py                   # Application entry point
│   ├── transactions.py           # Transaction management
│   ├── storage.py                # CSV persistence layer
│   ├── categories.py             # Category management
│   ├── summaries.py              # Reports & calculations
│   ├── visualizations.py         # Turtle graphics & charts
│   └── cli.py                    # Command-line interface
├── tests/                         # Unit tests
│   ├── test_transactions.py
│   ├── test_summaries.py
│   └── test_storage.py
├── data/                          # Data files
│   ├── transactions.csv           # Transaction records
│   └── categories.csv             # Category definitions
├── docs/                          # Documentation
│   ├── DEVELOPMENT.md             # Development guide
│   ├── Phase-1-Project-Proposal.pdf
│   ├── Phase-2-Project-Report.pdf
│   ├── Phase-3-Project-Report.pdf
│   └── Phase-4-Final-Project-Report.pdf
├── images/                        # Generated visualizations
├── .gitignore                     # Git ignore rules
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🛠️ Technical Stack

- **Language**: Python 3.10+
- **Data Storage**: CSV (Phase 2)
- **Visualization**: Turtle Graphics (required)
- **Testing**: pytest
- **Optional**: Matplotlib, pandas, SQLite (advanced phases)

## 📅 Phase Timeline

| Phase | Due | Focus |
|-------|-----|-------|
| **Phase 1** | Aug 30 | Project Proposal |
| **Phase 2** | Sep 13 | Transaction Recording & CSV Persistence |
| **Phase 3** | Sep 27 | Reports & Exception Handling |
| **Phase 4** | Oct 11 | Visualizations & Final Integration |

## 🚀 Getting Started

### Prerequisites
```bash
python --version  # Must be 3.10 or higher
```

### Setup
```bash
# Clone repository
git clone https://github.com/tjarchambault/JollyJadeJaguarsBank.git
cd JollyJadeJaguarsBank

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Tests
```bash
pytest tests/ -v
```

## 📖 Development Workflow

1. Create feature branches from `develop`
2. Make atomic commits with clear messages
3. Submit PRs for code review
4. Merge after team approval
5. See `/docs/DEVELOPMENT.md` for detailed workflow

## 📝 Module Responsibilities

| Module | Developer | Purpose |
|--------|-----------|----------|
| `main.py` | Lead | Application entry point and flow |
| `transactions.py` | Dev 1 | Transaction data model & operations |
| `storage.py` | Dev 2 | CSV read/write & persistence abstraction |
| `categories.py` | Lead | Category management |
| `summaries.py` | Dev 1 | Financial reports & calculations |
| `visualizations.py` | Dev 3 | Turtle-based charts & graphs |
| `cli.py` | Dev 1 | User interface & menus |

## 🤖 AI Usage Policy

Generative AI tools (ChatGPT, GitHub Copilot) are **allowed** for:
- Brainstorming and design
- Code drafting and refinement
- Debugging assistance
- Documentation templates

**Each team member is responsible for reviewing, testing, and understanding all AI-assisted code.**

## 📚 Documentation

- See `/docs/DEVELOPMENT.md` for development guidelines
- See `/docs/DEVELOPMENT.md` for testing instructions
- Project Proposal contains full specifications

---

*Last Updated: August 22, 2026*
