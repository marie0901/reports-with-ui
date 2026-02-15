# Campaign-Based Mapping Proposal

## Problem Statement

Current implementation relies on **filename patterns** to detect report sections, which causes issues:

❌ **Current Issues:**
- `ret1feb15.csv` - Contains "1" in multiple places (ret**1**, **15**)
- `ret2feb15.csv` - Contains both "1" (from **15**) and "2" (ret**2**, 1**5**)
- Files with dates like "feb15", "jan12" cause ambiguous matches
- Ret 2 data gets processed as Ret 1 because "15" contains "1"

✅ **Solution:**
Use `campaign_name` column from CSV instead of filename patterns.

---

## Campaign Name Analysis

### Discovered Campaign Names

| CSV File | Campaign Name | Current Detection | Proposed Detection |
|----------|---------------|-------------------|-------------------|
| `5-26casinosport.csv` | `casino+sport A/B Reg_No_Dep` | Filename contains "casinosport" | Campaign contains "casino+sport" |
| `5-26_ret1.csv` | `Ret 1 dep [SPORT] ⚽️` | Filename contains "ret" + "1" | Campaign contains "Ret 1 dep" |
| `5-26_ret2.csv` | `Ret 2 dep [SPORT] ⚽️` | Filename contains "ret" + "2" | Campaign contains "Ret 2 dep" |
| `5-26_inactive7.csv` | `Inactive 7 [SPORT] ⚽️` | Filename contains "inactive7" | Campaign contains "Inactive 7" |
| `5-26_inactive14.csv` | `Inactive 14 [SPORT] ⚽️` | Filename contains "inactive14" | Campaign contains "Inactive 14" |
| `5-26_inactive22.csv` | `Inactive 22 [SPORT] ⚽️` | Filename contains "inactive22" | Campaign contains "Inactive 22" |
| `5-26_inactive31.csv` | `Inactive 31+ [SPORT] ⚽️` | Filename contains "inactive31" | Campaign contains "Inactive 31" |

---

## Proposed Campaign Mappings

### Casino-Ret Report Type

```python
CAMPAIGN_MAPPINGS = {
    # Casino/Sport A/B campaigns → Section 1 (Row 3)
    "casino+sport A/B Reg_No_Dep": {
        "section": "casino",
        "start_row": 3,
        "label": "casino+sport A/B Reg_No_Dep",
        "template_mappings": CASINOSPORT_MAPPINGS
    },
    
    # Retention 1 campaigns → Section 2 (Row 75)
    "Ret 1 dep [SPORT] ⚽️": {
        "section": "retention_1",
        "start_row": 75,
        "label": "Ret 1 dep [SPORT] ⚽️",
        "template_mappings": RETENTION_MAPPINGS
    },
    
    # Retention 2 campaigns → Section 3 (Row 123)
    "Ret 2 dep [SPORT] ⚽️": {
        "section": "retention_2",
        "start_row": 123,
        "label": "Ret 2 dep [SPORT] ⚽️",
        "template_mappings": RETENTION_MAPPINGS
    }
}
```

### AWOL Report Type

```python
AWOL_CAMPAIGN_MAPPINGS = {
    "Inactive 7 [SPORT] ⚽️": {
        "timing_category": "7d",
        "label": "Inactive 7 days"
    },
    "Inactive 14 [SPORT] ⚽️": {
        "timing_category": "14d",
        "label": "Inactive 14 days"
    },
    "Inactive 22 [SPORT] ⚽️": {
        "timing_category": "22d",
        "label": "Inactive 22 days"
    },
    "Inactive 31+ [SPORT] ⚽️": {
        "timing_category": "31d",
        "label": "Inactive 31+ days"
    }
}
```

---

## Implementation Strategy

### Step 1: Group Files by Campaign

```python
def group_by_campaign(data_files: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """Group CSV data by campaign_name instead of filename."""
    campaign_groups = {}
    
    for file_name, df in data_files.items():
        if df.empty or 'campaign_name' not in df.columns:
            logger.warning(f"Skipping {file_name}: no campaign_name column")
            continue
        
        campaign_name = df['campaign_name'].iloc[0]
        
        if campaign_name in campaign_groups:
            # Append to existing campaign data
            campaign_groups[campaign_name] = pd.concat([campaign_groups[campaign_name], df])
        else:
            campaign_groups[campaign_name] = df
    
    return campaign_groups
```

### Step 2: Detect Section by Campaign Name

