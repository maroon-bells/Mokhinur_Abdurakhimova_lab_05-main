# Lab 05 — From Books to Auditable Text Evidence

**Course:** Data Exploration and Extraction  
**Programme:** MSc Data Science  
**Lab:** 05  
**Course:** Data Exploration and Extraction 
**Done by Mokhinur Abdurakhimova** 
**Status:** Implementation, analysis outputs, and report included

## Project overview

This project turns two differently formatted fictional field reports into a validated chapter-level dataset. It extracts only the intended narrative sections, preserves an auditable copy of the retained source text, cleans typographic markup, counts four literal name mentions, and compares counts while accounting for chapter length.

The two source files are `data/journey.txt` and `data/survey.txt`. Both are fictional teaching texts. They deliberately contain front-matter mentions, endnotes, bibliography material, inline footnote references, Unicode accents, and names embedded in longer words. These features make it important to define and validate the source boundaries before counting.

## Lab objectives and tasks

### T1 — Inspect and document source boundaries

- Read the provenance notes and inspect both original UTF-8 source files.
- Compute byte-level SHA-256 hashes and record file metadata.
- Identify examples of front matter, endnotes, bibliography text, and inline footnote markers.
- Preserve the original files and their line breaks.

**Outputs:** `outputs/source_audit.csv`, `outputs/boundary_examples.csv`

### T2 — Extract and clean chapters

- Extract the four expected chapters (`I`–`IV`) from both documented layouts.
- Reject missing, duplicated, or unexpected chapter markers and invalid source boundaries.
- Keep raw retained prose separate from cleaned text.
- Remove markup delimiters and inline numeric footnote references, normalize Unicode to NFC, and collapse whitespace without removing accents or punctuation.
- Record parser rejection checks and before/after cleaning examples.

**Outputs:** `outputs/chapters.csv`, `outputs/parser_checks.csv`, `outputs/cleaning_examples.csv`

### T3 — Count names and compare rates

The analysis tracks four literal names: **Mira, Asad, Hajjāj, and Nasr**.

- Count case-insensitive literal mentions using Unicode word boundaries.
- Check that `Mirabel` is not counted as `Mira`.
- Independently verify the four counts in Journey Chapter I.
- Build a chapter-by-name NumPy matrix for each book and calculate cumulative mentions along the chapter axis.
- Calculate book-level rates using total mentions divided by total book words, multiplied by 1,000. Each chapter contributes to the book word denominator only once.
- Compare raw mention totals and length-normalized rates.

**Outputs:** `outputs/chapter_summary.csv`, `outputs/manual_check.csv`, `outputs/cumulative_mentions.csv`, `outputs/book_summary.csv`

### T4 — Visualize the evidence

Three Matplotlib figures show:

1. Cumulative mentions by chapter, with a separate panel for each book.
2. Chapter-level mentions per 1,000 words, with books distinguished.
3. Chapter word count versus period count, with chapters labeled.

**Outputs:** `outputs/cumulative_mentions.png`, `outputs/chapter_rates.png`, `outputs/length_vs_periods.png`

A period count is not a sentence count. Literal name mentions do not establish a person's presence, importance, sentiment, or historical events.

### T5 — Reproduce and interpret

- Explain extraction, cleaning, measurement choices, findings, limitations, and reproduction in `REPORT.md`.
- Record assistance and independent checks in `AI_USE.md`.
- Run the public tests and execute the notebook from top to bottom.
- Record Python/package versions and reproduction commands in `outputs/environment.txt`.

## Python version and environment

This lab specifies **Python 3.12**. The project was configured locally in PyCharm with a Python 3.12 interpreter.

![PyCharm showing the Python 3.12 interpreter]()

*Interpreter evidence: add the screenshot to `docs/images/python-3.12-interpreter.png` so it appears above on GitHub.*
<center><img width="301" height="187" alt="Screenshot 2026-11-27 at 12 16 26 AM" src="https://github.com/user-attachments/assets/b88041e6-4055-4b4d-9cfb-a6de9771b92a" />
> **Reproducibility note:** The currently included `outputs/environment.txt` records an earlier run under Python 3.13.5. A screenshot of the selected Python 3.12 interpreter confirms the IDE configuration, but does not by itself prove that the notebook and tests were rerun under Python 3.12. After selecting the Python 3.12 environment, rerun the tests and notebook, then update `outputs/environment.txt` with the actual versions from that run.

### Create an environment with Python 3.12

From the project root, a standard virtual environment can be created with:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python --version
```

If you use Conda, an alternative is:

```bash
conda create -n lab05 python=3.12 pip -y
conda activate lab05
python --version
```

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
python -m pip install jupyterlab ipykernel
```

## Run the analysis and tests

Run these commands from the directory containing this README:

```bash
# Check the Python version
python --version

# Compile source and test files
python -m compileall -q src tests

# Run the public tests
python -m unittest discover -s tests -p 'test_public.py' -v

# Execute the notebook from top to bottom
python -m jupyter nbconvert --to notebook --execute --inplace notebooks/lab.ipynb
```

The notebook reads the supplied source data, applies the functions in `src/solution.py`, and generates the result tables and figures under `outputs/`.

## Repository structure

```text
lab_05-main/
├── data/
│   ├── PROVENANCE.md
│   ├── journey.txt
│   └── survey.txt
├── docs/
│   └── images/
│       └── python-3.12-interpreter.png
├── notebooks/
│   └── lab.ipynb
├── outputs/
│   ├── boundary_examples.csv
│   ├── book_summary.csv
│   ├── chapter_rates.png
│   ├── chapter_summary.csv
│   ├── chapters.csv
│   ├── cleaning_examples.csv
│   ├── cumulative_mentions.csv
│   ├── cumulative_mentions.png
│   ├── environment.txt
│   ├── length_vs_periods.png
│   ├── manual_check.csv
│   ├── parser_checks.csv
│   └── source_audit.csv
├── src/
│   └── solution.py
├── tests/
│   └── test_public.py
├── AI_USE.md
├── FUNCTION_GUIDE.md
├── REPORT.md
├── requirements.txt
└── README.md
```

## Interpretation and limitations

The tracked values are literal text matches, not resolved people or entities. The method does not perform alias recognition, sentiment analysis, or historical verification. Rates are descriptive comparisons normalized by the number of retained words; they do not establish significance or explain why a name appears more often.

The raw source files are fictional teaching materials and should remain unchanged during the assessment. See `data/PROVENANCE.md` for source provenance and `FUNCTION_GUIDE.md` for the exact function contracts.

## Submission

Follow the instructor's submission instructions in `SUBMISSION.md`. The supplied instructions specify a private repository accessible to the teacher. For GitHub submission, create a `submission` branch, commit the completed work, and open a pull request to `main` titled:

```text
Lab 05 — your_github_username
```

Submit the pull request URL and the full final commit SHA through the LMS. Do not upload `.venv`, credentials, or cache files. Check the course deadline and resubmission policy before submitting.
