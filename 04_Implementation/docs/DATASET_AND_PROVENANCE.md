# SAGE Dataset and Provenance Guide: IPAD Candidate

**Status:** IPAD is a candidate source for SAGE, not data checked into this workspace. This file is a retrieval and validation checklist; it does not state that the archive has been downloaded or that its license has been cleared.

## Source links and what they establish

- [Official IPAD project page](https://ljf1113.github.io/IPAD_VAD/) links to the paper, dataset download, and code. Its description says the dataset covers 16 industrial devices and more than six hours of synthetic and real-world footage. The page's displayed Creative Commons notice applies to the **website source code/content**; do not assume that notice licenses the dataset.
- [IPAD Hugging Face dataset mirror](https://huggingface.co/datasets/MSherbinii/ipad-industrial-anomaly) describes 597,979 frames, 12 synthetic and 4 real-world scenarios, 39 anomaly classes, training/testing frame folders, and frame-level anomaly annotations. It currently lists a total file size of 8.92 GB. Treat this as a mirror/card statement, not a verified local size or a license grant.
- [Original paper on arXiv](https://arxiv.org/abs/2404.15033), DOI: [10.48550/arXiv.2404.15033](https://doi.org/10.48550/arXiv.2404.15033). The Hugging Face card directs users to the original paper/project page for dataset licensing; it does not itself specify a clear dataset license.

The paper's open-access license and the project website's license should not be interpreted as automatically licensing the video frames. Before including any clips, frames, annotations, or derived imagery in a report, repository, or public demonstration, confirm the dataset-specific reuse terms from the dataset authors/original download page and record the source of that confirmation. If the terms cannot be established, do not redistribute the files; ask the authors or select a source with explicit reuse terms.

## Access procedure

1. Open the official project page and follow its Dataset link to the authors' original download location. Review the terms displayed there and retain a dated note or screenshot/reference in project records.
2. Compare the provided archive and documentation with the Hugging Face mirror card. The mirror documents the artifact as `ipad_dataset.zip` and gives an approximate reported size of 8.92 GB. Confirm the current file size before allocating storage; the local disk should have room for both the archive and extracted frames, which can substantially exceed the archive size.
3. If permitted and convenient, retrieve the archive from the Hugging Face dataset repository using its documented `huggingface_hub` flow (`hf_hub_download`, repository `MSherbinii/ipad-industrial-anomaly`, file `ipad_dataset.zip`, repository type `dataset`). This requires Python and the `huggingface_hub` package. Review the downloaded file before extracting; do not extract untrusted files into the project source directory.
4. Extract into a data location outside version control, for example `data/raw/ipad/` if the local project's ignore rules exclude it. The current project folder does not contain the IPAD archive or its frames.
5. Record retrieval date, exact source URL, file name, byte size, checksum (such as SHA-256), license/permission evidence, extraction path, and any transformations in a manifest. Keep raw files immutable; write converted or resized derivatives to a separate location and record each transformation.

## Expected layout and temporal-data validation

The mirror card describes a hierarchy with device folders such as `S01_conveyer_belt/` and `R01_conveyer_belt_real/`, each with `training/frames/` and `testing/frames/`. It describes training frames as normal-only, testing frames as normal plus anomalous, and frame-level anomaly annotations. Validate this against the actual downloaded archive; the Hugging Face dataset viewer is currently unavailable for the subset.

The described artifact may consist of image frames rather than playable video files with source timestamps. Before using it in SAGE:

1. Inventory actual filenames, extensions, dimensions, device and split folders, and annotation files.
2. Determine temporal ordering from the documented naming convention or source manifest. Check gaps, duplicates, resets between clips, and whether files belong to distinct sequences.
3. Find original frame-rate, timestamp, or cycle-period metadata for each sequence. Do not infer a physical frame rate from numeric filenames alone.
4. Align annotations to the exact sequence/frame convention. Confirm whether anomaly labels are frame-level, interval-based, or include periodicity metadata, and record the conversion rule used by SAGE.
5. Keep training and evaluation roles consistent with the source. Split by clip/device/process where possible; do not randomly split adjacent frames from a sequence across calibration and evaluation.

If original timestamps or frame rate cannot be established, report latency in **frames**. If the experiment replays frames at an assumed rate, call it a replay-time proxy and state the assumption; do not call it source-time or physical detection latency. Confirm frame-label alignment before reporting recall or false alarms. The dataset's periodicity labels should not silently be treated as anomaly ground truth.

## Provenance record template

Copy and complete one record per downloaded release or derived subset:

| Field | Value |
|---|---|
| Dataset | IPAD: Industrial Process Anomaly Detection Dataset |
| Original project page | https://ljf1113.github.io/IPAD_VAD/ |
| Original download location | [record exact URL after opening project page] |
| Mirror (if used) | https://huggingface.co/datasets/MSherbinii/ipad-industrial-anomaly |
| Paper / citation | J. Liu et al., “IPAD: Industrial Process Anomaly Detection Dataset,” arXiv:2404.15033, 2024; DOI 10.48550/arXiv.2404.15033 |
| Retrieval date and source | [ ] |
| Archive filename, bytes, SHA-256 | [ ] |
| License / permission evidence | [record dataset-specific terms; URL and date; do not substitute website or paper license] |
| Local raw data path (not committed) | [ ] |
| Device/clip IDs and split | [ ] |
| Actual file format and dimensions | [ ] |
| Ordering convention and continuity checks | [ ] |
| Source timestamp/FPS evidence | [ ] |
| Annotation files and alignment rule | [ ] |
| Transformations and derived-data paths | [ ] |
| Exclusions and reason | [ ] |
| Redistribution restrictions | [ ] |

## Citation

Use the paper citation and verify the final bibliographic metadata against the venue record before manuscript submission:

> J. Liu, Y. Yan, J. Li, W. Zhao, P. Chu, X. Sheng, Y. Liu, and X. Yang, “IPAD: Industrial Process Anomaly Detection Dataset,” *arXiv preprint arXiv:2404.15033*, 2024, doi: 10.48550/arXiv.2404.15033.

```bibtex
@article{liu2024ipad,
  author  = {Jinfan Liu and Yichao Yan and Junjie Li and Weiming Zhao and Pengzhi Chu and Xingdong Sheng and Yunhui Liu and Xiaokang Yang},
  title   = {IPAD: Industrial Process Anomaly Detection Dataset},
  journal = {arXiv preprint arXiv:2404.15033},
  year    = {2024},
  doi     = {10.48550/arXiv.2404.15033}
}
```

## SAGE reporting boundary

The reported frame count, class count, device count, duration, and archive size above come from the current project/mirror descriptions, not an inspection of files in this workspace. Recheck all such values against the retrieved release. No local copy is present. A public download is not by itself evidence of permission to redistribute. Dataset frames are not necessarily equivalent to timestamped videos, and labels need an explicit mapping to SAGE event definitions before use.
