# Prompt: Create New Report Type Plugin

## Overview

This document provides a structured prompt for AI agents to create a new report type plugin for the report automation system. Use this template when you need to add support for a new report format.

---

## Prerequisites

Before starting, you need:

1. **Source CSV files** - Sample data files with actual data
2. **Target Excel file** - The template/existing report to update
3. **Week boundaries** - Date ranges for each week (usually shared across all report types)

---

## AI Agent Prompt Template

```
I need to create a new report type plugin called "{REPORT_TYPE_NAME}".

## Source Files

I have {NUMBER} CSV files located at: {PATH_TO_CSV_FILES}

The CSV files contain these standard columns:
- timestamp (Unix timestamp)
- template_name (string)
- campaign_name (string)
- sent, delivered, opened, clicked, unsubscribed (integers)

## Target File

The target Excel file is located at: {PATH_TO_EXCEL}

It has {NUMBER} sheets:
- {SHEET_NAME_1}: {DESCRIPTION}
- {SHEET_NAME_2}: {DESCRIPTION}

## Requirements

1. **Campaign Detection**: Use the `campaign_name` column to identify which campaign the data belongs to
2. **Template Mapping**: Map CSV template names to Excel rows
3. **Week Filtering**: Filter data by week boundaries before calculating metrics
4. **Metric Calculation**: Calculate these metrics per template:
   - Sent, Delivered, Opened, Clicked, Unsubscribed
   - Percentages: % Delivered, % Open, % Click
5. **Formula Preservation**: Skip rows that contain Excel formulas (aggregate rows)
6. **Week Replacement**: Update specific week columns in existing Excel file

## Analysis Tasks

Please perform these steps:

### Step 1: Analyze Source CSV Files
```bash
# List all CSV files
ls -la {PATH_TO_CSV_FILES}

# For each CSV, show:
# - Campaign names (unique values in campaign_name column)
# - Template names (unique values in template_name column)
# - Row counts
# - Date range (min/max timestamp)
```

### Step 2: Analyze Target Excel Structure
```bash
# For each sheet in the Excel:
# - List all sheet names
# - For each sheet, identify:
#   - Column B values (campaign/template names)
#   - Column C values (filter indicators like "All Mail", "None")
#   - Row numbers where campaigns start
#   - Row numbers where templates are located
#   - Which rows have formulas (aggregate rows)
#   - Week column range (e.g., F-BE for 52 weeks)
```

### Step 3: Create Campaign Mappings

Based on the analysis, create a mapping structure:

```python
CAMPAIGN_SECTION_MAPPINGS = {
    "Campaign Name from CSV": {
        "sheet": "Target Sheet Name",
        "start_row": 3,  # First row of this campaign section
        "has_aggregate_row": True,  # Does first row have formulas?
        "label": "Campaign Name from CSV"
    },
    # ... more campaigns
}
```

### Step 4: Create Template Mappings

Document the mapping between CSV templates and Excel rows:

| Excel Column B | CSV Template Name | Excel Row | Notes |
|----------------|-------------------|-----------|-------|
| Campaign Name | *(aggregate - skip)* | 3 | Has formulas |
| Template 1 | Template 1 | 11 | Write data here |
| Template 2 | Template 2 | 19 | Write data here |

### Step 5: Identify Week Columns

```python
WEEK_COLUMNS = {
    '01': 'BE',  # Week 1 column
    '02': 'BD',  # Week 2 column
    # ... map week numbers to Excel columns
}
```

### Step 6: Create Plugin Implementation

Create a plugin file at:
`/api/packages/report_automation/plugins/implementations/{report_type}.py`

The plugin must:
1. Inherit from `BaseReportPlugin`
2. Use `@register_plugin` decorator
3. Implement these methods:
   - `execute()` - Main entry point
   - `_detect_campaign()` - Match CSV campaign to mapping
   - `_replace_week()` - Write data to Excel
   - `_find_template_row()` - Find Excel row for template
   - `_calculate_metrics()` - Calculate metrics from CSV data

### Step 7: Key Implementation Points

**Week Filtering (CRITICAL):**
```python
# Must filter by week BEFORE calculating metrics
week_idx = int(replace_week) - 1
week_start_str, week_end_str = WEEKLY_BOUNDARIES[week_idx]
week_start = pd.to_datetime(week_start_str + ' 00:00:00')
week_end = pd.to_datetime(week_end_str + ' 23:59:59')
df = df[(df['datetime'] >= week_start) & (df['datetime'] <= week_end)]
```

**Template Matching:**
```python
# Use EXACT match for template names
template_df = df[df['template_name'] == template_name]
```

**Skip Aggregate Rows:**
```python
# Don't write to rows with has_aggregate_row=True
if campaign_info.get('has_aggregate_row', False):
    logger.info(f"Skipping aggregate row {start_row}")
    # Skip to next template
