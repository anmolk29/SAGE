"""SAGE experiment results dashboard.

Reads saved experiment rows; it does not run detection or invent results. Sensor
quality/budgets are simulated study inputs. Processing time is measured on the
machine that produced the CSV and is not an edge-device or energy measurement.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st


st.set_page_config(page_title="SAGE | Experiment dashboard", page_icon="🏭", layout="wide")

st.title("SAGE — Industrial video monitoring")
st.caption("Sensor-Guided Adaptive Video Processing for Resource-Constrained Industrial Monitoring")
st.info(
    "This dashboard displays saved experiment data. Sensor triggers, sensor delay, and resource budgets "
    "are simulated. Processing time is measured software runtime on the run machine; it is not a "
    "Raspberry Pi benchmark, energy measurement, or physical-sensor result.",
    icon="ℹ️",
)

# Accept the canonical output names as well as common spelling variants. Keeping
# source columns intact makes the export traceable to the experiment file.
ALIASES: dict[str, tuple[str, ...]] = {
    "policy": ("policy", "scheduler", "scheduling_policy"),
    "clip": ("clip", "clip_id", "video", "video_id", "source"),
    "budget": ("budget", "budget_level", "sampling_budget", "frame_budget"),
    "detector": ("detector", "model", "vision_model", "method"),
    "recall": ("event_recall", "recall", "event_recall_fraction"),
    "false alarms/min": ("false_alarms_per_minute", "false_alarms_per_min", "fa_per_min"),
    "latency (s)": ("mean_latency_seconds", "latency_seconds", "mean_latency_s", "latency_s"),
    "frames analyzed": ("frames_analyzed", "processed_frames", "analyzed_frames", "frames_processed"),
    "total frames": ("total_frames", "frame_count", "video_frames"),
    "runtime (s)": ("processing_time_seconds", "runtime_seconds", "elapsed_seconds", "processing_seconds"),
    "events total": ("events_total", "total_events", "n_events"),
    "events detected": ("events_detected", "detected_events", "n_detected"),
    "cue reliability": ("cue_detection_probability", "sensor_recall", "cue_reliability", "sensor_sensitivity"),
    "cue false-trigger rate": ("false_trigger_rate", "sensor_false_trigger_rate", "cue_false_trigger_rate"),
    "cue delay (s)": ("cue_delay_seconds", "sensor_delay_seconds", "cue_delay_s"),
    "seed": ("seed", "random_seed", "simulator_seed"),
    "event_type": ("event_type", "event", "label", "class", "anomaly_type"),
    "event detected": ("event_detected", "detected", "is_detected", "detection_success", "hit"),
    "detection status": ("detection_status", "status", "outcome", "detection"),
    "event latency (s)": ("event_latency_seconds", "latency_seconds", "detection_latency_s", "latency_s", "latency"),
}


def canonicalize(frame: pd.DataFrame) -> pd.DataFrame:
    """Create normalized dashboard columns without dropping the original data."""
    out = frame.copy()
    lookup = {str(col).strip().lower(): col for col in out.columns}
    for canonical, names in ALIASES.items():
        if canonical in out.columns:
            continue
        found = next((lookup[name] for name in names if name in lookup), None)
        if found is not None:
            out[canonical] = out[found]
    for col in ("recall", "false alarms/min", "latency (s)", "event latency (s)", "frames analyzed", "total frames", "runtime (s)", "events total", "events detected", "cue reliability", "cue false-trigger rate", "cue delay (s)", "seed"):
        if col in out:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    return out


def canonicalize_events(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize event-level labels and detection outcomes for the event view."""
    out = canonicalize(frame)
    if "event detected" not in out and "detection status" in out:
        out["event detected"] = out["detection status"]

    def to_detected(value: Any) -> Any:
        if pd.isna(value):
            return pd.NA
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return bool(value)
        normalized = str(value).strip().lower()
        if normalized in {"true", "yes", "1", "detected", "hit", "success", "found", "tp"}:
            return True
        if normalized in {"false", "no", "0", "missed", "miss", "undetected", "failure", "not detected", "fn"}:
            return False
        return pd.NA

    if "event detected" in out:
        out["event detected"] = out["event detected"].map(to_detected).astype("boolean")
    return out


