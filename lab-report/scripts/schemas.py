"""JSON schema definitions for lab-report skill.

This module defines the data structures used for:
- Progress tracking (ProgressState)
- Student information (StudentInfo)
- Report template data (TemplateData)
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class ScreenshotRequirement:
    """Represents a screenshot requirement for a specific step.

    Attributes:
        step: The step number this screenshot applies to.
        description: Human-readable description of what to capture.
        captured: Whether the screenshot has been taken.
        path: File path to the screenshot file, or None if not yet captured.
    """
    step: int
    description: str
    captured: bool = False
    path: Optional[str] = None


@dataclass
class ProgressState:
    """Tracks the state of an experiment's progress.

    Attributes:
        experiment_name: Name of the experiment.
        total_steps: Total number of steps in the experiment.
        current_step: Current step being worked on (1-indexed).
        completed_steps: List of step numbers that have been completed.
        screenshots_required: List of screenshot requirements per step.
        notes: Dictionary mapping step identifiers to note content (key format: "step_N").
        last_updated: ISO8601 datetime of last update.
        status: Overall progress status: "not_started", "in_progress", or "completed".
    """
    experiment_name: str
    total_steps: int
    current_step: int = 0
    completed_steps: list[int] = field(default_factory=list)
    screenshots_required: list[ScreenshotRequirement] = field(default_factory=list)
    notes: dict[str, str] = field(default_factory=dict)
    last_updated: str = ""
    status: str = "not_started"


@dataclass
class StudentInfo:
    """Stores student identification information.

    Attributes:
        姓名: Student's full name.
        学号: Student ID number.
        学院: College/faculty name.
        专业: Major/discipline name.
        班级: Class/tutor group.
    """
    姓名: str
    学号: str
    学院: str
    专业: str
    班级: str


@dataclass
class TemplateData:
    """Complete template data for generating a lab report.

    Contains both student information and experiment details needed
    to populate a lab report document.

    Attributes:
        姓名: Student's full name.
        学号: Student ID number.
        学院: College/faculty name.
        专业: Major/discipline name.
        班级: Class/tutor group.
        课程名: Course name.
        实验名称: Experiment title.
        实验日期: Experiment date.
        实验地点: Experiment location.
        实验目的: Experiment objectives.
        实验原理: Experiment principles/theory.
        实验器材: Equipment and materials list.
        实验步骤: Experiment procedures.
        实验数据: Raw experimental data.
        实验结果: Processed results.
        实验结论: Conclusions and analysis.
    """
    姓名: str
    学号: str
    学院: str
    专业: str
    班级: str
    课程名: str
    实验名称: str
    实验日期: str
    实验地点: str
    实验目的: str
    实验原理: str
    实验器材: str
    实验步骤: str
    实验数据: str
    实验结果: str
    实验结论: str