"""Auditable chapter extraction and literal-name analysis for Lab 05."""
import re
import unicodedata
import numpy as np
import pandas as pd

_ROMAN = re.compile(r"^[IVXLCDM]+$")
_START_END = re.compile(r"^[ \t]*\*\*\* (START|END) OF .+? \*\*\*[ \t]*$", re.M)
_STOP = re.compile(r"^(?:FOOTNOTE:|FOOTNOTES:|NOTES|END OF THE FIRST VOLUME\.)[ \t]*$", re.I)


def extract_chapters(text, layout, expected_numbers):
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if layout not in {"travel", "survey"}:
        raise ValueError(f"unknown layout: {layout!r}")
    if not isinstance(expected_numbers, (list, tuple)) or not expected_numbers:
        raise ValueError("expected_numbers must be a nonempty sequence")
    if any(not isinstance(x, str) or not x or not _ROMAN.fullmatch(x) for x in expected_numbers):
        raise ValueError("expected_numbers must contain valid nonempty Roman numerals")
    if len(set(expected_numbers)) != len(expected_numbers):
        raise ValueError("expected_numbers must be unique")
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    markers = list(_START_END.finditer(text))
    starts = [m for m in markers if m.group(1) == 'START']
    ends = [m for m in markers if m.group(1) == 'END']
    if len(starts) != 1 or len(ends) != 1 or starts[0].start() >= ends[0].start():
        raise ValueError("require exactly one ordered full-line START and END marker")
    body = text[starts[0].end():ends[0].start()]
    lines = body.splitlines()
    if layout == 'travel':
        anchors = [i for i, line in enumerate(lines) if line.strip() == 'NARRATIVE.']
        if len(anchors) != 1:
            raise ValueError("travel layout requires one standalone NARRATIVE. line")
        head_re = re.compile(r"^[ \t]*(?:CHAPTER|CHAP\.)[ \t]+([IVXLCDM]+)\.[ \t]*$", re.I)
        found = []
        for i in range(anchors[0] + 1, len(lines)):
            m = head_re.fullmatch(lines[i])
            if m:
                roman = m.group(1).upper()
                j = i + 1
                while j < len(lines) and not lines[j].strip(): j += 1
                if j >= len(lines): raise ValueError(f"chapter {roman} has no title")
                title = ' '.join(lines[j].split())
                k = j + 1
                if k >= len(lines) or lines[k].strip():
                    raise ValueError(f"chapter {roman} is missing title/prose separator")
                p = k
                while p < len(lines) and not lines[p].strip(): p += 1
                if p >= len(lines):
                    raise ValueError(f"chapter {roman} has empty prose")
                end = p
                while end < len(lines) and not _STOP.fullmatch(lines[end].strip()) and not head_re.fullmatch(lines[end]): end += 1
                prose = '\n'.join(lines[p:end]).strip()
                found.append((roman, title, prose))
    else:
        anchors = [i for i, line in enumerate(lines) if line.strip() == 'I. INTRODUCTION']
        if len(anchors) != 1:
            raise ValueError("survey layout requires one standalone I. INTRODUCTION line")
        head_re = re.compile(r"^[ \t]*([IVXLCDM]+)\. ([A-Z ]+?)(?:\.)?(?:\[\d+\])?[ \t]*$")
        found = []
        for i in range(anchors[0], len(lines)):
            if lines[i].strip() == 'BIBLIOGRAPHY OF CHIEF WORKS CITED.': break
            m = head_re.fullmatch(lines[i])
            if not m: continue
            roman, title = m.group(1), m.group(2).strip()
            p = i + 1
            end = p
            while end < len(lines) and not _STOP.fullmatch(lines[end].strip()) and lines[end].strip() != 'BIBLIOGRAPHY OF CHIEF WORKS CITED.' and not head_re.fullmatch(lines[end]): end += 1
            prose = '\n'.join(lines[p:end]).strip()
            found.append((roman, title, prose))
    detected = [x[0] for x in found]
    if detected != list(expected_numbers):
        raise ValueError(f"chapter sequence mismatch: expected {list(expected_numbers)!r}, detected {detected!r}")
    records = []
    for n, (roman, title, prose) in enumerate(found, 1):
        if not title or not prose:
            raise ValueError(f"chapter {roman} has empty retained title or prose")
        records.append({'chapter': n, 'roman': roman, 'title': title, 'text': prose})
    return records


def clean_text(text):
    if not isinstance(text, str): raise TypeError("text must be a string")
    text = unicodedata.normalize('NFC', text)
    text = re.sub(r'\[\d+\]', '', text)
    text = text.replace('_', '').replace('~', '')
    return re.sub(r'\s+', ' ', text).strip()


def _validate_names(names):
    if not isinstance(names, (list, tuple)) or not names:
        raise ValueError("names must be a nonempty sequence")
    normalized = []
    for name in names:
        if not isinstance(name, str): raise TypeError("each name must be a string")
        n = re.sub(r'\s+', ' ', unicodedata.normalize('NFC', name)).strip()
        if not n: raise ValueError("names cannot be blank")
        normalized.append(n)
    if len({n.casefold() for n in normalized}) != len(normalized):
        raise ValueError("names must be unique ignoring case after normalization")
    return normalized


def count_names(chapters, names):
    if isinstance(chapters, (str, bytes)): raise TypeError("chapters must be a sequence of strings")
    norm_names = _validate_names(names)
    if any(not isinstance(c, str) for c in chapters): raise TypeError("each chapter must be a string")
    matrix = np.zeros((len(chapters), len(norm_names)), dtype=int)
    for j, name in enumerate(norm_names):
        parts = name.split()
        pattern = r'(?<!\w)' + r'\s+'.join(re.escape(p) for p in parts) + r'(?!\w)'
        rx = re.compile(pattern, re.IGNORECASE)
        for i, chapter in enumerate(chapters):
            matrix[i, j] = len(rx.findall(unicodedata.normalize('NFC', chapter)))
    return matrix


def summarize_chapters(book_id, records, names):
    if not isinstance(book_id, str) or not book_id.strip(): raise ValueError("book_id must be a nonempty string")
    if not isinstance(records, list) or not records: raise ValueError("records must be a nonempty list")
    _validate_names(names)
    for i, rec in enumerate(records, 1):
        if rec.get('chapter') != i: raise ValueError("chapter values must be 1,2,... in order")
        if not isinstance(rec.get('title'), str) or not rec['title'].strip() or not isinstance(rec.get('text'), str) or not rec['text'].strip():
            raise ValueError(f"chapter {i} requires nonempty title and prose")
    cleaned = [clean_text(r['text']) for r in records]
    if any(not x for x in cleaned): raise ValueError("chapter becomes empty after cleaning")
    word_rx = re.compile(r"\w+(?:['’-]\w+)*", re.UNICODE)
    matrix = count_names(cleaned, names)
    rows = []
    for i, (rec, txt) in enumerate(zip(records, cleaned)):
        wc = len(word_rx.findall(txt))
        if wc == 0: raise ValueError(f"chapter {i+1} has zero words")
        for j, name in enumerate(names):
            mentions = int(matrix[i, j])
            rows.append({'book_id': book_id, 'chapter': i+1, 'title': rec['title'], 'name': name,
                         'mentions': mentions, 'word_count': wc, 'char_count': len(txt),
                         'period_count': txt.count('.'), 'mentions_per_1000_words': 1000*mentions/wc})
    return pd.DataFrame(rows, columns=['book_id','chapter','title','name','mentions','word_count','char_count','period_count','mentions_per_1000_words'])
