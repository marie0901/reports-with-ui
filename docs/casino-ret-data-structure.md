# Casino-Ret Report Type - Data Structure Analysis

## Overview

The `casino-ret` report type processes marketing campaign data from CSV files and generates/updates Excel reports with week-based metrics. It handles two campaign categories:
1. **Casino & Sport A/B campaigns** - New user signups
2. **Retention campaigns** - Existing users (1st and 2nd deposits)

**Detection Method:** Campaign-based (uses `campaign_name` column from CSV, not filenames)

---

## Source Data Structure (CSV Files)

### Required Columns

| Column | Type | Description |
|--------|------|-------------|
| `timestamp` | Unix timestamp | Campaign send time (seconds since epoch) |
| `template_name` | String | Template identifier (e.g., "[S] 10 min sport basic wp", "Day 3") |
| `campaign_name` | String | **Campaign identifier** (e.g., "casino+sport A/B Reg_No_Dep", "Ret 1 dep [SPORT] ⚽️") |
| `sent` | Integer | Number of emails sent |
| `delivered` | Integer | Number of emails delivered |
| `opened` | Integer | Number of emails opened |
| `clicked` | Integer | Number of clicks |
| `converted` | Integer | Number of conversions |
| `unsubscribed` | Integer | Number of unsubscribes |

---

## Campaign-Based Section Detection

### Campaign Mappings

```python
CAMPAIGN_SECTION_MAPPINGS = {
    "casino+sport A/B Reg_No_Dep": {
        "section": "casino",
        "start_row": 3,
        "label": "casino+sport A/B Reg_No_Dep"
    },
    "Ret 1 dep [SPORT] ⚽️": {
        "section": "retention",
        "start_row": 75,
        "label": "Ret 1 dep [SPORT] ⚽️"
    },
    "Ret 2 dep [SPORT] ⚽️": {
        "section": "retention",
        "start_row": 123,
        "label": "Ret 2 dep [SPORT] ⚽️"
    }
}
```

### Detection Logic

1. Read `campaign_name` from first row of CSV
2. Exact match against known campaigns
3. Fuzzy match (case-insensitive, substring matching)
4. If no match found, skip file with error log

**Benefits:**
- ✅ Filename independent (any filename works)
- ✅ No ambiguous number matching
- ✅ Reliable and maintainable
- ✅ Clear error messages

---

## Template Mappings

### Casino & Sport Templates

```python
CASINOSPORT_MAPPINGS = {
    "[S] 10 min sport basic wp": "10min",
    "[S] 1h sport basic wp": "1h",
    "[S] 1d 2 BLOCKS (basic wp + highroller)": "1d",
    "[S] 3d casino 1st dep total wp": "4d",
    "[S] 5d casino 1st dep": "6d",
    "[S] 7d 2 BLOCKS SPORT + CAS": "8d",
    "[S] 10d A: freebet + 100fs": "10d",
    "[S] 10d b: 150%sport + 100fs": "10d",
    "[S] 12d A: freebet + 100fs": "12d",
    "[S] 12d b: 150%sport + 100fs": "12d",
}
```

### Retention Templates

```python
RETENTION_MAPPINGS = {
    "Day 3": "3d",
    "Day 4": "4d",
    "Day 6": "6d",
    "Day 8": "8d",
    "Day 10": "10d"
}
```

---

## Week Boundaries

Shared across all report types (from `plugins/constants.py`):

```python
WEEKLY_BOUNDARIES = [
    ("2025-12-29", "2026-01-04"),  # Week 1
    ("2026-01-05", "2026-01-11"),  # Week 2
    ("2026-01-12", "2026-01-18"),  # Week 3
    ("2026-01-19", "2026-01-25"),  # Week 4
    ("2026-01-26", "2026-02-01"),  # Week 5
    ("2026-02-02", "2026-02-08"),  # Week 6
    ("2026-02-09", "2026-02-15"),  # Week 7
    ("2026-02-16", "2026-02-22"),  # Week 8
]
```

---

## Target Excel Structure

