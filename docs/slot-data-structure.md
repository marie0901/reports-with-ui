# Slot Report Type - Data Structure Analysis

## Overview

The `slot` report type processes sport campaign data from CSV files and updates Excel reports with week-based metrics. It handles three campaign categories:
1. **Reg_No_Dep (casino/sport)** - New user signups (no deposit)
2. **Retention campaigns** - Existing users (1st and 2nd deposits)
3. **Inactive campaigns** - Re-engagement campaigns (7, 14, 21, 30+ days inactive)

**Detection Method:** Campaign-based (uses `campaign_name` column from CSV)

---

## Source Data Structure (CSV Files)

### File Types

| File | Campaign Name | Templates | Description |
|------|---------------|-----------|-------------|
| `SLOT_rnd_feb15.csv` | `Reg_No_Dep (casino/sport)` | 17 | New user signups (5 Sport + 12 Casino) |
| `SLOT_ret1_feb15.csv` | `Retention 1 dep (sport)` | 4 | 1st deposit retention |
| `SLOT_ret2_feb15.csv` | `Retention 2 dep (sport)` | 4 | 2nd deposit retention |
| `SLOT_inactive7_feb15.csv` | `Inactive 7 (sport)` | 2 | 7 days inactive |
| `SLOT_inactive14_feb15.csv` | `Inactive 14 (sport)` | 2 | 14 days inactive |
| `SLOT_inactive21_feb15.csv` | `Inactive 21 (sport)` | 2 | 21 days inactive |
| `SLOT_inactive30_feb15.csv` | `Inactive 30+ (sport)` | 8 | 30+ days inactive |

### Required Columns

| Column | Type | Description |
|--------|------|----------------|
| `timestamp` | Unix timestamp | Campaign send time (seconds since epoch) |
| `template_name` | String | Template identifier (e.g., "Day 2 - Sport Welcome bonus") |
| `campaign_name` | String | **Campaign identifier** (e.g., "Reg_No_Dep (casino/sport)") |
| `sent` | Integer | Number of emails sent |
| `delivered` | Integer | Number of emails delivered |
| `opened` | Integer | Number of emails opened |
| `clicked` | Integer | Number of clicks |
| `unsubscribed` | Integer | Number of unsubscribes |

---

## Campaign-Based Section Detection

### Campaign Mappings

```python
CAMPAIGN_SECTION_MAPPINGS = {
    "Reg_No_Dep (casino/sport)": {
        "sheet": "WP Chains Sport",
        "start_row": 3,
        "has_aggregate_row": True,  # Row 3 has formulas
        "label": "Reg_No_Dep (casino/sport)"
    },
    "Retention 1 dep (sport)": {
        "sheet": "WP Chains Sport",
        "start_row": 51,
        "has_aggregate_row": True,  # Row 51 has formulas
        "label": "Retention 1 dep (sport)"
    },
    "Retention 2 dep (sport)": {
        "sheet": "WP Chains Sport",
        "start_row": 91,
        "has_aggregate_row": True,  # Row 91 has formulas
        "label": "Retention 2 dep (sport)"
    },
    "Inactive 7 (sport)": {
        "sheet": "AWOL Chains Sport",
        "start_row": 3,
        "has_aggregate_row": True,  # Row 3 has formulas
        "label": "Inactive 7 (sport)"
    },
    "Inactive 14 (sport)": {
        "sheet": "AWOL Chains Sport",
        "start_row": 27,
        "has_aggregate_row": True,  # Row 27 has formulas
        "label": "Inactive 14 (sport)"
    },
    "Inactive 21 (sport)": {
        "sheet": "AWOL Chains Sport",
        "start_row": 51,
        "has_aggregate_row": True,  # Row 51 has formulas
        "label": "Inactive 21 (sport)"
    },
    "Inactive 30+ (sport)": {
        "sheet": "AWOL Chains Sport",
        "start_row": 75,
        "has_aggregate_row": True,  # Row 75 has formulas
        "label": "Inactive 30+ (sport)"
    }
}
```

### Detection Logic

1. Read `campaign_name` from CSV
2. Exact match against known campaigns
3. Determine target sheet and starting row
4. **Skip aggregate rows** (rows with formulas in Column C="All Mail"/"All Sport Mail")
5. Write template data to individual template rows

**Benefits:**
- ✅ Filename independent
- ✅ Clear sheet routing
- ✅ Preserves Excel formulas in aggregate rows

---

## Template Mappings

### Reg_No_Dep (casino/sport) Templates

