"""Behavioral examples; supplied-file extraction and interpretation are assessed separately."""

import unittest
from pathlib import Path

import numpy as np
from src import solution as s


class PublicTests(unittest.TestCase):
    def travel(self, text="Mira wrote. Asad read."):
        return (
            "Cover Mira\n*** START OF TEST ***\nCONTENTS\nCHAPTER I. — page 1\n"
            "NARRATIVE.\nCHAPTER I.\nFIRST PLACE\n\n" + text + "\nFOOTNOTES:\nMira in an excluded note.\n*** END OF TEST ***\nMira footer"
        )

    def test_extract_travel_excludes_front_matter_notes(self):
        rows = s.extract_chapters(self.travel(), "travel", ["I"])
        self.assertEqual(len(rows), 1)
        self.assertEqual(set(rows[0]), {"chapter", "roman", "title", "text"})
        self.assertEqual(rows[0], {"chapter": 1, "roman": "I", "title": "FIRST PLACE", "text": "Mira wrote. Asad read."})

    def test_extract_preserves_markup_for_audit(self):
        result = s.extract_chapters(self.travel("M_i_ra wrote.[2]"), "travel", ["I"])
        self.assertEqual(result[0]["text"], "M_i_ra wrote.[2]")

    def test_survey_heading_and_bibliography(self):
        text = "*** START OF TEST ***\nPreface Mira\nI. INTRODUCTION\nMira wrote.\nII. THE SECOND ARCHIVE.[3]\nNasr read.\nBIBLIOGRAPHY OF CHIEF WORKS CITED.\nMira excluded.\n*** END OF TEST ***"
        rows = s.extract_chapters(text, "survey", ["I", "II"])
        self.assertEqual([r["title"] for r in rows], ["INTRODUCTION", "THE SECOND ARCHIVE"])
        self.assertEqual(rows[1]["text"], "Nasr read.")

    def test_line_endings(self):
        a = s.extract_chapters(self.travel(), "travel", ["I"])
        b = s.extract_chapters(self.travel().replace("\n", "\r\n"), "travel", ["I"])
        self.assertEqual(a, b)

    def test_invalid_structure_rejected(self):
        invalid = [
            self.travel().replace("*** END OF TEST ***", ""),
            self.travel() + "\n*** START OF DUPLICATE ***",
            self.travel().replace("NARRATIVE.", "PREFACE."),
            self.travel().replace("CHAPTER I.\nFIRST", "CHAPTER II.\nFIRST"),
            self.travel().replace("FIRST PLACE\n\n", "FIRST PLACE\n"),
        ]
        for text in invalid:
            with self.subTest(text=text), self.assertRaises(ValueError):
                s.extract_chapters(text, "travel", ["I"])

    def test_expected_sequence_and_layout_checks(self):
        for expected in ([], ["I", "I"], ["one"]):
            with self.assertRaises(ValueError):
                s.extract_chapters(self.travel(), "travel", expected)
        with self.assertRaises(ValueError):
            s.extract_chapters(self.travel(), "other", ["I"])

    def test_clean_unicode_preserves_accents_punctuation(self):
        self.assertEqual(s.clean_text("  Haj_j_a\u0304j[12]\n A~sad 2.5. [x] "), "Hajjāj Asad 2.5. [x]")
        self.assertEqual(s.clean_text(""), "")

    def test_names_whole_literal_case_and_order(self):
        result = s.count_names(["Mira MIRA Mirabel Mira's. Nasr.", "Nasr"], ["Nasr", "Mira"])
        np.testing.assert_array_equal(result, [[1, 3], [1, 0]])
        self.assertEqual(result.shape, (2, 2))
        self.assertTrue(np.issubdtype(result.dtype, np.integer))

    def test_names_multiword_and_metacharacters(self):
        result = s.count_names(["Runjeet   Sing met A+B. AAB did not meet Runjeet Singleton."], ["A+B", "Runjeet Sing"])
        np.testing.assert_array_equal(result, [[1, 1]])

    def test_empty_chapters_and_invalid_names(self):
        self.assertEqual(s.count_names([], ["Mira"]).shape, (0, 1))
        np.testing.assert_array_equal(s.count_names([""], ["Mira"]), [[0]])
        for names in ([], [" "], ["Mira", "MIRA"], ["Hajjāj", "Hajja\u0304j"]):
            with self.assertRaises(ValueError):
                s.count_names(["Mira"], names)

    def test_summary_long_form_and_word_rule(self):
        records = [{"chapter": 1, "roman": "I", "title": "INTRODUCTION", "text": "Mira's field-note: Mira. 2.5."}]
        result = s.summarize_chapters("A", records, ["Mira", "Nasr"])
        self.assertEqual(list(result.columns), ["book_id", "chapter", "title", "name", "mentions", "word_count", "char_count", "period_count", "mentions_per_1000_words"])
        self.assertEqual(result["mentions"].tolist(), [2, 0])
        self.assertEqual(result["word_count"].tolist(), [5, 5])
        self.assertEqual(result["period_count"].tolist(), [3, 3])
        self.assertAlmostEqual(result.iloc[0]["mentions_per_1000_words"], 400.0)
        self.assertEqual(result.iloc[0]["char_count"], len(records[0]["text"]))
        self.assertEqual(records[0]["text"], "Mira's field-note: Mira. 2.5.")

    def test_summary_validation(self):
        with self.assertRaises(ValueError):
            s.summarize_chapters("A", [], ["Mira"])
        rec = [{"chapter": 2, "roman": "II", "title": "TITLE", "text": "Mira"}]
        with self.assertRaises(ValueError):
            s.summarize_chapters("A", rec, ["Mira"])
        rec = [{"chapter": 1, "roman": "I", "title": "TITLE", "text": "..."}]
        with self.assertRaises(ValueError):
            s.summarize_chapters("A", rec, ["Mira"])

    def test_supplied_sources_have_expected_structures(self):
        root = Path(__file__).resolve().parents[1]
        for book, layout in [("journey", "travel"), ("survey", "survey")]:
            rows = s.extract_chapters((root / "data" / f"{book}.txt").read_text(encoding="utf-8"), layout, ["I", "II", "III", "IV"])
            self.assertEqual(len(rows), 4)
            self.assertNotIn("FOOTNOTES:", "\n".join(r["text"] for r in rows))
            self.assertNotIn("excluded bibliography", "\n".join(r["text"] for r in rows))


if __name__ == "__main__":
    unittest.main()
