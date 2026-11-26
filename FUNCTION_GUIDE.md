# Lab 05 — Function contracts

Implement exactly these four APIs in `src/solution.py`. Functions must work on other valid inputs, must not mutate caller inputs, and must not hard-code fixture answers. Return new objects. Raise `ValueError` for invalid conditions specified below; a non-string text or name may also raise `TypeError`.

## `extract_chapters(text, layout, expected_numbers)`

Return a list of dictionaries, in source order, each with exactly `chapter` (1-based integer), `roman` (Roman-number string), `title` (str), and `text` (unmodified retained prose apart from outer whitespace trimming). `layout` is `travel` or `survey`. `expected_numbers` is a nonempty sequence of unique, nonempty Roman-number strings; compare detected headings with that sequence exactly. Only Roman numerals formed from I,V,X,L,C,D,M are valid in the sequence.

1. Normalize CRLF/CR line endings to LF. Require exactly one full-line start marker matching `*** START OF ... ***` and one matching `*** END OF ... ***`, in that order; optional surrounding spaces/tabs are allowed. Retain only text between them. Missing, duplicate, or reversed markers raise `ValueError`.
2. For `travel`, begin after the standalone `NARRATIVE.` line. Recognize full-line `CHAPTER I.` and `CHAP. II.` headings, with spaces/tabs around tokens. A title is the first nonempty paragraph after a chapter heading. The prose starts after the first blank line following that title. A missing title/prose separator or empty prose is invalid. Collapse title whitespace to single spaces, keeping spelling/punctuation.
3. For `survey`, begin at the standalone `I. INTRODUCTION` line. Stop before the standalone `BIBLIOGRAPHY OF CHIEF WORKS CITED.` line if it exists. Headings have a Roman number followed by `. ` and an uppercase title, with an optional trailing period and optional numeric footnote reference, e.g. `II. THE RIVER ARCHIVE.[4]`. The title belongs to the heading; remove its Roman prefix, optional terminal period, and footnote reference. Keep the prose after it. Restrict heading titles to uppercase ASCII letters and spaces, as in the supplied fixture.
4. In either layout, stop each chapter's prose at the first standalone `FOOTNOTE:`, `FOOTNOTES:`, `NOTES`, or `END OF THE FIRST VOLUME.` line if present. Do not include those lines or text after them. Heading lines and titles are not prose.
5. Reject an unknown layout, missing required narrative/introduction line, unexpected/missing/duplicate chapters, or any empty retained title/prose. Do not run `clean_text` inside this function: retain markup and numeric callouts for an auditable intermediate result.

## `clean_text(text)`

Return a string. Remove all `_` and `~` markup delimiters and inline numeric footnote references of the exact form `[12]` (one or more digits). Normalize Unicode to NFC. Collapse all runs of whitespace to one ASCII space and trim outer whitespace. Retain accents, case, punctuation, digits outside note references, and all other text. Thus `Haj_j_āj[7]` becomes `Hajjāj`; decomposed accents normalize to the same accented spelling. Do not transliterate names.

## `count_names(chapters, names)`

`chapters` is a one-dimensional sequence of already-cleaned chapter strings. `names` is a nonempty sequence of nonempty literal names. Normalize names to NFC and collapse their internal whitespace; reject duplicate names ignoring case after this normalization. Reject blank names and non-string entries.

Return an integer NumPy array with shape `(len(chapters), len(names))`, preserving both supplied orders. Empty chapters are allowed and yield zero counts; an empty chapter sequence yields shape `(0, len(names))`. Match names case-insensitively, accepting any intervening whitespace between multiword name components. Use Unicode word boundaries: a match cannot have a word character immediately before or after it. Treat regex metacharacters literally. Mira does not match Mirabel; `Mira's` matches Mira. Hyphens and apostrophes are not word characters under this rule. This is literal matching, not entity resolution, sentiment analysis, or alias recognition.

## `summarize_chapters(book_id, records, names)`

`book_id` is a nonempty string. `records` is a nonempty list in the shape returned by `extract_chapters`. Require chapter values to equal 1,2,... in order and each title/prose to be nonempty. Clean each chapter with `clean_text`; reject a chapter that becomes empty. Use `count_names` for the supplied names.

Return a pandas DataFrame in chapter-major, then supplied-name order, with exactly these columns:

`book_id, chapter, title, name, mentions, word_count, char_count, period_count, mentions_per_1000_words`

- `name` retains the original supplied name label; `mentions` is an integer.
- Define a word as a Unicode `\w+` token optionally joined to further such tokens by one apostrophe (`'` or `’`) or hyphen (`-`). The exact regex is `\w+(?:['’-]\w+)*`. Numerals and underscore-containing tokens follow this stated operational definition; underscores have already been removed by cleaning.
- `word_count` is the number of these tokens. Reject zero-word chapters.
- `char_count = len(cleaned_text)`, including spaces and punctuation.
- `period_count = cleaned_text.count('.')`, not a sentence estimate.
- `mentions_per_1000_words = 1000 * mentions / word_count`.

A chapter's length metadata repeats for each name. Do not sum those repeated lengths when computing book totals. Do not average chapter rates without weighting by chapter word counts.