**CSV Campaign:** `Reg_No_Dep (casino/sport)`  
**Target Sheet:** WP Chains Sport  
**CSV File:** `SLOT_rnd_feb15.csv`  
**Total CSV Templates:** 17 (5 Sport + 12 Casino)

#### Templates Written to Excel (Sport only - 5 templates)

| Excel Column B | CSV Template Name | Excel Row |
|----------------|-------------------|----------|
| Reg_No_Dep (casino/sport) | *(aggregate - skip, has formulas)* | 3 |
| Day 2 - Sport Welcome bonus  | Day 2 - Sport Welcome bonus  | 11 |
| Day 4 - Sport Welcome bonus reminder | Day 4 - Sport Welcome bonus reminder | 19 |
| Day 13 - Sport Welcome boost bonus  | Day 13 - Sport Welcome boost bonus  | 27 |
| Day 15 - Sport Welcome boost bonus reminder | Day 15 - Sport Welcome boost bonus reminder | 35 |
| Day 20 - Sport Highroller | Day 20 - Sport Highroller | 43 |

#### Templates NOT Written (Casino - 12 templates)

These templates exist in CSV but are NOT written to Excel:
- Day 1 (10 min)
- Day 1 (1 hour)
- Day 2
- Day 4
- Day 6 A
- Day 6 B
- Day 8 A
- Day 8 B
- Day 10 A
- Day 10 B
- Day 13 A
- Day 13 B

### Retention 1 dep (sport) Templates

**CSV Campaign:** `Retention 1 dep (sport)`  
**Target Sheet:** WP Chains Sport  
**CSV File:** `SLOT_ret1_feb15.csv`  
**Total CSV Templates:** 4 (all written)

| Excel Column B | CSV Template Name | Excel Row |
|----------------|-------------------|----------|
| Retention 1 dep (sport) | *(aggregate - skip)* | 51 |
| Day 1 - Bonus on 2nd deposit | Day 1 - Bonus on 2nd deposit | 59 |
| Day 3 - Bonus on 2nd deposit reminder | Day 3 - Bonus on 2nd deposit reminder | 67 |
| Day 5 - Welcome boost dep bonus | Day 5 - Welcome boost dep bonus | 75 |
| Day 8 - Welcome boost dep bonus reminder | Day 8 - Welcome boost dep bonus reminder | 83 |

### Retention 2 dep (sport) Templates

**CSV Campaign:** `Retention 2 dep (sport)`  
**Target Sheet:** WP Chains Sport  
**CSV File:** `SLOT_ret2_feb15.csv`  
**Total CSV Templates:** 4 (all written)

| Excel Column B | CSV Template Name | Excel Row |
|----------------|-------------------|----------|
| Retention 2 dep (sport) | *(aggregate - skip)* | 91 |
| Day 1 - Bonus on 3nd deposit | Day 1 - Bonus on 3nd deposit | 99 |
| Day 3 - Bonus on 3nd deposit reminder | Day 3 - Bonus on 3nd deposit reminder | 107 |
| Day 5 - Welcome boost dep bonus | Day 5 - Welcome boost dep bonus | 115 |
| Day 8 - Welcome boost dep bonus reminder  | Day 8 - Welcome boost dep bonus reminder  | 123 |

**Note:** Template name has trailing space in CSV.

### Inactive 7 (sport) Templates

**CSV Campaign:** `Inactive 7 (sport)`  
**Target Sheet:** AWOL Chains Sport  
**CSV File:** `SLOT_inactive7_feb15.csv`  
**Total CSV Templates:** 2 (all written)

| Excel Column B | CSV Template Name | Excel Row |
|----------------|-------------------|----------|
| Inactive 7 (sport) | *(aggregate - skip)* | 3 |
| Sport Inactive 7_1 (multi-line) | Sport Inactive 7_1 | 11 |
| Sport Inactive 7_2 (multi-line) | Sport Inactive 7_2 | 19 |

### Inactive 14 (sport) Templates

**CSV Campaign:** `Inactive 14 (sport)`  
**Target Sheet:** AWOL Chains Sport  
**CSV File:** `SLOT_inactive14_feb15.csv`  
**Total CSV Templates:** 2 (all written)

| Excel Column B | CSV Template Name | Excel Row |
|----------------|-------------------|----------|
| Inactive 14 (sport) | *(aggregate - skip)* | 27 |
| Sport Inactive 14_1 (multi-line) | Sport Inactive 14_1 | 35 |
| Sport Inactive 14_2 (multi-line) | Sport Inactive 14_2 | 43 |

