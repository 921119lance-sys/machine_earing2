# Messy-to-Clean

## Student Details
- **Name:** [your name]
- **Student ID:** [your ID]
- **Course:** [course]
- **Lecturer:** [lecturer]
- **Deadline:** [date]

## Project Summary
[Line 1: Describe the messy dataset and the main problem.]
[Line 2: Explain what you want to clean, analyze, or improve.]

## Where to Find What

| Folder | Purpose |
|---|---|
| `data/raw/` | Original data; never edit. |
| `data/interim/` | Temporary data from cleaning steps. |
| `data/processed/` | Final cleaned data for analysis. |
| `notebooks/` | Jupyter notebooks for exploration and analysis. |
| `src/` | Reusable scripts and functions. |
| `reports/` | Report drafts, final paper (PDF), and slides. |
| `reports/figures/` | PNG charts for reports and slides. |
| `references/` | Assignment brief, papers, data dictionary/codebook, and lecturer feedback. |

## Progress log

| Date | What I did | Next step | Lecturer feedback |
|---|---|---|
| 2026-11-19 | Added CSV cleaner, automatic tests, and usage instructions. | Run tests and try a real CSV. | — |
| 2026-11-19 | Updated AGENTS.md with the nine project rules. | Follow these rules in future work. | — |

## Run the cleaning program

From the `messy-to-clean/` folder, run:

```bash
python src/clean_data.py --demo
python -m unittest discover -s src -p "test_*.py" -v
python src/clean_data.py data/raw/input.csv data/processed/cleaned.csv
```

The demo creates `data/processed/demo_cleaned.csv`. Input files stay unchanged. The cleaner trims spaces, standardizes column names, replaces common missing markers with blanks, and removes duplicate or empty rows. It does not guess missing values or change number formats.
