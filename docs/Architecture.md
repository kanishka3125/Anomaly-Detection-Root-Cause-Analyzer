# SYSTEM ARCHITECTURE DOCUMENT
## AI Data Anomaly Detection & Root Cause Analyzer

**Version:** 1.0  
**Status:** Final  
**Last Updated:** April 2026  

---

## 1. ARCHITECTURE OVERVIEW

### 1.1 High-Level Architecture Philosophy
This system follows a **layered architecture** designed for simplicity, maintainability, and rapid development. Each layer has a single responsibility, enabling easy testing and future enhancements.

**Key Design Principle:** Simple, stateless, local-processing pipeline with no external dependencies.

### 1.2 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER (Streamlit)               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  UI Components: File Upload, Data Preview, Dashboard    │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────────┘
                     │ (Data Flow)
┌────────────────────▼────────────────────────────────────────────┐
│              DATA PROCESSING LAYER (Pandas/NumPy)               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  CSV Loading → Validation → Cleaning → Preprocessing    │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────────┐
│         ANOMALY DETECTION ENGINE (Z-Score Algorithm)            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Calculate Mean → Std Dev → Z-Scores → Classification  │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────────┐
│         EXPLANATION ENGINE (Rule-Based Logic)                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Generate Severity → Create Description → Context Data  │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────────┐
│        VISUALIZATION LAYER (Matplotlib)                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Time-Series Chart → Distribution Plot → Box Plot       │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. SYSTEM COMPONENTS

### 2.1 Presentation Layer (Streamlit UI)

**Responsibility:** User-facing interface for interaction and results display

**Key Components:**
- **File Upload Widget:** Accept CSV files, validate file size
- **Data Preview Table:** Display first few rows with column info
- **Column Selector:** Let user choose which column to analyze
- **Sensitivity Slider:** Adjust Z-score threshold (1.5 to 4.0)
- **Results Dashboard:** Multi-tab display of results
- **Export Buttons:** Download CSV/PNG/PDF

**Technology:** Streamlit 1.20+

**Key Features:**
```
- st.file_uploader() → Handle CSV uploads
- st.dataframe() → Display data tables
- st.slider() → Adjust sensitivity threshold
- st.tabs() → Organize results into sections
- st.download_button() → Export functionality
```

**Dependencies on Other Layers:**
- Calls Data Processing Layer for file validation
- Calls Anomaly Detection Engine for analysis
- Calls Visualization Layer for charts
- Calls Explanation Engine for descriptions

---

### 2.2 Data Processing Layer (Pandas/NumPy)

**Responsibility:** Load, validate, and prepare data for analysis

**Subcomponents:**

#### 2.2.1 File I/O Module
- **Function:** `load_csv(file_path) → DataFrame`
- **Input:** CSV file (string path or file object)
- **Output:** Pandas DataFrame
- **Validation:**
  - File size < 10MB
  - Valid CSV structure
  - Readable encoding (UTF-8, Latin-1)
  - Non-empty data

**Error Handling:**
```
- FileNotFoundError → Prompt user to re-upload
- EncodingError → Try alternative encodings
- EmptyDataError → Show error message
- CSVError (malformed) → Display parsing error
```

#### 2.2.2 Data Validation Module
- **Function:** `validate_data(df) → (bool, str)`
- **Checks:**
  - Minimum 10 rows (statistical validity)
  - At least one numeric column
  - Column names are valid (no duplicates)
  - No completely empty columns (> 90% null)

**Return:** (is_valid, error_message)

#### 2.2.3 Data Cleaning Module
- **Function:** `clean_data(df, column) → Series`
- **Operations:**
  - Remove rows with NaN in selected column
  - Convert to numeric type (coerce errors)
  - Remove infinite values (np.inf, -np.inf)
  - Return clean series for analysis

**Preprocessing Steps:**
1. Drop rows where value is NaN
2. Drop rows where value is infinite
3. Ensure numeric type (float64)
4. Return clean Series

---

### 2.3 Anomaly Detection Engine (Z-Score Algorithm)

**Responsibility:** Identify anomalous data points using statistical method

**Algorithm:** Z-Score Based Anomaly Detection

**Mathematical Foundation:**
```
Z-score = (x - μ) / σ

Where:
  x = individual data point
  μ = mean of dataset
  σ = standard deviation of dataset
  
Anomaly if |Z-score| > threshold (default: 3.0)
```

**Key Functions:**