### Inactive 21 (sport) Templates

**CSV Campaign:** `Inactive 21 (sport)`  
**Target Sheet:** AWOL Chains Sport  
**CSV File:** `SLOT_inactive21_feb15.csv`  
**Total CSV Templates:** 2 (all written)

| Excel Column B | CSV Template Name | Excel Row |
|----------------|-------------------|----------|
| Inactive 21 (sport) | *(aggregate - skip)* | 51 |
| Sport Inactive 21_1 (multi-line) | Sport Inactive 21_1 | 59 |
| Sport Inactive 21_2 (multi-line) | Sport Inactive 21_2 | 67 |

### Inactive 30+ (sport) Templates

**CSV Campaign:** `Inactive 30+ (sport)`  
**Target Sheet:** AWOL Chains Sport  
**CSV File:** `SLOT_inactive30_feb15.csv`  
**Total CSV Templates:** 8 (all written)

| Excel Column B | CSV Template Name | Excel Row |
|----------------|-------------------|----------|
| Inactive 30+ (sport) | *(aggregate - skip)* | 75 |
| Day 30 - Freebet 100% up to 125 EUR | Day 30 - Freebet 100% up to 125 EUR | 83 |
| Day 32 - Freebet 100% up to 125 EUR reminded | Day 32 - Freebet 100% up to 125 EUR reminded | 91 |
| Day 45 - Deposit 100% up to 125 EUR | Day 45 - Deposit 100% up to 125 EUR | 99 |
| Day 47 - Deposit 100% up to 125 EUR reminder | Day 47 - Deposit 100% up to 125 EUR reminder | 107 |
| Day 60 - Freebet 100% up to 150 EUR | Day 60 - Freebet 100% up to 150 EUR | 115 |
| Day 62 - Freebet 100% up to 150 EUR reminder | Day 62 - Freebet 100% up to 150 EUR reminder | 123 |
| Day 90 - Deposit Bonus 150% up to 100 EUR | Day 90 - Deposit Bonus 150% up to 100 EUR | 131 |
| Day 92 - Deposit Bonus 150% up to 100 EUR reminder | Day 92 - Deposit Bonus 150% up to 100 EUR reminder | 139 |

---

## Target Excel Structure

### Sheets

1. **WP Chains Sport** - Welcome and retention campaigns
2. **AWOL Chains Sport** - Inactive user campaigns

### Week Column Structure

```python
# Week columns in target Excel (52 weeks, F-BE, reverse chronological)
# Only weeks 1-8 are currently supported
WEEK_COLUMNS = {
    '01': 'BE',  # 2026-01-05
    '02': 'BD',  # 2026-01-12
    '03': 'BC',  # 2026-01-19
    '04': 'BB',  # 2026-01-26
    '05': 'BA',  # 2026-02-02
    '06': 'AZ',  # 2026-02-09
    '07': 'AY',  # 2026-02-16
    '08': 'AX'   # 2026-02-23
}
```

### Row Structure

Each template occupies 8 rows:

| Row Offset | Metric | Description | Formula? |
|------------|--------|-------------|----------|
| +0 | Sent | Total emails sent | No |
| +1 | Delivered | Total emails delivered | No |
| +2 | Opened | Total emails opened | No |
| +3 | Clicked | Total clicks | No |
| +4 | Unsubscribed | Total unsubscribes | No |
| +5 | % Delivered | Delivered / Sent × 100 | **Yes** |
| +6 | % Open | Opened / Delivered × 100 | **Yes** |
| +7 | % Click | Clicked / Delivered × 100 | **Yes** |

**CRITICAL:** Only rows +0 to +4 should be written. Rows +5 to +7 contain Excel formulas and must be preserved.

### Aggregate Rows (Campaign Headers)

Rows with Column C = "All Mail" or "All Sport Mail" contain formulas that sum all templates below:

- **Retention 1 dep (sport)** - Row 51: `=SUM(F59, F67, F75, F83)` (sums 4 templates)
- **Retention 2 dep (sport)** - Row 91: `=SUM(F99, F107, F115, F123)` (sums 4 templates)
- **Inactive 7 (sport)** - Row 3: `=SUM(F11, F19)` (sums 2 templates)
- **Inactive 14 (sport)** - Row 27: `=SUM(F35, F43)` (sums 2 templates)
- **Inactive 21 (sport)** - Row 51: `=SUM(F59, F67)` (sums 2 templates)
- **Inactive 30+ (sport)** - Row 75: `=SUM(F83, F91, F99, F107, F115, F123, F131, F139)` (sums 8 templates)

