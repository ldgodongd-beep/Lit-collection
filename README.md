# Lit-collection

Literature digests (Chinese–English) of new papers in 16 human, economic and urban geography journals, organised by journal and by research topic.

- `digests/YYYY-MM-DD.md`: the digest for that run
- `digests/YYYY-MM-DD.json`: structured data for the same papers
- `scripts/fetch.py`: pulls recent articles from the Crossref API
- `scripts/build.py`: builds the Markdown digest from the fetched data and the translations
