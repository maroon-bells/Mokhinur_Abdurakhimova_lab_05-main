# Lab 05 — From books to auditable text evidence

**Course:** Data Exploration and Extraction, MSc Data Science  
**Marks:** 100  
**Python:** 3.12  
**Estimated work:** 3–4 hours

## Your goal

Turn two differently formatted field reports into a validated chapter dataset. Compare literal name mentions while controlling for chapter length. Preserve the source text and show exactly what the parser retained. This lab extends `Lecture book_read`; it assesses text structure and interpretation rather than repeating the statistics in previous labs.

Both supplied reports are short, fictional teaching texts. They contain misleading front-matter mentions, endnotes, markup, Unicode accents, and names inside longer words. Internet access is not required.

## Before you start

Read `FUNCTION_GUIDE.md` for exact API contracts and `SUBMISSION.md` for setup. Implement functions in `src/solution.py`. Use `notebooks/lab.ipynb` to run the analysis and produce results. Write all explanations and captions once, in the existing `REPORT.md`. The notebook contains computational scaffolding; do not duplicate the report there. Complete the separate administrative disclosure in `AI_USE.md`.

## T1 — Inspect and document the source boundaries

1. Read `data/PROVENANCE.md` and both raw UTF-8 files. Compute their byte-level SHA-256 hashes.
2. Produce `outputs/source_audit.csv` with file, layout, byte_count, sha256, and expected_chapters.
3. Identify examples of a cover/front-matter mention, an endnote mention, a bibliography mention, and an inline footnote marker. Store the examples with their file names in `outputs/boundary_examples.csv`.
4. Keep raw files unchanged. Preserve line breaks until chapter extraction is complete.

## T2 — Extract and clean chapters

1. Implement `extract_chapters` for both documented layouts. Validate the exact Roman-number sequence I–IV; a parser must fail clearly when a chapter is lost or duplicated.
2. Implement `clean_text` without removing accents or punctuation.
3. Save one row per retained chapter to `outputs/chapters.csv`: book_id, chapter, roman, title, raw_text, clean_text.
4. Demonstrate rejection of one missing-marker case and one duplicated/missing-chapter case in the notebook. Record observed exception types/messages in `outputs/parser_checks.csv`.
5. Save two before/after excerpt pairs showing the cleanup operation in `outputs/cleaning_examples.csv`. Include the raw markup spelling and its retained accented form.

## T3 — Count names and compare rates

1. Implement `count_names` and `summarize_chapters` for the four names Mira, Asad, Hajjāj, Nasr.
2. Save the long-form chapter/name summary to `outputs/chapter_summary.csv` using the documented columns. Verify that Mirabel contributes zero matches to Mira.
3. Independently check the four counts in journey Chapter I by reading the retained text. Save expected/manual and computed counts in `outputs/manual_check.csv`.
4. Build a chapter-by-name NumPy matrix for each book. Use NumPy cumulative sums along the chapter axis, then save `outputs/cumulative_mentions.csv` with book_id, chapter, name, cumulative_mentions. Confirm each final cumulative count equals that name's sum across chapters.
5. Save `outputs/book_summary.csv` with book_id, name, mentions, word_count, and mentions_per_1000_words. Count each chapter's words only once when forming a book denominator; the long summary repeats chapter metadata for each name. A book rate is total mentions / total words × 1,000, not the unweighted mean of chapter rates.
6. Rank names within each book by total mentions and compare the raw and normalized comparisons. Do not add distinct book chapter numbers into one timeline.

## T4 — Visualize the evidence

Create three Matplotlib figures in `outputs/`:

- `cumulative_mentions.png`: a separate panel for each book, consistent name colors, integer chapter ticks.
- `chapter_rates.png`: chapter-level mentions per 1,000 words for both books; label the denominator and distinguish books.
- `length_vs_periods.png`: chapter word count versus period count, distinguished by book and labeled chapter.

Use readable labels, units, legends, and stable plotting order. Refer to the saved tables rather than retyping all their numbers. A period count is not a sentence count. Name mentions are not proof of presence, importance, positive sentiment, or historical events.

## T5 — Reproduce and interpret

Complete `REPORT.md` in 200–300 words, excluding tables and captions. Its prompts are the only written questions to answer. Run the public tests and restart/run the notebook from top to bottom. Save `outputs/environment.txt` with Python/package versions and the exact reproduction commands.

See `RUBRIC.md` for assessment. Passing public tests alone does not establish correct extraction from the supplied files or justify the interpretation.
