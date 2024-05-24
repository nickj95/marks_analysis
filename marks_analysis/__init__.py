# marks_analysis/__init__.py
from .data_processing import load_data, preprocess_marker_data, preprocess_paper_data
from .analysis import (
    MarkBreakdown,
    get_other_mark,
    plot_agreed_marks,
    check_agreed_marks,
    plot_mark_differences,
    plot_absolute_mark_differences,
    analyze_data,
    analyze_all_examiners
)

__all__ = [
    "load_data",
    "preprocess_marker_data",
    "preprocess_paper_data",
    "MarkBreakdown",
    "get_other_mark",
    "plot_agreed_marks",
    "check_agreed_marks",
    "plot_mark_differences",
    "plot_absolute_mark_differences",
    "analyze_data",
    "analyze_all_examiners"
]