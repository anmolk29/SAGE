# SAGE Change Log

All operations on 2026-11-02, run from `P:\Dev\Projects\SAGE`. Every move and copy was checked by comparing SHA-256 hashes before and after; all matched. No file was deleted.

## Folders created

`00_Master/`, `01_Research/`, `02_Project_Brief/`, `03_Assets/`, `04_Implementation/`, `05_Archive/Superseded_Drafts/`, `05_Archive/Pre_Cleanup_Originals/`, `06_Admin/`

## Copies (backups)

| # | Source | Destination | Hash check |
|---|---|---|---|
| C1 | `Documentation/SAGE_Technical_Project_Report.md` | `05_Archive/Pre_Cleanup_Originals/SAGE_Technical_Project_Report_pre-cleanup.md` | match |

## Moves (no renames)

| # | Source | Destination | Hash check |
|---|---|---|---|
| M1 | `Documentation/SAGE_Technical_Project_Report.docx` | `00_Master/SAGE_Technical_Project_Report.docx` | match |
| M2 | `Documentation/SAGE_Technical_Project_Report.pdf` | `00_Master/SAGE_Technical_Project_Report.pdf` | match |
| M3 | `Documentation/SAGE_Technical_Project_Report.md` | `00_Master/SAGE_Technical_Project_Report.md` | match (before edit E1) |
| M4 | `Documentation/SAGE_Research_Proposal.docx` | `01_Research/SAGE_Research_Proposal.docx` | match |
| M5 | `Documentation/SAGE_Literature_Review_and_Reading_Map.docx` | `01_Research/SAGE_Literature_Review_and_Reading_Map.docx` | match |
| M6 | `Documentation/SAGE_Project_Brief_and_Defense_Guide.docx` | `02_Project_Brief/SAGE_Project_Brief_and_Defense_Guide.docx` | match |
| M7 | `Documentation/sage_architecture.png` | `03_Assets/sage_architecture.png` | match |
| M8 | `Documentation/sage_policies.png` | `03_Assets/sage_policies.png` | match |
| M9 | `Documentation/sage_subjects.png` | `03_Assets/sage_subjects.png` | match |
| M10 | `Documentation/sage_workflow.png` | `03_Assets/sage_workflow.png` | match |
| M11 | `Documentation/SAGE_Project_Feasibility_and_Scope.md` | `05_Archive/Superseded_Drafts/SAGE_Project_Feasibility_and_Scope.md` | match |
| M12 | `Documentation/SAGE_Research_Problem_and_Project_Direction.md` | `05_Archive/Superseded_Drafts/SAGE_Research_Problem_and_Project_Direction.md` | match |
| M13 | `Documentation/SAGE_Industrial_Production_Line_Monitoring.md` | `05_Archive/Superseded_Drafts/SAGE_Industrial_Production_Line_Monitoring.md` | match |

## Edits

| # | File | Change | Backup |
|---|---|---|---|
| E1 | `00_Master/SAGE_Technical_Project_Report.md` | Updated the 3 image links (lines 107, 152, 341) from `sage_X.png` to `../03_Assets/sage_X.png` so the figures still render after the move. No other text changed. | C1 |

## Other

| # | Action |
|---|---|
| O1 | Removed the now-empty `Documentation/` folder (`rmdir`, which works only on empty folders). |
| O2 | Created `04_Implementation/README.md` (placeholder; the folder had no implementation files to hold). |
| O3 | Created `06_Admin/SAGE_File_Audit.xlsx`, `SAGE_Cleanup_Report.md`, `SAGE_Change_Log.md`, `SAGE_Deletion_Review.md`. |

## Merges

None. No content was merged into any canonical document. Candidate material is listed in `SAGE_Cleanup_Report.md` §3 for your approval.

## How to undo (round 1)

Move each file in the Moves table back to its Source path, then copy `C1` back over the master MD.

---

# Round 2: changes made after your decisions (2026-11-02)

Your decisions: (1) remove the Proposal, Literature Review and Brief; (2) skip the PDF re-export; (3) skip the missing Professor Review source; (4) keep `sage_workflow.png` as a spare; (6) the IEEE manuscript is required; (7) simulation is acceptable for the assessment; (8) merge as I judge suitable.

## Backups

| # | Source | Destination | Hash check |
|---|---|---|---|
| C2 | `00_Master/SAGE_Technical_Project_Report.docx` (v1.0) | `05_Archive/Pre_Cleanup_Originals/SAGE_Technical_Project_Report_pre-merge.docx` | match (`c36abc18…`) |
| C3 | `00_Master/SAGE_Technical_Project_Report.md` (v1.0, links fixed) | `05_Archive/Pre_Cleanup_Originals/SAGE_Technical_Project_Report_pre-merge.md` | match (`675f8cc6…`) |

## Merges into the master report (MD and DOCX; v1.0 → v1.1)

The same content was written to both files by one script. Every MD line was then checked against the DOCX text, and the DOCX passes OOXML schema validation (445 → 569 paragraphs). Five existing lines were changed; everything else is an addition.