```python
def detect_section(campaign_name: str) -> dict:
    """Detect report section based on campaign name."""
    
    # Exact match first
    if campaign_name in CAMPAIGN_MAPPINGS:
        return CAMPAIGN_MAPPINGS[campaign_name]
    
    # Fuzzy match for variations
    campaign_lower = campaign_name.lower()
    
    if "casino+sport" in campaign_lower or "a/b" in campaign_lower:
        return CAMPAIGN_MAPPINGS["casino+sport A/B Reg_No_Dep"]
    elif "ret 1 dep" in campaign_lower:
        return CAMPAIGN_MAPPINGS["Ret 1 dep [SPORT] ⚽️"]
    elif "ret 2 dep" in campaign_lower:
        return CAMPAIGN_MAPPINGS["Ret 2 dep [SPORT] ⚽️"]
    
    logger.warning(f"Unknown campaign: {campaign_name}")
    return None
```

### Step 3: Process by Campaign

```python
def transform_data(self, data_files: Dict[str, pd.DataFrame]) -> Dict[str, Dict[str, pd.DataFrame]]:
    """Transform data grouped by campaign."""
    
    # Group by campaign instead of filename
    campaign_groups = self.group_by_campaign(data_files)
    
    report_data = {}
    
    for campaign_name, data in campaign_groups.items():
        section_config = self.detect_section(campaign_name)
        
        if not section_config:
            continue
        
        # Use campaign-specific template mappings
        mappings = section_config["template_mappings"]
        
        # Filter and aggregate
        filtered = data[data['template_name'].isin(mappings.keys())]
        weekly_data = self._aggregate_by_weeks(filtered)
        
        # Group by timing category
        campaign_report = {}
        for template_name, timing_category in mappings.items():
            timing_data = {}
            for week_key, week_df in weekly_data.items():
                template_data = week_df[week_df['template_name'] == template_name]
                if not template_data.empty:
                    template_data = self._calculate_percentages(template_data)
                    timing_data[week_key] = template_data
                else:
                    timing_data[week_key] = self._empty_data(template_name)
            campaign_report[timing_category] = timing_data
        
        report_data[campaign_name] = campaign_report
    
    return report_data
```

### Step 4: Populate Sections by Campaign

```python
def generate_excel(self, report_data: Dict[str, Dict[str, pd.DataFrame]], output_path: Path):
    """Generate Excel using campaign-based routing."""
    wb = Workbook()
    ws = wb.active
    
    # Headers
    # ... (same as before)
    
    # Populate sections by campaign
    for campaign_name, section_data in report_data.items():
        section_config = self.detect_section(campaign_name)
        
        if not section_config:
            continue
        
        self._populate_section(
            ws,
            section_data,
            section_config["start_row"],
            section_config["label"],
            section_config["section"]
        )
    
    wb.save(output_path)
```

---

## Benefits

### 1. Filename Independence
✅ Works with any filename: `5-26_ret1.csv`, `ret1feb15.csv`, `retention_1_data.csv`  
✅ No ambiguous number matching  
✅ No need to rename files

### 2. Reliable Detection
✅ Based on actual data content, not filename conventions  
✅ Handles campaign name variations (case-insensitive, fuzzy matching)  
✅ Clear error messages when campaign is unknown

### 3. Multi-File Support
✅ Multiple files can contain same campaign (auto-merged)  
✅ Single file can contain multiple campaigns (auto-split)  
✅ Flexible file organization

### 4. Maintainability
✅ Single source of truth: campaign names in CSV  
✅ Easy to add new campaigns  
✅ No complex filename parsing logic

---

## Migration Path

### Phase 1: Add Campaign Detection (Backward Compatible)
```python
# Try campaign-based detection first
section_config = self.detect_section_by_campaign(data)

# Fallback to filename detection
if not section_config:
    section_config = self.detect_section_by_filename(file_name)
```

### Phase 2: Deprecate Filename Detection
- Log warnings when filename detection is used
- Update documentation to recommend campaign-based approach

### Phase 3: Remove Filename Detection
- Remove all filename-based logic
- Rely solely on campaign names

---

## Testing

### Test Cases

```python
# Test 1: Exact campaign match
assert detect_section("Ret 1 dep [SPORT] ⚽️")["start_row"] == 75

# Test 2: Case-insensitive match
assert detect_section("ret 1 dep [sport] ⚽️")["start_row"] == 75

# Test 3: Fuzzy match
assert detect_section("Ret 1 deposit [SPORT]")["start_row"] == 75

# Test 4: Multiple files, same campaign
files = ["file1.csv", "file2.csv"]  # Both contain "Ret 1 dep"
groups = group_by_campaign(files)
assert len(groups) == 1  # Merged into single campaign

# Test 5: Single file, multiple campaigns
# Should split into separate campaign groups
```

---

## Summary

### Current (Filename-Based)
```python
if "ret" in filename and "1" in filename:  # ❌ Ambiguous
    section = "retention_1"
```

### Proposed (Campaign-Based)
```python
if "Ret 1 dep" in campaign_name:  # ✅ Reliable
    section = "retention_1"
```

### Impact
- ✅ Fixes Ret 2 detection issue
- ✅ Works with any filename format
- ✅ More maintainable and reliable
- ✅ Backward compatible (can add fallback)
- ✅ Easier to test and debug
