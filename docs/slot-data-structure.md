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

| File | Campaign Name | Description |
|------|---------------|-------------|
| `SLOT_rnd_feb15.csv` | `Reg_No_Dep (casino/sport)` | New user signups (4462 rows) |
| `SLOT_ret1_feb15.csv` | `Retention 1 dep (sport)` | 1st deposit retention (920 rows) |
| `SLOT_ret2_feb15.csv` | `Retention 2 dep (sport)` | 2nd deposit retention (920 rows) |
| `SLOT_inactive7_feb15.csv` | `Inactive 7 (sport)` | 7 days inactive (460 rows) |
| `SLOT_inactive14_feb15.csv` | `Inactive 14 (sport)` | 14 days inactive (460 rows) |
| `SLOT_inactive21_feb15.csv` | `Inactive 21 (sport)` | 21 days inactive (460 rows) |
| `SLOT_inactive30_feb15.csv` | `Inactive 30+ (sport)` | 30+ days inactive (1886 rows) |

### Required Columns

| Column | Type | Description |
|--------|------|-------------|
| `timestamp` | Unix timestamp | Campaign send time (seconds since epoch) |
| `template_name` | String | Template identifier (e.g., "Day 2 - Sport Welcome bonus") |
| `campaign_name` | String | **Campaign identifier** (e.g., "Reg_No_Dep (casino/sport)") |
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
    "Reg_No_Dep (casino/sport)": {
        "sheet": "WP Chains Sport",
        "start_row": 3,
        "filter": "Sport",  # C="All Sport Mail" - filter templates containing "Sport"
        "label": "Reg_No_Dep (casino/sport)"
    },
    "Retention 1 dep (sport)": {
        "sheet": "WP Chains Sport",
        "start_row": 51,
        "filter": None,  # C="All Mail" - all templates
        "label": "Retention 1 dep (sport)"
    },
    "Retention 2 dep (sport)": {
        "sheet": "WP Chains Sport",
        "start_row": 91,
        "filter": None,  # C="All Mail" - all templates
        "label": "Retention 2 dep (sport)"
    },
    "Inactive 7 (sport)": {
        "sheet": "AWOL Chains Sport",
        "start_row": 3,
        "filter": None,  # C="All Mail" - all templates
        "label": "Inactive 7 (sport)"
    },
    "Inactive 14 (sport)": {
        "sheet": "AWOL Chains Sport",
        "start_row": 27,
        "filter": None,  # C="All Mail" - all templates
        "label": "Inactive 14 (sport)"
    },
    "Inactive 21 (sport)": {
        "sheet": "AWOL Chains Sport",
        "start_row": 51,
        "filter": None,  # C="All Mail" - all templates
        "label": "Inactive 21 (sport)"
    },
    "Inactive 30+ (sport)": {
        "sheet": "AWOL Chains Sport",
        "start_row": 75,
        "filter": None,  # C="All Mail" - all templates
        "label": "Inactive 30+ (sport)"
    }
}
```

### Detection Logic

1. Read `campaign_name` from CSV
2. Exact match against known campaigns
3. Determine target sheet and starting row
4. Apply template filter if specified ("Sport" keyword or None for all)

**Benefits:**
- ✅ Filename independent
- ✅ Clear sheet routing
- ✅ Template filtering per campaign
- ✅ Reliable and maintainable

---

## Target Excel Structure

### Sheets

1. **WP Chains Sport** - Welcome and retention campaigns
   - Reg_No_Dep (casino/sport) - Row 3
   - Retention 1 dep (sport) - Row 51
   - Retention 2 dep (sport) - Row 91

2. **AWOL Chains Sport** - Inactive user campaigns
   - Inactive 7 (sport) - Row 3
   - Inactive 14 (sport) - Row 27
   - Inactive 21 (sport) - Row 51
   - Inactive 30+ (sport) - Row 75

### Column Structure

- **Column A**: Metric names (Sent, Delivered, Open, Click, Unsub, Spam, Open Rate, Click Rate)
- **Column B**: Campaign name OR template name
- **Column C**: Filter indicator
  - **"All Sport Mail"**: Aggregate only templates containing "Sport" (case-insensitive)
  - **"All Mail"**: Aggregate all templates (Note: future may add channel=email filter)
  - **"None"**: Individual template row
- **Columns D-E**: Additional metadata
- **Columns F-P**: Week data (11 weeks)

### Week Column Structure

```python
# Week columns in target Excel (F-BE = 52 weeks)
# Headers contain dates starting from 2026-12-21 (most recent) going back to 2026-01-05
# Column F: 2026-12-21 (Week 52)
# Column G: 2026-12-14 (Week 51)
# ...
# Column BE: 2026-01-05 (Week 1)

