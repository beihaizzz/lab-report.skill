# Lab Report JSON Schemas

This document defines the JSON data structures used by the lab-report skill.

---

## progress.json Schema

Tracks the experiment progress state.

```json
{
  "experiment_name": "string",
  "total_steps": "int",
  "current_step": "int",
  "completed_steps": ["int"],
  "screenshots_required": [
    {
      "step": "int",
      "description": "string",
      "captured": "bool",
      "path": "string|null"
    }
  ],
  "notes": {"step_N": "string"},
  "last_updated": "ISO8601 datetime",
  "status": "not_started | in_progress | completed"
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `experiment_name` | string | Name of the experiment |
| `total_steps` | int | Total number of steps in the experiment |
| `current_step` | int | Current step being worked on (1-indexed) |
| `completed_steps` | [int] | List of completed step numbers |
| `screenshots_required` | array | List of screenshot requirements per step |
| `notes` | object | Step-level notes, key format: "step_N" |
| `last_updated` | string | ISO8601 datetime of last update |
| `status` | string | Overall progress status: not_started, in_progress, or completed |

---

## student-info.json Schema

Stores student identification information.

```json
{
  "姓名": "string",
  "学号": "string",
  "学院": "string",
  "专业": "string",
  "班级": "string"
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `姓名` | string | Student's full name |
| `学号` | string | Student ID number |
| `学院` | string | College/faculty name |
| `专业` | string | Major/discipline name |
| `班级` | string | Class/turor group |

---

## template-data.json Schema

Complete template data for generating a lab report.

```json
{
  "姓名": "string",
  "学号": "string",
  "学院": "string",
  "专业": "string",
  "班级": "string",
  "课程名": "string",
  "实验名称": "string",
  "实验日期": "string",
  "实验地点": "string",
  "实验目的": "string",
  "实验原理": "string",
  "实验器材": "string",
  "实验步骤": "string",
  "实验数据": "string",
  "实验结果": "string",
  "实验结论": "string"
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `姓名` | string | Student's full name |
| `学号` | string | Student ID number |
| `学院` | string | College/faculty name |
| `专业` | string | Major/discipline name |
| `班级` | string | Class/tutor group |
| `课程名` | string | Course name |
| `实验名称` | string | Experiment title |
| `实验日期` | string | Experiment date |
| `实验地点` | string | Experiment location |
| `实验目的` | string | Experiment objectives |
| `实验原理` | string | Experiment principles/theory |
| `实验器材` | string | Equipment and materials list |
| `实验步骤` | string | Experiment procedures |
| `实验数据` | string | Raw experimental data |
| `实验结果` | string | Processed results |
| `实验结论` | string | Conclusions and analysis |