# v19.5 - Elsevier / Neural Networks LaTeX formatting freeze

V19.5 changes submission formatting only. Scientific claims, experimental results, analyses, conclusions, abstract wording, keywords, figures, and numerical values are unchanged from the v19.4 scientific freeze.

Changes:
- Converted the manuscript from the generic `article` class to Elsevier `elsarticle` using `preprint,12pt,authoryear` and `\journal{Neural Networks}`.
- Rebuilt title, author, affiliation, corresponding-author email, abstract, and keywords with `elsarticle` front matter.
- Flattened all figure references and the Editorial Manager LaTeX source archive so every source file is at one folder level.
- Adjusted table typography and one displayed equation line break only to fit the narrower Elsevier preprint layout; no table values or equation content changed.
- Added `xurl` for robust URL line breaking.

The manuscript PDF is 43 pages in Elsevier preprint layout.