WEEK_COLUMNS = {
    'week1': 'BE',   # 2026-01-05
    'week2': 'BD',   # 2026-01-12
    'week3': 'BC',   # 2026-01-19
    'week4': 'BB',   # 2026-01-26
    'week5': 'BA',   # 2026-02-02
    'week6': 'AZ',   # 2026-02-09
    'week7': 'AY',   # 2026-02-16
    'week8': 'AX',   # 2026-02-23
    # ... continues to week 52 in column F
}
```

### Section Structure

#### WP Chains Sport Sheet

```
Row 3:  B="Reg_No_Dep (casino/sport)"  C="All Sport Mail"  → Filter: Sport templates only
Row 11:   B="Day 2 - Sport Welcome bonus"  C="None"
Row 19:   B="Day 4 - Sport Welcome bonus reminder"  C="None"
Row 27:   B="Day 13 - Sport Welcome boost bonus"  C="None"
Row 35:   B="Day 15 - Sport Welcome boost bonus reminder"  C="None"
Row 43:   B="Day 20 - Sport Highroller"  C="None"

Row 51: B="Retention 1 dep (sport)"  C="All Mail"  → Filter: All templates
Row 59:   B="Day 1 - Bonus on 2nd deposit"  C="None"
Row 67:   B="Day 3 - Bonus on 2nd deposit reminder"  C="None"
Row 75:   B="Day 5 - Welcome boost dep bonus"  C="None"
Row 83:   B="Day 8 - Welcome boost dep bonus reminder"  C="None"

Row 91: B="Retention 2 dep (sport)"  C="All Mail"  → Filter: All templates
Row 99:   B="Day 1 - Bonus on 3nd deposit"  C="None"
Row 107:  B="Day 3 - Bonus on 3nd deposit reminder"  C="None"
Row 115:  B="Day 5 - Welcome boost dep bonus"  C="None"
Row 123:  B="Day 8 - Welcome boost dep bonus reminder"  C="None"
```

#### AWOL Chains Sport Sheet

```
Row 3:  B="Inactive 7 (sport)"  C="All Mail"  → Filter: All templates
Row 11:   B="Sport Inactive 7_1\nOnlyWin Freebet 50% up to 150 EUR"  C="None"
Row 19:   B="Sport Inactive 7_2\nAllWin Freebet 50% up to 100 EUR"  C="None"

Row 27: B="Inactive 14 (sport)"  C="All Mail"  → Filter: All templates
Row 35:   B="Sport Inactive 14_1\nNoRisk Freebet 70% up to 125 EUR"  C="None"
Row 43:   B="Sport Inactive 14_2\n80% up to 125 EUR"  C="None"

Row 51: B="Inactive 21 (sport)"  C="All Mail"  → Filter: All templates
Row 59:   B="Sport Inactive 21_1\nAllWin Freebet 100% up to 70 EUR"  C="None"
Row 67:   B="Sport Inactive 21_2\n100% up to 150 EUR"  C="None"

