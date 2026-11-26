# Lab 05 report

Course ID: Data Exploration and Extraction
Word count: 299

## 1. Source and extraction evidence (T1–T2)

A chapter record is one numbered narrative unit: title and retained prose. Travel extraction starts at `NARRATIVE.` and excludes front matter, endnotes and the volume ending. Survey extraction starts at `I. INTRODUCTION` and stops before the bibliography. Raw callouts remain auditable but are removed during cleaning ([boundary_examples.csv](outputs/boundary_examples.csv)). Newlines matter because blank lines separate titles from prose and headings define boundaries. Hashes are in [source_audit.csv](outputs/source_audit.csv). The parser rejected a missing end marker and detected `I, II, II, IV` ([parser_checks.csv](outputs/parser_checks.csv)).

## 2. Cleaning and measurement choices (T2–T3)

Cleaning removes `_`, `~` and numeric references, normalizes Unicode to NFC, and collapses whitespace. Accents and punctuation remain: `Haj_j_āj` becomes `Hajjāj`, as does the decomposed spelling ([cleaning_examples.csv](outputs/cleaning_examples.csv)). Case-insensitive literal matching with Unicode word boundaries excludes Mirabel from Mira; apostrophes and hyphens delimit names. Counts are textual occurrences, not resolved identities.

## 3. Findings and denominator check (T3)

Journey Chapter I counts were manually verified: Mira 4, Asad 1, Hajjāj 1, Nasr 1 ([manual_check.csv](outputs/manual_check.csv)). Cumulative totals equal matrix column sums ([cumulative_mentions.csv](outputs/cumulative_mentions.csv)). Journey contains 151 words and survey 132; each chapter's denominator is counted once. Journey ranks Mira first (9 mentions; 59.6 per 1,000 words), while survey ranks Hajjāj first (7; 53.0 per 1,000; [book_summary.csv](outputs/book_summary.csv)).

## 4. Figures and limits (T4)

Figures show cumulative mentions, chapter rates and chapter length versus periods ([cumulative_mentions.png](outputs/cumulative_mentions.png); [chapter_rates.png](outputs/chapter_rates.png); [length_vs_periods.png](outputs/length_vs_periods.png)). Periods in decimals and abbreviations are not sentence counts. Mentions do not prove presence, importance or historical truth. Literal matching cannot resolve aliases or unnormalized variants.

## 5. Reproduction (T5)

See [environment.txt](outputs/environment.txt). All 13 public tests passed; the notebook ran top to bottom. Runtime was Python 3.13.5, not 3.12; rerun under 3.12 if required.