def read_csv_bytes(raw: bytes, label: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(pd.io.common.BytesIO(raw))
    except Exception as exc:  # provide an actionable, user-facing parse error
        st.error(f"Could not read {label} as CSV: {exc}")
        st.stop()
    if df.empty:
        st.warning(f"{label} has a header but no result rows.")
    return canonicalize(df)


with st.sidebar:
    st.header("Choose experiment results")
    default_path = Path("results/demo/results.csv")
    path_text = st.text_input("CSV file path", value=str(default_path))
    uploaded = st.file_uploader("Or upload a results CSV", type=["csv"])
    uploaded_events = st.file_uploader("Optional event-results CSV", type=["csv"], key="event_results_upload")
    st.caption("Expected: one row per clip × policy × condition (or a comparable aggregate row).")

if uploaded is not None:
    data = read_csv_bytes(uploaded.getvalue(), uploaded.name)
    source_label = uploaded.name
else:
    source = Path(path_text).expanduser()
    if not source.is_absolute():
        source = Path.cwd() / source
    if source.is_file():
        data = read_csv_bytes(source.read_bytes(), str(source))
        source_label = str(source)
    else:
        st.warning(f"No results file found at `{source}`. Run the experiment CLI and point this dashboard to its CSV, or upload a results file.")
        st.markdown(
            "**Quick start:** from the project root, activate the project environment, run the documented SAGE experiment command, "
            "then launch `streamlit run app.py`. Use the generated CSV path in the sidebar."
        )
        st.markdown("**Required study comparisons:** fixed-rate, video-activity-adaptive, sensor-triggered, and budget-aware adaptive.")
        st.stop()

st.caption(f"Loaded **{len(data):,} rows** from `{source_label}`.")
if not len(data):
    st.stop()
if "data_source" in data and data["data_source"].astype(str).str.contains("synthetic_demo|synthetic_test", case=False, regex=True).any():
    st.warning("These rows include synthetic demo/test data. Use them to check the pipeline only; they are not results from public industrial footage.")

# Event-level annotations have their own input path, filters, and display. They
# are deliberately kept separate from the aggregate summary policy statistics.
event_data: pd.DataFrame | None = None
event_source_label: str | None = None
if uploaded_events is not None:
    event_data = canonicalize_events(read_csv_bytes(uploaded_events.getvalue(), uploaded_events.name))
    event_source_label = uploaded_events.name
elif uploaded is None:
    sibling_events = source.with_name("event_results.csv")
    if sibling_events.is_file():
        event_data = canonicalize_events(read_csv_bytes(sibling_events.read_bytes(), str(sibling_events)))
        event_source_label = str(sibling_events)

if event_data is not None:
    if "data_source" in event_data and event_data["data_source"].astype(str).str.contains("synthetic_demo|synthetic_test", case=False, regex=True).any():
        st.warning("Event-level rows include synthetic demo/test data. Event metrics below are pipeline checks, not findings from public industrial footage.")

# Filters are based on values actually present in the loaded file.
with st.sidebar:
    st.header("Filter the loaded rows")
    filtered = data.copy()
    for col, title in (("policy", "Scheduling policy"), ("clip", "Clip"), ("detector", "Detector"), ("budget", "Budget")):
        if col in filtered.columns:
            options = sorted(filtered[col].dropna().astype(str).unique().tolist())
            chosen = st.multiselect(title, options, default=options, key=f"filter_{col}")
            filtered = filtered[filtered[col].astype(str).isin(chosen)]
    for col, title in (("cue reliability", "Cue reliability"), ("cue false-trigger rate", "Cue false-trigger rate"), ("cue delay (s)", "Cue delay (s)"), ("seed", "Random seed")):
        if col in filtered.columns and filtered[col].notna().any():
            values = sorted(filtered[col].dropna().unique().tolist())
            selected = st.multiselect(title, values, default=values, key=f"filter_{col}")
            filtered = filtered[filtered[col].isin(selected)]

if filtered.empty:
    st.warning("These filters leave no rows. Select at least one value in the sidebar.")
    st.stop()

st.subheader("Study snapshot")
metric_cols = st.columns(5)
summary_items: list[tuple[str, Any, str]] = []
if "recall" in filtered:
    summary_items.append(("Mean event recall", f"{filtered['recall'].mean():.3f}", "from loaded rows"))
if "false alarms/min" in filtered:
    summary_items.append(("Mean false alarms/min", f"{filtered['false alarms/min'].mean():.3f}", "from loaded rows"))
if "latency (s)" in filtered:
    summary_items.append(("Mean detection latency", f"{filtered['latency (s)'].mean():.3f} s", "missed events should be reported separately"))
if "frames analyzed" in filtered:
    summary_items.append(("Frames analyzed", f"{filtered['frames analyzed'].sum():,.0f}", "sum of selected rows"))
if "runtime (s)" in filtered:
    summary_items.append(("Mean software runtime", f"{filtered['runtime (s)'].mean():.3f} s", "machine-specific; not hardware energy"))
for slot, item in zip(metric_cols, summary_items):
    slot.metric(item[0], item[1], help=item[2])
if not summary_items:
    st.warning("No recognized metric columns were found. The source rows are still available below; check the experiment CSV schema.")

st.subheader("Policy comparison")
metric_candidates = [c for c in ("recall", "false alarms/min", "latency (s)", "frames analyzed", "runtime (s)") if c in filtered.columns]
if "policy" in filtered.columns and metric_candidates:
    grouped = filtered.groupby("policy", dropna=False)[metric_candidates].mean(numeric_only=True)
    st.dataframe(grouped, width="stretch")
    left, right = st.columns(2)
    if "recall" in grouped:
        with left:
            st.markdown("**Event recall by policy**")
            st.bar_chart(grouped[["recall"]])
    cost_col = "frames analyzed" if "frames analyzed" in grouped else "runtime (s)" if "runtime (s)" in grouped else None
    if cost_col and "recall" in grouped:
        with right:
            st.markdown(f"**Recall vs. {cost_col}**")
            tradeoff = grouped[[cost_col, "recall"]].dropna()
            st.scatter_chart(tradeoff, x=cost_col, y="recall")
else:
    st.caption("A policy column and recognized metric columns are needed for the comparison chart.")

st.subheader("Per-run / per-clip results")
st.dataframe(filtered, width="stretch", height=360)
csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download filtered rows as CSV", data=csv, file_name="sage_filtered_results.csv", mime="text/csv")

with st.expander("Interpretation and limits"):
    st.markdown(
        "- **Simulated inputs:** cue reliability, false triggers, cue delay, and modeled processing budgets.\n"
        "- **Measured software outputs:** elapsed runtime and processed-frame counts recorded by the experiment on its named computer.\n"
        "- **Vision comparison:** classical motion analysis and the configured pretrained model must be identified in the result rows.\n"
        "- **Report misses explicitly:** event recall alone does not communicate the number or duration of missed events.\n"
        "- **Physical extension:** camera, sensors, microcontroller, and edge-device validation are future work; this dashboard does not imply those components exist."
    )

if event_data is not None:
    st.divider()
    st.subheader("Event-level results")
    st.caption(
        f"One row per annotated event from `{event_source_label}`. These per-event outcomes are shown separately "
        "from aggregate clip/policy summary metrics above."
    )
    if "data_source" in event_data and event_data["data_source"].astype(str).str.contains("synthetic_demo|synthetic_test", case=False, regex=True).any():
        st.info("Synthetic event rows are for a smoke-test workflow only; they do not establish industrial-video performance.")

    event_filtered = event_data.copy()
    with st.sidebar:
        st.header("Filter event-level rows")
        for col, title in (("policy", "Event policy"), ("clip", "Event clip"), ("event_type", "Event type"), ("budget", "Event budget")):
            if col in event_filtered.columns:
                options = sorted(event_filtered[col].dropna().astype(str).unique().tolist())
                chosen = st.multiselect(title, options, default=options, key=f"event_filter_{col}")
                event_filtered = event_filtered[event_filtered[col].astype(str).isin(chosen)]
        if "event detected" in event_filtered.columns and event_filtered["event detected"].notna().any():
            state_options = [("Detected", True), ("Missed", False)]
            present = set(event_filtered["event detected"].dropna().astype(bool).unique())
            chosen_states = st.multiselect(
                "Detection state",
                options=[label for label, value in state_options if value in present],
                default=[label for label, value in state_options if value in present],
                key="event_filter_detection_state",
            )
            state_values = [value for label, value in state_options if label in chosen_states]
            event_filtered = event_filtered[event_filtered["event detected"].isin(state_values)]
        for col, title in (("cue reliability", "Event cue reliability"), ("cue false-trigger rate", "Event cue false-trigger rate"), ("cue delay (s)", "Event cue delay (s)"), ("seed", "Event random seed")):
            if col in event_filtered.columns and event_filtered[col].notna().any():
                values = sorted(event_filtered[col].dropna().unique().tolist())
                selected = st.multiselect(title, values, default=values, key=f"event_filter_{col}")
                event_filtered = event_filtered[event_filtered[col].isin(selected)]

    if event_filtered.empty:
        st.warning("The event filters leave no rows. Select at least one event type and detection state.")
    else:
        event_counts = st.columns(4)
        event_counts[0].metric("Annotated events", f"{len(event_filtered):,}", help="Count of event-level rows after event filters.")
        if "event detected" in event_filtered:
            known = event_filtered["event detected"].dropna()
            detected_n = int(known.sum()) if len(known) else 0
            event_counts[1].metric("Detected events", f"{detected_n:,}", help="Event-level detections; unknown states are excluded.")
            if len(known):
                event_counts[2].metric("Event-level recall", f"{known.mean():.3f}", help="Detected annotated events divided by annotated events with known detection state.")
        if "event latency (s)" in event_filtered:
            detected_latencies = event_filtered.loc[event_filtered.get("event detected", pd.Series(True, index=event_filtered.index)).eq(True), "event latency (s)"]
            if detected_latencies.notna().any():
                event_counts[3].metric("Mean detected-event latency", f"{detected_latencies.mean():.3f} s", help="Mean over detected events with a recorded latency; missed events are not assigned a latency.")

        breakdown_dims = [c for c in ("policy", "event_type") if c in event_filtered.columns]
        if breakdown_dims and "event detected" in event_filtered.columns:
            breakdown = (
                event_filtered.groupby(breakdown_dims, dropna=False)
                .agg(annotated_events=("event detected", "count"), detected_events=("event detected", "sum"))
                .reset_index()
            )
            breakdown["event-level recall"] = breakdown["detected_events"] / breakdown["annotated_events"].replace(0, pd.NA)
            st.markdown("**Event-level breakdown by policy and event type**")
            st.dataframe(breakdown, width="stretch")
        st.markdown("**Filtered event-level rows**")
        st.dataframe(event_filtered, width="stretch", height=320)
        st.download_button(
            "Download filtered event rows as CSV",
            data=event_filtered.to_csv(index=False).encode("utf-8"),
            file_name="sage_filtered_event_results.csv",
            mime="text/csv",
        )
elif uploaded is not None or ("event_type" in data.columns and ("event detected" in data.columns or "detection status" in data.columns)):
    st.info("No separate event-results CSV is loaded. Upload one in the sidebar to view per-event detections, misses, and latency separately from summary metrics.")