```

**Write Only Data Metrics:**
```python
# Write only first 5 metrics (skip percentage rows with formulas)
for offset in range(5):  # Sent, Delivered, Opened, Clicked, Unsubscribed
    cell = ws[f'{target_col}{template_row + offset}']
    cell.value = metrics[offset]
```

### Step 8: Create Documentation

Create a data structure document at:
`/docs/{report_type}-data-structure.md`

Include:
- Overview of report type
- Source CSV structure
- Target Excel structure
- Campaign mappings (with tables)
- Template mappings (with tables)
- Week column mappings
- Row structure (8 rows per template: 5 data + 3 formula)
- Implementation notes

### Step 9: Register Plugin

Add to `/api/packages/report_automation/plugins/implementations/__init__.py`:
```python
from .{report_type} import {ReportType}Plugin

__all__ = [..., "{ReportType}Plugin"]
```

### Step 10: Test

Test with actual data:
1. Upload CSV files for a specific week
2. Provide existing Excel file
3. Specify week number to replace
4. Verify:
   - Correct values written to correct rows
   - Formulas preserved in aggregate rows
   - Formulas preserved in percentage rows
   - Only specified week column updated

## Output Format

Please provide:

1. **Analysis Report** (Markdown)
   - CSV file analysis
   - Excel structure analysis
   - Campaign mappings
   - Template mappings

2. **Plugin Code** (Python)
   - Complete implementation
   - Proper error handling
   - Logging for debugging

3. **Documentation** (Markdown)
   - Data structure document
   - Comparison with similar report types
   - Known limitations

4. **Test Results**
   - Sample calculation showing correct values
   - Verification that formulas are preserved
```

---

## Example: Creating "Slot" Report Type

### Input to AI Agent

```
I need to create a new report type plugin called "slot".

## Source Files

I have 7 CSV files located at: /Users/mmshiji/Downloads/week7_slot/

Files:
- SLOT_rnd_feb15.csv (Reg_No_Dep campaign, 17 templates)
- SLOT_ret1_feb15.csv (Retention 1 dep, 4 templates)
- SLOT_ret2_feb15.csv (Retention 2 dep, 4 templates)
- SLOT_inactive7_feb15.csv (Inactive 7, 2 templates)
- SLOT_inactive14_feb15.csv (Inactive 14, 2 templates)
- SLOT_inactive21_feb15.csv (Inactive 21, 2 templates)
- SLOT_inactive30_feb15.csv (Inactive 30+, 8 templates)

## Target File

The target Excel file is: SLOT_ChainsReport_2026.xlsx

It has 2 main sheets:
- WP Chains Sport: Welcome and retention campaigns
- AWOL Chains Sport: Inactive user campaigns

## Requirements

1. Campaign Detection: Use campaign_name column
2. Template Mapping: Each template gets its own 8-row block
3. Week Filtering: Filter by week 7 (Feb 9-15, 2026)
4. Metrics: Sent, Delivered, Opened, Clicked, Unsubscribed + 3 percentage formulas
5. Formula Preservation: Skip aggregate rows (Column C = "All Mail"/"All Sport Mail")
6. Week Replacement: Update column AY (week 7) in existing Excel

Please analyze the files and create the plugin.
```

### Expected Output