### Week Column Mappings

```python
WEEK_COLUMNS = {
    'week1': 'P',  # Week 1 (29.12)
    'week2': 'O',  # Week 2 (05.01)
    'week3': 'N',  # Week 3 (12.01)
    'week4': 'M',  # Week 4 (19.01)
    'week5': 'L',  # Week 5 (26.01)
    'week6': 'K',  # Week 6 (02.02)
    'week7': 'J',  # Week 7 (09.02)
    'week8': 'I'   # Week 8 (16.02)
}
```

### Timing Block Row Mappings

```python
TIMING_BLOCKS = {
    "10min": {"casino_rows": [3, 8]},
    "1h":    {"casino_rows": [9, 14]},
    "1d":    {"casino_rows": [15, 20]},
    "3d":    {"casino_rows": [21, 26], "section_1_rows": [93, 98], "section_2_rows": [141, 146]},
    "4d":    {"casino_rows": [27, 32], "section_1_rows": [99, 104], "section_2_rows": [147, 152]},
    "6d":    {"casino_rows": [33, 38], "section_1_rows": [105, 110], "section_2_rows": [153, 158]},
    "8d":    {"casino_rows": [39, 44], "section_1_rows": [111, 116], "section_2_rows": [159, 164]},
    "10d":   {"casino_rows": [45, 50], "section_1_rows": [117, 122], "section_2_rows": [165, 170]},
    "12d":   {"casino_rows": [51, 56]},
}
```

### Metrics per Block

Each timing block contains 6 rows of metrics:

| Row Offset | Metric | Description |
|------------|--------|-------------|
| +0 | Sent | Total emails sent |
| +1 | Delivered | Total emails delivered |
| +2 | Opened | Total emails opened |
| +3 | Clicked | Total clicks |
| +4 | Unsubscribed | Total unsubscribes |
| +5 | Pct Delivered | Percentage delivered (calculated) |

---

## Week Replacement Feature

### Week Column Mappings

```python
WEEK_MAPPINGS = {
    'source': {
        '01': 'P',   # Generated report columns
        '02': 'O',
        '03': 'N',
        '04': 'M',
        '05': 'L',
        '06': 'K',
        '07': 'J',
        '08': 'I'
    },
    'target': {
        '01': 'BF',  # Existing report columns
        '02': 'BE',
        '03': 'BD',
        '04': 'BC',
        '05': 'BB',
        '06': 'BA',
        '07': 'AZ',
        '08': 'AY'
    }
}
```

---

## Summary

### Key Features

✅ **Multi-file processing** - Handles 3 CSV files (casino/sport, ret1, ret2)  
✅ **Campaign-based detection** - Uses campaign_name column, not filenames  
✅ **Template mapping** - Maps 15 unique templates to timing categories  
✅ **Week aggregation** - Groups data into 8 weekly periods  
✅ **Percentage calculation** - Auto-calculates delivery/open/click/conversion rates  
✅ **Week replacement** - Updates specific weeks in existing reports  
✅ **Data validation** - Checks template matches and suggests corrections  
✅ **Section routing** - Places data in correct Excel sections based on campaign

### Output

- **Target Sheet:** `WP Chains Sport`
- **Sections:** 3 (Signed up, Retention 1, Retention 2)
- **Timing Blocks:** 8 for casino, 5 for retention
- **Metrics per Block:** 6 rows
- **Week Columns:** 8 (I-P in generated, AY-BF in existing)
- **Total Values Copied (Week Replacement):** ~90 values
- **Detection Method:** Campaign-based (from campaign_name column)

### Metrics Tracked

- **Sent** - Total emails sent
- **Delivered** - Total emails delivered
- **Opened** - Total emails opened
- **Clicked** - Total clicks
- **Converted** - Total conversions
- **Unsubscribed** - Total unsubscribes
- **% Delivered** - Delivered / Sent × 100
- **% Open** - Opened / Delivered × 100
- **% Click** - Clicked / Delivered × 100
- **% CR** - Converted / Delivered × 100
