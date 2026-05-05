# bib-tidy

> Opinionated BibTeX bibliography formatter and deduplicator with DOI resolution and citation key normalization.

---

## Installation

```bash
pip install bib-tidy
```

Or with [pipx](https://pypa.github.io/pipx/) for isolated CLI usage:

```bash
pipx install bib-tidy
```

---

## Usage

```bash
# Format and deduplicate a .bib file in place
bib-tidy references.bib

# Resolve DOIs and normalize citation keys, write to a new file
bib-tidy references.bib --resolve-doi --normalize-keys --output clean.bib

# Preview changes without writing (dry run)
bib-tidy references.bib --dry-run
```

You can also use it as a Python library:

```python
from bibtidy import BibTidy

tidy = BibTidy("references.bib")
tidy.deduplicate()
tidy.normalize_keys()
tidy.resolve_dois()
tidy.save("clean.bib")
```

---

## Features

- **Formatting** — consistent field ordering, indentation, and quoting style
- **Deduplication** — detects duplicate entries by DOI, title, or citation key
- **DOI resolution** — fetches and fills missing metadata via the CrossRef API
- **Key normalization** — generates clean `AuthorYearTitle` citation keys automatically

---

## License

MIT © bib-tidy contributors