#### 2.3.1 Calculate Statistics
```python
def calculate_stats(data):
    """
    Compute mean, std dev, min, max for data
    Input: Series of numeric values
    Output: dict with statistics
    """
    return {
        'mean': np.mean(data),
        'std': np.std(data),
        'min': np.min(data),
        'max': np.max(data),
        'median': np.median(data),
        'q1': np.percentile(data, 25),
        'q3': np.percentile(data, 75),
        'iqr': np.percentile(data, 75) - np.percentile(data, 25)
    }
```

#### 2.3.2 Calculate Z-Scores
```python
def calculate_zscore(data, mean, std):
    """
    Calculate Z-score for each value
    Handles edge case: std = 0 (constant values)
    If std = 0, return Z-score = 0 (not anomalous)
    """
    if std == 0:
        return np.zeros(len(data))
    return np.abs((data - mean) / std)
```

#### 2.3.3 Detect Anomalies
```python
def detect_anomalies(zscores, threshold=3.0):
    """
    Binary classification: anomaly (True) or normal (False)
    """
    return zscores > threshold
```

**Parameters:**
- **Threshold (Default: 3.0):** Corresponds to ~0.3% of data in normal distribution
- **Adjustable Range:** 1.5 to 4.0 (via Streamlit slider)
  - 1.5σ = Sensitive (catches ~13% of normal data as anomalies)
  - 2.0σ = Moderate (~5% false positive rate)
  - 3.0σ = Conservative (~0.3% false positive rate)
  - 4.0σ = Very conservative (~0.006% false positive rate)

**Output:**
```python
{
    'zscores': array,        # Z-score for each row
    'is_anomaly': array,     # Boolean array
    'anomaly_count': int,    # Total anomalies detected
    'anomaly_percent': float # % of data that is anomalous
}
```

---

### 2.4 Explanation Engine (Rule-Based Logic)

**Responsibility:** Generate human-readable explanations for detected anomalies

**Key Features:**
- Severity classification (Mild, Moderate, Severe)
- Context-aware descriptions
- Comparative statistics
- Non-technical language

**Explanation Rules:**

#### Rule 1: Severity Classification
```
IF zscore between 3.0 and 3.5:
    severity = "MILD"
    multiplier = "3.0-3.5 times"
    
ELIF zscore between 3.5 and 4.5:
    severity = "MODERATE"
    multiplier = "3.5-4.5 times"
    
ELIF zscore > 4.5:
    severity = "SEVERE"
    multiplier = "> 4.5 times"
```

#### Rule 2: Direction-Based Description
```
IF value > mean:
    direction = "SPIKE"
    description = f"Value is {percent_above_mean}% above normal"
    
ELIF value < mean:
    direction = "DIP"
    description = f"Value is {percent_below_mean}% below normal"
```

#### Rule 3: Context Description
```
Full explanation = 
    f"[SEVERITY] {direction}: {description}"
    + f"Normal range: {mean ± std}"
    + f"Actual value: {value}"
    + f"Deviation: {zscore:.2f}σ"
```

**Example Output:**
```
SEVERE SPIKE: Value is 450% above normal range.
Expected: 100 ± 20 (80-120)
Actual: 550
Deviation: 4.8 standard deviations above mean
```

**Key Function:**
```python
def generate_explanation(row_value, mean, std, zscore):
    """
    Generate human-readable explanation for anomaly
    Returns: dict with severity, direction, full_text
    """
    severity = classify_severity(zscore)
    direction = classify_direction(row_value, mean)
    percent_change = abs((row_value - mean) / mean * 100)
    
    return {
        'severity': severity,
        'direction': direction,
        'zscore_magnitude': zscore,
        'percent_from_mean': percent_change,
        'explanation': f"{severity} {direction}: "
                      f"{percent_change:.1f}% from normal. "
                      f"Expected: {mean:.2f} ± {std:.2f}"
    }
```

---

### 2.5 Visualization Layer (Matplotlib)

**Responsibility:** Create publication-quality visualizations of results

**Chart Types:**

#### 2.5.1 Time-Series Line Plot
- X-axis: Row index or timestamp
- Y-axis: Data values
- Normal points: Blue line
- Anomalous points: Red scatter points
- Features:
  - Mean line (dashed green)
  - Upper/lower bounds (mean ± 3σ, shaded)
  - Legend and labels
  - Title and gridlines

**Code Structure:**
```python
def plot_timeseries(data, is_anomaly, mean, std):
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot normal points
    ax.plot(data[~is_anomaly], label='Normal', color='blue')
    
    # Plot anomalies
    ax.scatter(np.where(is_anomaly)[0], 
               data[is_anomaly], 
               color='red', label='Anomaly', s=50)
    
    # Add reference lines
    ax.axhline(mean, color='green', linestyle='--', label='Mean')
    ax.axhline(mean + 3*std, color='orange', linestyle=':', alpha=0.7)
    ax.axhline(mean - 3*std, color='orange', linestyle=':', alpha=0.7)
    
    ax.legend()
    ax.set_title('Time-Series Anomaly Detection')
    ax.set_xlabel('Data Point Index')
    ax.set_ylabel('Value')
    
    return fig
```

