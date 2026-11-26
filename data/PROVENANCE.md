# Data provenance

`journey.txt` and `survey.txt` are fictional teaching texts written for this lab. They are not passages from real records. Names are used only as text-analysis examples. No claims about real people or events follow from these fixtures.

The formats imitate features demonstrated in `Lecture read_book`: outer start/end markers, front matter, mixed chapter-heading formats, typographic markup, accented names, inline numeric notes, excluded endnotes, and a bibliography. The texts are intentionally short so students can inspect and audit every retained chapter. The Gutenberg texts linked in the lecture remain optional external examples; internet access is not needed here.

The synthetic texts may be reused and modified for educational purposes, subject to the consent of the author, Jamshid Yakhshilikov. Keep the distributed inputs unchanged during assessment. Record their SHA-256 hashes before analysis. The expected chapter sequence for both fixtures is I, II, III, IV.

| File | Parser layout | Analysis unit | Tracked literal names |
|---|---|---|---|
| journey.txt | travel | One narrative chapter | Mira; Asad; Hajjāj; Nasr |
| survey.txt | survey | One narrative chapter | Mira; Asad; Hajjāj; Nasr |

The decomposed accented spelling and underscore/tilde markup are deliberate. Both books contain mentions outside the retained narrative. Counting the complete file gives a different result.
