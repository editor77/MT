# README_SETUP.md — CATSS v2 setup on a new computer

## 0) Goal

Set up CATSS v2 with MT-first token alignment and live sources:
- MT (BHSA)
- LXX (all mlxx files)
- DSS
- SP
- Peshitta

Analysis authority:
- `MT-LXX_Parallel_Manual (1).pdf`

---

## 1) Project structure

Create this folder tree:

```text
catss-v2/
  app/
    main.py
    sources.py
    formatter.py
  requirements.txt
  README.md
```

---

## 2) Python environment

Open terminal in `catss-v2` and run:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

`requirements.txt`:

```txt
streamlit>=1.38.0
pandas>=2.2.0
```

---

## 3) Source paths (must be edited in `app/sources.py`)

In `SourceConfig.default()`, set:

- MT (BHSA):  
  `C:\Users\chris\OneDrive\Documentos\AU\Index of gopher text religion biblical lxxmorph\bhsa-master`
- LXX (all mlxx):  
  `C:\Users\chris\OneDrive\Documentos\AU\Index of gopher text religion biblical lxxmorph\LXX`
- DSS:  
  `C:\Users\chris\OneDrive\Documentos\AU\Index of gopher text religion biblical lxxmorph\DSS`
- SP:  
  `C:\Users\chris\OneDrive\Documentos\AU\Index of gopher text religion biblical lxxmorph\sp-main`
- Peshitta:  
  `C:\Users\chris\OneDrive\Documentos\AU\Index of gopher text religion biblical lxxmorph\peshitta-master`

---

## 4) Required CATSS behavior

### Trigger
Use:
- `CATSS <Book> <chapter>:<verse>`
- Example: `CATSS Deut 32:8`

### Alignment policy
- MT token is the base row.
- OG/Th, DSS, SP, Syriac align by equivalence to MT token rows.
- If uncertain/not matchable, output:
  - `--` for missing token
  - `---` for missing witness stream item (where applicable)

### LXX rule
- Read all `mlxx` files in LXX folder.
- Keep Greek in Greek script (not transliteration-only).
- OG/Th shown as:
  - `OG: ...`
  - `Th: ...`

### DSS rule
- Use DBs from DSS folder (prefer `.db` sources).
- Conservative token mapping only.
- Do not force OCR fragments into MT slots.
- If uncertain: `--`.

### SP + Syriac rule
- Conservative MT-row equivalence alignment.
- If uncertain: `--`.

### CATSS Notation & Analysis must include
- Notation line
- Word differences line
- DSS status line
- Gloss line
- Exact statement:
  - `Suffixes are separated by a slash / for analysis.`

---

## 5) Run app

```powershell
streamlit run app/main.py
```

---

## 6) Smoke tests

Run these:
- `CATSS Deut 32:8`
- `CATSS Daniel 1:3`

Check:
- MT rows look correct.
- LXX is aligned (not shifted raw sequence).
- DSS is conservative (`--` where uncertain).
- SP/Syriac are equivalence-aligned to MT.

---

## 7) Troubleshooting

### Wrong MT tokens (common in BHSA stream for some refs)
Use MT sanity anchors and fallback logic (if implemented):
- If BHSA token stream fails expected anchors, fallback to MT XML corpus (`...\MT`) for that reference.

### Greek letters not displaying
Ensure:
- UTF-8 files
- terminal/editor font supports Greek

### Syriac display issues
Ensure:
- UTF-8
- font supports Syriac script

### DB not found
Verify:
- `...\DSS\dss_ulrich_ocr.db`
- `...\DSS\dss_catss_full.db`

---

## 8) Authority note

For notation and analysis decisions, follow:
- `C:\Users\chris\OneDrive\Documentos\AU\Index of gopher text religion biblical lxxmorph\MT-LXX_Parallel_Manual (1).pdf`