| # | Report location | Change | Source |
|---|---|---|---|
| R1 | Title / Version | 1.0 → 1.1 | — |
| R2 | Revision note | Added project origin (physical active vision → adaptive processing) and a v1.1 note | Feasibility §2, §9 |
| R3 | §1.3 → new "Working hypotheses" | H1–H3 and a note that a negative result is acceptable | Proposal §3; Industrial §6.3 |
| R4 | §1.5 objective 8 | Now includes "an IEEE-structured research manuscript" | Your decision 6 |
| R5 | New §4.2 Scheduling complexity | F/k; scheduling complexity kept separate from image-processing cost | Feasibility §4 |
| R6 | New §5.5 Candidate event categories (provisional) | 5 conveyor event candidates, labelled as not final | Industrial §2 |
| R7 | New §5.6 Data rights and handling | Licence/use checks, no face recognition, retention, provenance | Proposal §9; Industrial §8.2 |
| R8 | §7.1 | Classical pipeline steps; compare two activity methods where feasible | Feasibility §5 |
| R9 | §8.3 | "paired bootstrap intervals if practical" | Proposal §8 |
| R10 | New §8.5 Research manuscript | Required deliverable plus IEEE outline | Feasibility §8; your decision 6 |
| R11 | §13 | New "Evidence and supported claims" table; economic-claims bullet | Research Problem §3.5; Industrial §7 |
| R12 | §14 Decision register | "Semester implementation" now "Frozen — simulation confirmed acceptable for assessment"; new row "Research manuscript … Required" | Your decisions 6, 7 |
| R13 | Appendix B | Lists the three removed DOCX files as consolidated sources | — |
| R14 | New Appendix C — Literature reading map | Sources [1]–[6] with full citations, synthesis, unverified leads, search plan, reading-group questions | Literature Review DOCX; Research Problem §1 |
| R15 | New Appendix D — Responses to supervisor review questions | The Brief's four Q&As; "clips" → "industrial footage", "video-only" → "video-activity-adaptive", "paper" → "manuscript" | Brief |

`00_Master/SAGE_Technical_Project_Report.docx` was replaced by the merged version. The PDF was **not** changed (decision 2), so it is still v1.0.

## Removals (Recycle Bin, recoverable)

| # | File | SHA-256 (first 16) | Unique content now in |
|---|---|---|---|
| X1 | `01_Research/SAGE_Research_Proposal.docx` | `f3a2266b867bbbc4` | Report §1.3, §5.6, §8.3 |
| X2 | `01_Research/SAGE_Literature_Review_and_Reading_Map.docx` | `2433bcc73e59a240` | Report Appendix C |
| X3 | `02_Project_Brief/SAGE_Project_Brief_and_Defense_Guide.docx` | `a277e54e5e2a6831` | Report Appendix D |
| X4 | Removed the empty `01_Research/` and `02_Project_Brief/` folders | — | — |

To restore one of these, open the Recycle Bin, right-click the file and choose **Restore**. It goes back to its `01_Research/` or `02_Project_Brief/` path.

## Admin updates

`SAGE_File_Audit.xlsx` was regenerated, and `SAGE_Cleanup_Report.md` and `SAGE_Deletion_Review.md` were rewritten to match.

---

# Round 3: detector comparison made required (2026-11-02)

Your decision: the classical-vs-pretrained comparison is a **required** part of the evaluation.

## Backups

| # | Source | Destination |
|---|---|---|
| C4 | `00_Master/SAGE_Technical_Project_Report.md` (v1.1) | `05_Archive/Pre_Cleanup_Originals/SAGE_Technical_Project_Report_v1.1.md` (hash match) |
| C5 | `00_Master/SAGE_Technical_Project_Report.docx` (v1.1) | `05_Archive/Pre_Cleanup_Originals/SAGE_Technical_Project_Report_v1.1.docx` (hash match) |

## Report edits (MD and DOCX; v1.1 → v1.2)

The DOCX passes OOXML validation (569 → 579 paragraphs), and the MD/DOCX text parity check found 0 mismatches.

| # | Location | Change |
|---|---|---|
| D1 | Version | 1.1 → 1.2; revision note mentions the v1.2 change |
| D2 | §1.5 objective 3 | Adds "compare classical and pretrained-model detection on the same footage" |
| D3 | §7.1 | "if justified … a pretrained model" → "at least one pretrained model … evaluate them comparatively (§7.3)"; "optional pretrained object detector" → "a pretrained model … selected during dataset validation" |
| D4 | New §7.3 Classical vs. pretrained detection comparison | Required. Same footage, events, ROI and matching rules; detection and cost metrics per detector; no training from scratch; model and version recorded; model choice provisional. Whether the policy comparison is repeated per detector is left to protocol design. |
| D5 | §14 Decision register | New row: "Detector comparison: Classical OpenCV pipeline vs. pretrained model, Required; specific model open" |

## Changes in the folder that were not made by me

From about 03:56 onward, another process or session wrote these files. I have not modified, moved or audited any of them:

- `04_Implementation/`: `sage/` package, `app.py`, `tests/`, `docs/` (incl. `IEEE_MANUSCRIPT_DRAFT.md`), `pyproject.toml`, `requirements.txt`, `.gitignore`, a new `README.md`. My placeholder README was kept as `README.before_sync_2026-11-02.md`.
- `.venv/` at the project root.
- `Unconfirmed 959113.crdownload` at the project root, an unfinished browser download (~612 MB and still growing at 04:11).