1. **Analysis Report**: Shows all campaigns, templates, and row mappings
2. **Plugin Code**: Complete slot.py implementation
3. **Documentation**: slot-data-structure.md with all mappings
4. **Test Results**: Verification that week 7 data is correctly written

---

## Common Patterns Across Report Types

### Pattern 1: Campaign-Based Detection

All report types use `campaign_name` column to route data to correct Excel section.

```python
def _detect_campaign(self, df):
    campaign_name = df['campaign_name'].iloc[0]
    if campaign_name in CAMPAIGN_SECTION_MAPPINGS:
        return CAMPAIGN_SECTION_MAPPINGS[campaign_name]
```

### Pattern 2: Week Filtering

All report types filter by week boundaries before calculating metrics.

```python
week_start = pd.to_datetime(WEEKLY_BOUNDARIES[week_idx][0] + ' 00:00:00')
week_end = pd.to_datetime(WEEKLY_BOUNDARIES[week_idx][1] + ' 23:59:59')
df = df[(df['datetime'] >= week_start) & (df['datetime'] <= week_end)]
```

### Pattern 3: Template Matching

Match CSV template_name to Excel Column B value.

```python
# Exact match
template_df = df[df['template_name'] == template_name]

# Or substring match for multi-line Excel cells
if template_name in str(excel_col_b_value):
    return row_number
```

### Pattern 4: Metric Calculation

Calculate 5 data metrics + 3 percentage metrics (formulas).

```python
def _calculate_metrics(self, df):
    sent = df['sent'].sum()
    delivered = df['delivered'].sum()
    opened = df['opened'].sum()
    clicked = df['clicked'].sum()
    unsubscribed = df['unsubscribed'].sum()
    
    # Percentages calculated by Excel formulas
    return [sent, delivered, opened, clicked, unsubscribed, 0, 0, 0]
```

### Pattern 5: Formula Preservation

Never write to rows with formulas.

```python
# Skip aggregate rows
if campaign_info.get('has_aggregate_row', False):
    # Don't write to start_row
    pass

# Write only first 5 metrics (skip percentage rows 6-8)
for offset in range(5):
    ws[f'{col}{row + offset}'].value = metrics[offset]
```

---

## Differences Between Report Types

| Aspect | Casino-Ret | AWOL | AB-Report | Slot |
|--------|-----------|------|-----------|------|
| **Grouping** | Timing categories | Day periods | Time periods | Individual templates |
| **Aggregation** | Sum by category | Sum by day | Sum by period | Sum by template |
| **Target Sheets** | 1 (WP Chains Sport) | 1 (AWOL Chains Sport) | 1 (WP Chains Sport) | 2 (WP + AWOL) |
| **Metrics per Block** | 6 rows | 8 rows | 8 rows | 8 rows |
| **Template Mapping** | Many-to-one | Many-to-one | Many-to-one | One-to-one |
| **Aggregate Rows** | Skip | Skip | Skip | Skip |

---

## Validation Checklist

After creating a new report type, verify:

- [ ] Campaign detection works for all CSV files
- [ ] Template names match exactly between CSV and Excel
- [ ] Week filtering is applied before metric calculation
- [ ] Only specified week column is updated
- [ ] Aggregate rows are skipped (formulas preserved)
- [ ] Percentage rows are skipped (formulas preserved)
- [ ] Values match manual calculation
- [ ] Plugin is registered in __init__.py
- [ ] Documentation is complete
- [ ] Code has proper logging for debugging

---

## Tips for AI Agents

1. **Always analyze first**: Don't assume structure, check actual files
2. **Use exact matches**: Template names must match exactly (including spaces)
3. **Filter by week early**: Apply week filter immediately after reading CSV
4. **Preserve formulas**: Never write to rows with formulas
5. **Log everything**: Add detailed logging for debugging
6. **Test with real data**: Verify calculations match expected values
7. **Document thoroughly**: Create clear mapping tables in documentation
8. **Follow patterns**: Use existing plugins (casino-ret, slot) as reference
9. **Handle edge cases**: Empty data, missing templates, invalid week numbers
10. **Keep it simple**: Minimal code, clear logic, no over-engineering
