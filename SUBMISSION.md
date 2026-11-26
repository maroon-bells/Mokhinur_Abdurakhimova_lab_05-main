# Start, check, and submit

Use Python 3.12. Open a terminal in the folder containing this lab's `README.md`.

```bash
python -m venv .venv
```

Activate using your system's command:

| System | Command |
|---|---|
| Windows PowerShell | `.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `.venv\Scripts\activate.bat` |
| Linux/macOS | `source .venv/bin/activate` |

```bash
python -m pip install -r requirements.txt
python -m pip install jupyterlab ipykernel
python -m jupyterlab
```

Select the environment containing the lab packages. Open `notebooks/lab.ipynb`. Complete the functions in `src/solution.py`; the initial public tests fail until you implement them. Enable the commented notebook calls as each function becomes available, and add your analysis code. The scaffold alone is not a completed lab.

Write narrative answers only in the existing `REPORT.md`; no file must be copied or renamed. Complete `AI_USE.md`. Keep raw input files unchanged. Save all specified result tables/figures under `outputs/`.

From the lab root:

```bash
python -m compileall -q src tests
python -m unittest discover -s tests -p 'test_public.py' -v
```

Restart the notebook kernel and run all cells top to bottom; save the executed notebook. Capture Python/package versions and reproduction commands in `outputs/environment.txt`. Passing public tests provides partial evidence, not a full grade.

Use the teacher's template to create a private repository accessible to the teacher. Follow the teacher's deadline and resubmission policy. Do not submit .venv, credentials, or caches.

If submission is performed via GitHub create a `submission` branch, commit your work, and open a pull request to `main` titled `Lab xx — your_github_username`. Submit the PR URL and full final commit SHA to the LMS. Keep `main` as the starting version; do not merge before assessment.
If submission is performed via University LMS create zip with filename `Lab xx — your_github_username.zip`. 
