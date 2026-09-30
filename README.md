# Disclosure Lens

Analyzes where a company places important information in a disclosure and how it is worded:
information order, hedging, and tone vs. financial facts.

## Run it
```
python analyze.py data/sample_release.txt
```

## Test it
```
pip install pytest
pytest
```

## Project layout
- `disclosure_lens/preprocess.py`: paragraphs, sentences, positions
- `disclosure_lens/classify.py`: financial direction + materiality (rule-based, needs validation)
- `disclosure_lens/hedges.py`: tiered hedge lexicon, density, modal intensity
- `disclosure_lens/tone.py`: tone score (placeholder lexicon, replace with Loughran-McDonald)
- `disclosure_lens/metrics.py`: headline metrics
- `analyze.py`: prints a text version of the Disclosure Map and Profile

## Known limitations (to fix next)
- Sentence splitter never splits after an abbreviation (e.g. "...sales of $1.2 bn. The market..." will not split); fine for a first version
- Tone word list is a tiny placeholder
- "Expenses declined" is good news but is read as negative
- Rules are unvalidated until you hand-label ~200 sentences
