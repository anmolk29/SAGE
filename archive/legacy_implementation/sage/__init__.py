"""SAGE: Sensor-Guided Adaptive Video Processing experiment baseline."""

from .engine import (
    Event,
    ExperimentConfig,
    SimulationConfig,
    load_events,
    load_frames,
    run_experiment,
    write_event_results,
)

__all__ = [
    "Event",
    "ExperimentConfig",
    "SimulationConfig",
    "load_events",
    "load_frames",
    "run_experiment",
    "write_event_results",
]