Row 75: B="Inactive 30+ (sport)"  C="All Mail"  → Filter: All templates
Row 83:   B="Day 30 - Freebet 100% up to 125 EUR"  C="None"
Row 91:   B="Day 32 - Freebet 100% up to 125 EUR reminded"  C="None"
Row 99:   B="Day 45 - Deposit 100% up to 125 EUR"  C="None"
Row 107:  B="Day 47 - Deposit 100% up to 125 EUR reminder"  C="None"
Row 115:  B="Day 60 - Freebet 100% up to 150 EUR"  C="None"
Row 123:  B="Day 62 - Freebet 100% up to 150 EUR reminder"  C="None"
Row 131:  B="Day 90 - Deposit Bonus 150% up to 100 EUR"  C="None"
Row 139:  B="Day 92 - Deposit Bonus 150% up to 100 EUR reminder"  C="None"
```

### Metrics per Template

Each template row contains 8 metrics (similar to AWOL):

| Metric | Description |
|--------|-------------|
| Sent | Total emails sent |
| Delivered | Total emails delivered |
| Opened | Total emails opened |
| Clicked | Total clicks |
| Unsubscribed | Total unsubscribes |
| % Delivered | Delivered / Sent × 100 |
| % Open | Opened / Delivered × 100 |
| % Click | Clicked / Delivered × 100 |

---

## Key Differences from Other Report Types

### vs Casino-Ret
- ✅ Uses template-level granularity (not timing categories)
- ✅ Two target sheets (WP Chains Sport + AWOL Chains Sport)
- ✅ Different campaign names ("Retention 1 dep (sport)" vs "Ret 1 dep [SPORT] ⚽️")
- ✅ 8 metrics per template (vs 6 metrics per timing block)

### vs AWOL
- ✅ Includes welcome/retention campaigns (not just inactive)
- ✅ Uses "Inactive X (sport)" naming (vs "Inactive X [SPORT] ⚽️")
- ✅ More granular templates (Day 30, Day 32, Day 45, etc.)

---

## Implementation Plan

### 1. Plugin Structure

```python
@register_plugin
class SlotPlugin(BaseReportPlugin):
    name = "slot"
    supports_multiple_files = True
    
    def process_csv(self, csv_paths: List[Path]) -> Dict[str, pd.DataFrame]:
        # Read and group by campaign_name
        pass
    
    def transform_data(self, data_files: Dict[str, pd.DataFrame]) -> Dict:
        # Aggregate by weeks and templates
        pass
    
    def generate_excel(self, report_data: Dict, output_path: Path):
        # Populate two sheets: WP Chains Sport + AWOL Chains Sport
        pass
```

### 2. Campaign Detection

```python
def detect_campaign(campaign_name: str) -> dict:
    if campaign_name in SLOT_CAMPAIGN_MAPPINGS:
        return SLOT_CAMPAIGN_MAPPINGS[campaign_name]
    
    # Fuzzy matching
    if "reg_no_dep" in campaign_name.lower():
        return SLOT_CAMPAIGN_MAPPINGS["Reg_No_Dep (casino/sport)"]
    elif "retention 1" in campaign_name.lower():
        return SLOT_CAMPAIGN_MAPPINGS["Retention 1 dep (sport)"]
    # ... etc
```

### 3. Template Filtering

Slot uses Column C to determine filtering logic:

```python
# C="All Sport Mail" - filter by "Sport" keyword (case-insensitive)
if col_c == "All Sport Mail":
    filtered = df[df['template_name'].str.contains('Sport', case=False, na=False)]
    # Includes: "Day 2 - Sport Welcome bonus", "Day 15 - Sport Welcome boost bonus reminder"
    # Excludes: "Day 1 (10 min)", "Day 2", "Day 4"

# C="All Mail" - include all templates
# Note: Future enhancement may add channel=email filter
if col_c == "All Mail":
    filtered = df  # All templates from campaign

# C="None" - match exact template name from Column B
if col_c == "None":
    filtered = df[df['template_name'] == col_b_value]
```

### 4. Week Aggregation

Same as other report types - uses shared WEEKLY_BOUNDARIES from `plugins/constants.py`.

---

## Summary

### Key Features

✅ **Multi-file processing** - Handles 7 CSV files  
✅ **Campaign-based detection** - Uses campaign_name column  
✅ **Template-level granularity** - Each template gets its own row block  
✅ **Two target sheets** - WP Chains Sport + AWOL Chains Sport  
✅ **Week aggregation** - Groups data into 8 weekly periods  
✅ **8 metrics per template** - Includes percentages  

### Output

- **Target Sheets:** `WP Chains Sport`, `AWOL Chains Sport`
- **Campaigns:** 7 (1 signup, 2 retention, 4 inactive)
- **Templates:** Variable per campaign (2-8 templates each)
- **Metrics per Template:** 8 rows
- **Week Columns:** 11 (F-P)
- **Detection Method:** Campaign-based (from campaign_name column)

### Metrics Tracked

- **Sent** - Total emails sent
- **Delivered** - Total emails delivered
- **Opened** - Total emails opened
- **Clicked** - Total clicks
- **Unsubscribed** - Total unsubscribes
- **% Delivered** - Delivered / Sent × 100
- **% Open** - Opened / Delivered × 100
- **% Click** - Clicked / Delivered × 100
