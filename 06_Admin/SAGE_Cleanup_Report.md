# SAGE Cleanup Report

**Date:** 2026-11-02 (round 1: audit and reorganisation; round 2: your decisions applied)
**Companion files:** `SAGE_File_Audit.xlsx`, `SAGE_Change_Log.md`, `SAGE_Deletion_Review.md`

**Summary.** No byte-identical duplicates were found. The project now has a single master document: **Technical Project Report v1.2** (MD + DOCX), which absorbs the unique content of the three earlier drafts and of the Proposal, Literature Review and Brief. At your request those three DOCX files were sent to the Recycle Bin, so they can still be restored. Nothing has been permanently deleted.

---

## 1. Files retained as active

| Document | Location | Notes |
|---|---|---|
| Technical Project Report v1.2 (MD) | `00_Master/SAGE_Technical_Project_Report.md` | Canonical source text. |
| Technical Project Report v1.2 (DOCX) | `00_Master/SAGE_Technical_Project_Report.docx` | Same content as the MD; passes OOXML validation; 3 embedded figures. |
| Technical Project Report (PDF) | `00_Master/SAGE_Technical_Project_Report.pdf` | **Still v1.0** and missing top-level headings. Re-export was skipped at your request, so it does not match v1.2. |
| Figures 1–3 | `03_Assets/sage_architecture.png`, `sage_policies.png`, `sage_subjects.png` | Used by the report. |
| Workflow diagram | `03_Assets/sage_workflow.png` | Kept as a spare (your decision). |

## 2. Confirmed duplicates

None at the file level (13 distinct SHA-256 hashes). The report MD/DOCX/PDF are three formats of one document. The PNGs embedded in the DOCX match the files in `03_Assets/`. None of these files from your list was in the folder: `SAGE_Research_Problem_and_Professor_Review.md`, `(1)` copies, or pasted-text files.

> **Noticed in passing:** your Windows Recycle Bin already held `SAGE_Technical_Project_Report (1)` and `SAGE_Study_Protocol_and_Two_Week_Plan` from before this cleanup. I did not touch or inspect them. If the Study Protocol has anything you still need, restore it before emptying the bin.

## 3. Files merged and where their content went

| Source | Content | Now in report v1.1 |
|---|---|---|
| Research Proposal (removed) | Hypotheses H1–H3 | §1.3 "Working hypotheses" |
| | Privacy, ethics and data handling | §5.6 |
| | Paired bootstrap intervals | §8.3 |
| Literature Review and Reading Map (removed) | Sources [1]–[6], relevance and verification notes, synthesis, search plan, reading-group questions, full citations | Appendix C |
| Project Brief and Defense Guide (removed) | Answers to the supervisor's review questions, incl. "useful negative result" | Appendix D |
| Feasibility and Scope (archived) | Scheduling complexity | §4.2 |
| | Classical CV steps; compare two activity methods | §7.1 |
| | IEEE manuscript structure | §8.5 |
| | Project origin (physical active vision) | Revision note |
| Research Problem and Project Direction (archived) | Evidence-vs-claims table | §13 |
| | Literature leads (Vaisenberg 2009; Adaptive Frame Sampling 2026; IEEE 9839465) | Appendix C, marked unverified |
| Industrial Production-Line Monitoring (archived) | Candidate conveyor events (marked provisional) | §5.5 |
| | Economic-claim limit | §13 |
| | Separate use permissions (repo/demo/publication) | §5.6 |
| Your decisions | Manuscript required; simulation acceptable | §1.5, §8.5, §14 register |

**Deliberately not merged:**
- Acceptance-criteria checklists: largely covered by report §10 and §15. They remain in the archived Feasibility draft and are worth turning into the implementation plan later.
- Option A/B contribution framing: §13 already states the narrower contribution.
- Timelines ("10 days", "two weeks"): excluded per your instruction.
- Footage through industrial contacts: superseded by the public-dataset strategy.
- The ChatGPT/Codex workflow notes.

Small wording changes in Appendix D, to match the current baseline: "clips" became "industrial footage", "video-only" became "video-activity-adaptive", and "paper" became "manuscript". Dataset candidates and sensor-cue assumptions remain labelled provisional, and no results, novelty, real-time or efficiency claims were added.

