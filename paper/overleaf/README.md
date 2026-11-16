# SAGE IEEE conference paper source

This folder contains the Overleaf-ready LaTeX source for the SAGE study:

- `main.tex` — IEEE conference paper source using `IEEEtran` and the standard `cite` package.
- `references.bib` — 20 DOI-bearing references.
- `SAGE_IEEE_Overleaf.zip` — the same source files packaged for Overleaf's **New Project → Upload Project** flow.

## Compile on Overleaf

1. Upload `SAGE_IEEE_Overleaf.zip` as a new Overleaf project.
2. Set `main.tex` as the main document if Overleaf does not select it automatically.
3. Use pdfLaTeX and BibTeX (the default Overleaf build sequence for this template).
4. Replace the `\SAGEaffiliation` definition near the top of `main.tex` with the department, institution, city, and country for the authors before sharing or submitting the paper.
5. Check the target conference's page limit, anonymization rules, and author instructions. This source follows the IEEE conference class and does not claim acceptance or compliance with any particular conference's additional rules.

The affiliation is intentionally marked for replacement because the project team has not supplied those details yet. No external data files are needed to compile the paper. The exact article-level Scopus records were not individually checked; see `../../docs/research/SCOPUS_SOURCE_AUDIT.md` for the venue/year coverage audit and its limits.

The requested starter is the [IEEE Conference Template on Overleaf](https://www.overleaf.com/latex/templates/ieee-conference-template/grfzhhncsfqn).