#### 2.5.2 Distribution Histogram
- Bins: 30-50 (auto)
- Normal data: Blue bars
- Anomalies: Red overlay
- Features:
  - Mean and std dev lines
  - Quartile markers (Q1, Q3)
  - Density curve (optional)

#### 2.5.3 Box Plot
- Shows quartiles, median, IQR
- Whiskers at 1.5×IQR
- Outlier points marked separately
- Clear visualization of data spread

#### 2.5.4 Statistical Summary Panel
- Text-based display of:
  - Total records and anomalies
  - Anomaly percentage
  - Mean, std dev, min, max
  - Sensitivity threshold
  - Detection threshold values

---

### 2.6 Results Aggregation & Output

**Responsibility:** Combine all layers and format final output

**Output Structure:**
```python
results = {
    'summary': {
        'total_records': int,
        'total_anomalies': int,
        'anomaly_percent': float,
        'mean': float,
        'std': float,
        'threshold': float
    },
    'details': {
        'data': DataFrame,           # Original + anomaly flags
        'statistics': dict,
        'zscores': array,
        'explanations': list[str]
    },
    'visualizations': {
        'timeseries': matplotlib_fig,
        'histogram': matplotlib_fig,
        'boxplot': matplotlib_fig
    }
}
```

---

## 3. DATA FLOW

### 3.1 Complete End-to-End Flow

```
Step 1: USER UPLOADS FILE
        ↓
Step 2: STREAMLIT receives file
        ↓ [Data Processing Layer]
Step 3: Load CSV → Validate format → Check file size
        ↓
Step 4: Check for numeric columns → Validate row count
        ↓ DISPLAY: Data Preview (first 5 rows)
        ↓
Step 5: USER SELECTS COLUMN & SENSITIVITY
        ↓
Step 6: USER CLICKS "ANALYZE"
        ↓ [Data Cleaning]
Step 7: Remove NaN values → Remove infinite values → Ensure numeric type
        ↓ [Anomaly Detection Engine]
Step 8: Calculate mean, std dev
        ↓
Step 9: Calculate Z-scores for each value
        ↓
Step 10: Compare Z-scores to threshold → Create anomaly labels
        ↓ [Explanation Engine]
Step 11: For each anomaly:
         - Classify severity (Mild/Moderate/Severe)
         - Determine direction (Spike/Dip)
         - Generate explanation text
        ↓ [Visualization Layer]
Step 12: Create time-series chart (with anomalies highlighted)
        ↓
Step 13: Create histogram and box plot
        ↓
Step 14: Format results and statistics
        ↓ [Back to Presentation Layer]
Step 15: DISPLAY RESULTS DASHBOARD:
         - Summary statistics
         - Visualizations
         - Detailed anomaly table
         - Explanations
        ↓
Step 16: USER CAN EXPORT (CSV/PNG)
        ↓
Step 17: END
```

### 3.2 Data Transformation Journey

```
INPUT: CSV File (raw bytes)
  ↓
AFTER LOADING: Pandas DataFrame
  ↓
AFTER CLEANING: Pandas Series (clean numeric values)
  ↓
AFTER Z-SCORE CALC: NumPy Array (Z-score values)
  ↓
AFTER CLASSIFICATION: NumPy Array (boolean: anomaly Y/N)
  ↓
AFTER EXPLANATION: List of dicts (anomaly details + explanations)
  ↓
AFTER VISUALIZATION: Matplotlib Figures (PNG images)
  ↓
OUTPUT: Dashboard Display + Export Files
```

---

## 4. TECHNOLOGY CHOICES & RATIONALE

### 4.1 Core Technologies

| Technology | Why Chosen | Alternatives Considered |
|------------|-----------|------------------------|
| **Python 3.8+** | Industry standard for data science; rapid development | Java, C++ (overkill) |
| **Streamlit** | Fastest way to build data UI; minimal boilerplate | Flask, Django, Dash |
| **Pandas** | Best for CSV handling and data manipulation | SQL, raw NumPy |
| **NumPy** | Efficient numerical computations; Z-score math | Scipy (heavier) |
| **Matplotlib** | Lightweight visualization; good for static charts | Plotly, ggplot (overkill) |
| **SciPy** | Statistical functions (if needed); percentiles | Custom implementation |