## 4. Files archived and why

| File | Location | Reason |
|---|---|---|
| `SAGE_Project_Feasibility_and_Scope.md` | `05_Archive/Superseded_Drafts/` | Superseded by the report; useful content merged. Kept for the acceptance-criteria checklists. |
| `SAGE_Research_Problem_and_Project_Direction.md` | `05_Archive/Superseded_Drafts/` | Superseded; useful content merged. |
| `SAGE_Industrial_Production_Line_Monitoring.md` | `05_Archive/Superseded_Drafts/` | Superseded; useful content merged. |
| `SAGE_Technical_Project_Report_pre-cleanup.md` | `05_Archive/Pre_Cleanup_Originals/` | Original MD before the image-link fix. |
| `SAGE_Technical_Project_Report_pre-merge.md` / `.docx` | `05_Archive/Pre_Cleanup_Originals/` | v1.0 before the merge (the DOCX is byte-identical to the original). |

## 5. Removed at your request (Recycle Bin)

`SAGE_Research_Proposal.docx`, `SAGE_Literature_Review_and_Reading_Map.docx`, `SAGE_Project_Brief_and_Defense_Guide.docx`. Their unique content was merged first (§3). They can be restored from the Recycle Bin until you empty it.

## 6. Open items

1. **Pretrained models: resolved.** The comparison is now required (report v1.2, §7.3 and the decision register).
2. **PDF.** Still v1.0 and missing headings (re-export skipped by you). Until it is re-exported, use the DOCX or MD.
3. **Appendix B** still cites *SAGE Research Problem and Professor Review*, which is not in the folder (left as is per your "skip").

## 7. Final folder structure

```
SAGE/
├── 00_Master/
│   ├── SAGE_Technical_Project_Report.docx   (v1.2)
│   ├── SAGE_Technical_Project_Report.md     (v1.2)
│   └── SAGE_Technical_Project_Report.pdf    (v1.0, stale)
├── 03_Assets/
│   ├── sage_architecture.png
│   ├── sage_policies.png
│   ├── sage_subjects.png
│   └── sage_workflow.png                    (spare)
├── 04_Implementation/                       (now being populated by another process; see §8)
├── 05_Archive/
│   ├── Pre_Cleanup_Originals/
│   │   ├── SAGE_Technical_Project_Report_pre-cleanup.md
│   │   ├── SAGE_Technical_Project_Report_pre-merge.docx
│   │   ├── SAGE_Technical_Project_Report_pre-merge.md
│   │   ├── SAGE_Technical_Project_Report_v1.1.docx
│   │   └── SAGE_Technical_Project_Report_v1.1.md
│   └── Superseded_Drafts/
│       ├── SAGE_Industrial_Production_Line_Monitoring.md
│       ├── SAGE_Project_Feasibility_and_Scope.md
│       └── SAGE_Research_Problem_and_Project_Direction.md
└── 06_Admin/
    ├── SAGE_Change_Log.md
    ├── SAGE_Cleanup_Report.md
    ├── SAGE_Deletion_Review.md
    └── SAGE_File_Audit.xlsx
```

`01_Research/` and `02_Project_Brief/` were removed because nothing remained in them after the removals.

## 8. Activity in the folder from another process

While this cleanup was running, something other than this session began writing to the project. That includes implementation code in `04_Implementation/` (a `sage/` package, a Streamlit `app.py`, tests, docs and an IEEE manuscript draft), a `.venv/` at the root, and a partial browser download (`Unconfirmed 959113.crdownload`, over 600 MB). I did not touch any of it. Points to check once that work settles:

- The new `04_Implementation/README.md` calls IPAD "the selected public dataset candidate". The master report still lists the dataset as **open pending validation**.
- It names OpenCV's pretrained HOG *person* detector as the pretrained comparator. That fits the new §7.3 only if a person-related event class is chosen; §7.3 leaves the model choice provisional.
- It says "the four supplied project documents remain unchanged as reference material". After this cleanup that is no longer accurate.
- The `.venv/` and the finished download probably belong in `04_Implementation/` (or outside the project) rather than at the root. I'll leave that until the work in progress has finished.