**Exception:** Reg_No_Dep row 3 ("All Sport Mail") does NOT have formulas - it's actually a template row, not an aggregate.

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

## Key Differences from Other Report Types

### vs Casino-Ret
- ✅ Uses template-level granularity (not timing categories)
- ✅ Two target sheets (WP Chains Sport + AWOL Chains Sport)
- ✅ Different campaign names ("Retention 1 dep (sport)" vs "Ret 1 dep [SPORT] ⚽️")
- ✅ 8 metrics per template (vs 6 metrics per timing block)
- ✅ Has aggregate rows with formulas (must skip)

### vs AWOL
- ✅ Includes welcome/retention campaigns (not just inactive)
- ✅ Uses "Inactive X (sport)" naming (vs "Inactive X [SPORT] ⚽️")
- ✅ More granular templates (Day 30, Day 32, Day 45, etc.)
- ✅ Reg_No_Dep campaign filters by "Sport" keyword

---

## Implementation Notes

### Template Matching

Templates are matched by exact string comparison with Column B values in Excel:

```python
# CSV template_name must match Excel Column B exactly
csv_template = "Day 2 - Sport Welcome bonus "  # Note trailing space
excel_col_b = "Day 2 - Sport Welcome bonus "   # Must match exactly

# For Inactive templates, match by prefix (Excel has multi-line text)
csv_template = "Sport Inactive 7_1"
excel_col_b = "Sport Inactive 7_1\n\nOnlyWin Freebet 50% up to 150 EUR"
# Match using: csv_template in excel_col_b
```

### Formula Preservation

**DO NOT WRITE** to these rows:
1. Aggregate rows (Column C = "All Mail" or "All Sport Mail") - except Reg_No_Dep row 3
2. Percentage rows (rows +5, +6, +7 in each 8-row block)

**ONLY WRITE** to:
1. Template rows (Column C = "None")
2. Metric rows +0 to +4 (Sent, Delivered, Opened, Clicked, Unsubscribed)

### Week Replacement Logic

```python
def _replace_week(existing_excel, week_data, week_num):
    # 1. Load existing Excel (preserve formulas)
    wb = openpyxl.load_workbook(existing_excel, data_only=False)
    
    # 2. Get target column
    target_col = WEEK_COLUMNS[week_num]  # e.g., '07' -> 'AY'
    
    # 3. For each campaign:
    for campaign_name, templates in week_data.items():
        # 3a. SKIP aggregate row if has_aggregate_row=True
        
        # 3b. For each template:
        for template_name, metrics in templates.items():
            # Find template row by matching Column B
            template_row = find_template_row(ws, template_name)
            
            # Write only first 5 metrics (rows +0 to +4)
            for offset in range(5):
                ws[f'{target_col}{template_row + offset}'].value = metrics[offset]
    
    # 4. Save (formulas preserved)
    wb.save(existing_excel)
```

---

## Summary

### Key Features

✅ **Multi-file processing** - Handles 7 CSV files  
✅ **Campaign-based detection** - Uses campaign_name column  
✅ **Template-level granularity** - Each template gets its own 8-row block  
✅ **Two target sheets** - WP Chains Sport + AWOL Chains Sport  
✅ **Week replacement** - Updates specific weeks in existing reports  
✅ **Formula preservation** - Skips aggregate rows and percentage rows  
  

### Output

- **Target Sheets:** `WP Chains Sport`, `AWOL Chains Sport`
- **Campaigns:** 7 (1 signup, 2 retention, 4 inactive)
- **Templates:** 27 total (6 RND, 4 Ret1, 4 Ret2, 2 Inactive7, 2 Inactive14, 2 Inactive21, 8 Inactive30+) - Note: 1 aggregate row per campaign except RND
- **Metrics per Template:** 8 rows (5 data + 3 formula)
- **Week Columns:** 52 total (8 supported: BE-AX)
- **Detection Method:** Campaign-based (from campaign_name column)

### Metrics Tracked

- **Sent** - Total emails sent
- **Delivered** - Total emails delivered
- **Opened** - Total emails opened
- **Clicked** - Total clicks
- **Unsubscribed** - Total unsubscribes
- **% Delivered** - Formula: `=Delivered/Sent*100`
- **% Open** - Formula: `=Opened/Delivered*100`
- **% Click** - Formula: `=Clicked/Delivered*100`