### 4.2 Why NOT Other Approaches

**Why not Deep Learning?**
- Overkill for statistical anomaly detection
- Requires labeled training data (don't have it)
- Takes hours to train models
- Z-score is fast, interpretable, proven

**Why not Isolation Forest?**
- More complex algorithm
- Requires scikit-learn (additional dependency)
- Z-score sufficient for 6-hour MVP
- Easy to add later if needed

**Why not Real-time Streaming?**
- Out of scope for MVP
- Requires streaming library (Kafka, Spark)
- Can be added in Phase 2
- Local CSV processing sufficient for now

**Why not Cloud Deployment?**
- Adds deployment complexity
- Requires DevOps (Docker, K8s)
- No value-add for MVP
- Local processing is actually more private

---

## 5. DESIGN DECISIONS

### 5.1 Single Column Analysis (MVP)
**Decision:** Analyze one numeric column at a time

**Rationale:**
- Simpler UI/UX for users
- Faster implementation (6 hours)
- Easier to explain results
- Multi-column feature planned for Phase 2

**Implementation:**
```python
# User selects one column from dropdown
selected_column = st.selectbox("Choose column to analyze", numeric_columns)
analysis_data = df[selected_column]
```

---

### 5.2 Z-Score as Primary Algorithm
**Decision:** Use Z-score-based anomaly detection

**Rationale:**
- Fast: O(n) complexity
- Simple: Easy to understand and explain
- No training required: Works on any dataset immediately
- Statistical: Mathematically sound, well-proven
- Interpretable: Results make intuitive sense

**Limitations:**
- Assumes roughly normal distribution
- Sensitive to outliers in std dev calculation
- Not ideal for multivariate data

**Future Enhancement:** Add Isolation Forest for Phase 2

---

### 5.3 Threshold as Sensitivity Control
**Decision:** Let users adjust Z-score threshold (1.5 to 4.0)

**Rationale:**
- Different use cases need different sensitivity
- Domain experts know their data best
- Simple slider UI is intuitive
- Can rapidly test different thresholds

**Default: 3.0σ** (statistically conservative, ~0.3% false positive rate)

---

### 5.4 Rule-Based Explanations
**Decision:** Generate explanations using if-then rules, not ML

**Rationale:**
- Instant results (no ML training)
- Completely interpretable
- Users trust simple rules
- Sufficient for MVP

**Example Rule:**
```
IF zscore > 4.5: severity = "SEVERE"
IF value > mean: direction = "SPIKE"
Explanation = f"{severity} {direction}: {percent_change}% from normal"
```

---

### 5.5 Local Processing Only
**Decision:** No cloud, no external APIs, no database

**Rationale:**
- Zero infrastructure cost
- Data privacy (users own their data)
- Works offline (important for some users)
- Simpler architecture
- Faster iteration

**Trade-off:** Can't persist results across sessions (acceptable for MVP)

---

### 5.6 CSV as Input Format
**Decision:** Accept only CSV files (at least for MVP)

**Rationale:**
- Most common data format
- Simple to parse with Pandas
- Works with Excel (export to CSV)
- No database connector needed

**Future:** Support JSON, Parquet, SQL in Phase 2

---

## 6. ARCHITECTURAL PATTERNS USED

### 6.1 Separation of Concerns
Each layer has one job:
- **UI Layer:** Display and user interaction
- **Data Layer:** File I/O and validation
- **Algorithm Layer:** Anomaly detection logic
- **Explanation Layer:** Rule-based descriptions
- **Viz Layer:** Charts and visualizations

**Benefit:** Easy to test, modify, and extend each part independently

---

### 6.2 Functional Programming
- Functions are pure (same input → same output)
- No global state
- Functions have single responsibility
- Easy to unit test

**Example:**
```python
def detect_anomalies(data, threshold):
    # Pure function: no side effects
    # Same data + threshold → same output every time
    pass
```

---

### 6.3 Configuration over Code
- Threshold adjustable via UI (not hardcoded)
- Column selection via dropdown (not coded)
- Error messages in config (not hardcoded strings)

---

### 6.4 Error Handling Strategy
- **Fail Fast:** Validate input immediately
- **Clear Messages:** Tell users exactly what went wrong
- **Graceful Degradation:** App doesn't crash on edge cases
- **Recovery Path:** Give users way to fix (re-upload, etc.)

---

## 7. SCALABILITY & PERFORMANCE

### 7.1 Performance Targets
- **Small datasets (< 1MB):** Analyze in < 1 second
- **Medium datasets (1-10MB):** Analyze in 1-3 seconds
- **Large datasets (> 10MB):** Not supported (reject with error)

### 7.2 Optimization Strategies
- Use NumPy for vectorized operations (not loops)
- Cache calculations (mean, std) to avoid recalculation
- Matplotlib figures cached when possible
- Streamlit caching with @st.cache_data

### 7.3 Memory Efficiency
- Stream data loading (don't load entire file if possible)
- Delete temporary variables after use
- Numpy uses efficient memory layout (C-contiguous)

### 7.4 Scalability Limitations
- **Current:** Single column, local processing
- **Future:** Distributed processing, API backend

---

## 8. SECURITY CONSIDERATIONS

### 8.1 Data Privacy
✓ All files processed locally (no upload to cloud)
✓ No persistent storage (data deleted after session)
✓ No external API calls
✓ No user authentication (simple app)

### 8.2 Input Validation
✓ File size limits (< 10MB)
✓ File type validation (CSV only)
✓ Encoding validation (UTF-8, Latin-1)
✓ Data type validation (numeric columns)

### 8.3 Error Prevention
✓ Division by zero handling (std = 0)
✓ NaN/Inf value handling
✓ Bounds checking on user inputs

---

## 9. DEPLOYMENT ARCHITECTURE

### 9.1 How It Runs
```
User's Computer
├── Python 3.8+
├── Dependencies (Pandas, Numpy, Streamlit, etc.)
├── Application Code (app.py)
└── Input: CSV files (user's disk)

Command to run:
$ streamlit run app.py

Access: http://localhost:8501 (opens in browser)
```

### 9.2 Dependencies Installation
```bash
pip install -r requirements.txt

# Contents of requirements.txt:
streamlit>=1.20.0
pandas>=1.3.0
numpy>=1.20.0
matplotlib>=3.5.0
scipy>=1.7.0
```

### 9.3 File Structure
```
anomaly-detector/
├── app.py                 # Main Streamlit application
├── src/
│   ├── data_processor.py  # CSV loading, validation, cleaning
│   ├── anomaly_detector.py # Z-score algorithm
│   ├── explainer.py       # Rule-based explanations
│   └── visualizer.py      # Matplotlib charts
├── tests/
│   ├── test_detector.py
│   ├── test_processor.py
│   └── test_explainer.py
├── data/
│   └── sample_data.csv    # Sample dataset for testing
├── requirements.txt       # Python dependencies
├── README.md             # User documentation
└── ARCHITECTURE.md       # This file
```

---

## 10. LIMITATIONS & FUTURE IMPROVEMENTS

### 10.1 Current Limitations
1. **Single Column:** Can't detect correlations between columns
2. **Z-Score Only:** Assumes normal distribution
3. **No Training Data:** Uses simple statistics, not learned models
4. **No Time Context:** Treats data as simple sequence, ignores temporal patterns
5. **No Multivariate Analysis:** Can't detect complex patterns

### 10.2 Why These Limitations Exist
- **MVP Constraint:** 6-hour build time
- **Simplicity Goal:** Easy to understand and modify
- **Scope Control:** Focus on core functionality first

### 10.3 Future Enhancements
- **Phase 2:** Isolation Forest, DBSCAN algorithms
- **Phase 3:** Multi-column correlation analysis
- **Phase 4:** Real-time streaming data support
- **Phase 5:** Advanced visualization dashboard
- **Phase 6:** Cloud deployment, API layer

---

## 11. TESTING & QUALITY ASSURANCE

### 11.1 Unit Testing Strategy
- Test each function independently
- Mock file I/O (don't require actual files)
- Test edge cases (empty data, single value, etc.)
- Aim for > 80% code coverage

### 11.2 Integration Testing
- Test complete flow: Upload → Analyze → Display
- Verify visualization output
- Check export functionality

### 11.3 Acceptance Testing
- Test with real-world datasets
- Validate accuracy against ground truth
- Measure performance (response time)
- Check error messages for clarity

---

## APPENDIX: REFERENCE ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION ENTRY POINT                  │
│                        (app.py)                              │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
    ┌────────┐  ┌─────────┐  ┌──────────┐
    │ INPUT  │  │ PROCESS │  │ OUTPUT   │
    ├────────┤  ├─────────┤  ├──────────┤
    │ Upload │  │ Detect  │  │ Display  │
    │ CSV    │→ │Anomalies│→ │Results   │
    │        │  │ Explain │  │ Export   │
    └────────┘  └─────────┘  └──────────┘
        │            │            │
    [CSV data] [Statistics] [Visualizations]
```

---

**Document Version:** 1.0  
**Last Updated:** April 2026  
**Next Review:** Post-implementation

