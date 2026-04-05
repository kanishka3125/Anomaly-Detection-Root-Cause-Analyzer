# LIMITATIONS & FUTURE SCOPE DOCUMENT
## AI Data Anomaly Detection & Root Cause Analyzer

**Version:** 1.0  
**Status:** Final  
**Created:** April 2026  

---

## 1. CURRENT LIMITATIONS (MVP)

### 1.1 Algorithm Limitations

#### Limitation 1.1.1: Single Algorithm (Z-Score Only)
**Current State:**
- Only Z-score based detection available
- Assumes roughly normal distribution
- Effective for univariate analysis only

**Why It Exists:**
- 6-hour build time constraint
- Z-score is simple, fast, and interpretable
- Sufficient for MVP scope

**Impact:**
- Can't detect anomalies in heavy-tailed distributions
- May miss subtle pattern changes
- Limited to statistical outlier detection

**Workaround for Users:**
- Users can adjust sensitivity threshold
- Can preprocess data to make it more normal (log transform, etc.)
- Multiple passes with different thresholds possible

**Example Where It Fails:**
```
Dataset: Stock returns (heavy-tailed distribution)
- Normal returns: -5% to +5%
- Rare events: -50% to +50%

Z-score threshold (3σ):
- Flags large moves (50%) as anomalies ✓
- But naturally high variance inflates σ
- May miss more subtle 15% moves ✗
```

---

#### Limitation 1.1.2: No Seasonal Decomposition
**Current State:**
- Treats data as simple sequence
- Doesn't account for repeating patterns (daily, weekly, yearly)
- Can't distinguish anomalies from seasonal variation

**Why It Exists:**
- Seasonal decomposition requires more complex algorithms
- Needs more data (at least 2 full cycles)
- Time-series analysis beyond MVP scope

**Impact:**
- **False Positives** in seasonal data
  - Every Monday spike flagged as anomaly (if weekly pattern)
  - Holiday sales treated as unusual
- **False Negatives** if noise hides true anomalies
  
**Real-World Example:**
```
Retail Sales Data (daily):
Monday-Friday:   Average $10,000
Saturday-Sunday: Average $3,000
Monday again:    Expected $10,000

Z-Score sees:
- Saturday dip: "This is unusual!" ✓ Flag as anomaly
- But it's just the weekend pattern ✗ False positive
```

**Planned Fix:** Phase 2 (Seasonal Decomposition)

---

#### Limitation 1.1.3: No Multivariate Analysis
**Current State:**
- Analyzes one column at a time
- Can't detect correlated anomalies
- Misses complex patterns involving multiple variables

**Why It Exists:**
- Single column simplifies MVP
- Multivariate detection is more complex
- UI would be more complicated

**Impact:**
- Can't detect when multiple metrics change together
- Missing context about dependencies
- May miss root causes involving multiple factors

**Example:**
```
Server Performance Data:
- CPU: Normal (50%)
- Memory: Normal (60%)
- Response Time: High (5sec)

Univariate Analysis:
- CPU: Normal ✓
- Memory: Normal ✓
- Response Time: Anomaly ✗

Multivariate Analysis (Future):
- Would detect: "Unusual combo - high response time 
  despite normal CPU/memory suggests I/O bottleneck"
```

---

### 1.2 Data Limitations

#### Limitation 1.2.1: CSV Files Only
**Current State:**
- Accepts only .csv files
- No support for JSON, Excel, Parquet, or databases
- Can't connect to live data sources

**Impact:**
- Users must convert their data format to CSV
- No real-time streaming support
- No database integration
- Manual file handling required

**Workaround:**
- Export Excel to CSV (1 minute)
- Convert JSON to CSV via Python/R
- Database export to CSV

---

#### Limitation 1.2.2: File Size & Row Count Limits
**Current State:**
- Max 10 MB file size
- Recommended max 100,000 rows
- Older systems may struggle with 10MB

**Why It Exists:**
- Local processing (no cloud scaling)
- Streamlit browser memory limits
- 6-hour build time (no optimization)

**Impact:**
- Can't analyze very large datasets
- Must sample large datasets beforehand
- Performance degrades with huge files

**Solution (Future):**
- Implement pagination/chunking
- Move to cloud backend (Phase 5)
- Use more efficient data formats (Parquet)

---

#### Limitation 1.2.3: Numeric Data Only
**Current State:**
- Only analyzes numeric columns
- Ignores text, categorical, date columns
- Can't detect anomalies in text data

**Impact:**
- Can't analyze product names, categories, user IDs
- Timestamps treated as headers, not data
- Limited to numerical measurements

**Why It Exists:**
- Z-score requires numeric values
- Text analysis needs different algorithms (NLP)
- Out of scope for statistical anomaly detection

---

### 1.3 Feature Limitations

#### Limitation 1.3.1: No Custom Thresholds per Anomaly Type
**Current State:**
- Single global threshold for all anomalies
- Can't define different sensitivity for spikes vs dips
- Can't set business-specific thresholds

**Example:**
```
E-commerce Sales:
- Dip (sales drop): Want to catch at 2.0σ (very sensitive)
- Spike (high sales): Can tolerate 4.0σ (less sensitive)

Currently: Must choose one threshold for both
```

**Planned Fix:** Phase 3 (Advanced settings)

---

#### Limitation 1.3.2: No Context or Root Cause Analysis
**Current State:**
- Shows THAT something is anomalous
- Explains severity and direction
- Doesn't explain WHY (actual root cause)

**Example Explanation (Current):**
```
"SEVERE SPIKE: Value jumped 62% above normal.
Expected: 5250 ± 850. Actual: 8500."
```

**What's Missing:**
- Was there a promotion that day?
- Did competitors have issues?
- Was there a seasonal event?
- What external factors could explain this?

**Why It Exists:**
- Requires domain knowledge or external data
- Root cause analysis is complex and domain-specific
- Would need integration with other systems

**Planned Fix:** Phase 5 (Advanced explanations with external data)

---

#### Limitation 1.3.3: No Persistence or History
**Current State:**
- Results exist only during active session
- No saved reports
- No comparison with historical analyses
- No trend tracking

**Impact:**
- User must re-upload to re-analyze
- Can't track changes over time
- No audit trail
- No historical comparison

**Why It Exists:**
- Local processing (no database)
- Session-based architecture
- 6-hour MVP scope

**Planned Fix:** Phase 5 (Cloud backend with persistence)

---

#### Limitation 1.3.4: No Real-Time Alerts
**Current State:**
- Batch processing only
- User must manually upload and analyze
- No automated alerting system
- No continuous monitoring

**Impact:**
- Anomalies detected hours/days after occurrence
- No automated responses
- Manual workflow required
- Not suitable for critical systems

**Example Use Case That Fails:**
```
Bank Fraud Detection:
- Need: Alert within seconds of suspicious transaction
- Current: Analyst uploads daily batch, analyzes next day
- Gap: 24-hour delay ✗
```

**Planned Fix:** Phase 4 (Real-time streaming + alerting)

---

### 1.4 UI/UX Limitations

#### Limitation 1.4.1: Desktop-First Only
**Current State:**
- Designed for desktop browsers
- Mobile layout not optimized
- Touch interactions untested

**Impact:**
- Small screens cramped
- Difficult to use on phones/tablets
- Tables may not be scrollable on mobile
- Charts may be too small

**Planned Fix:** Phase 3 (Responsive design)

---

#### Limitation 1.4.2: No Dark Mode
**Current State:**
- Light mode only
- No automatic color scheme adaptation
- High brightness for nighttime use

**Impact:**
- Eye strain in low-light environments
- No accessibility for users with light sensitivity
- Not aligned with modern UI standards

**Note:** Streamlit has built-in dark mode support
**Planned Fix:** Phase 2 (Easy config update)

---

#### Limitation 1.4.3: Basic Visualizations
**Current State:**
- Static Matplotlib charts
- No interactive exploration
- No zoom/pan/hover details
- Limited customization

**Comparison:**
```
Current (Matplotlib):
├─ Time-series line chart ✓
├─ Histogram ✓
└─ Box plot ✓
  └─ Static, no interaction

Future (Plotly/Altair):
├─ Time-series line chart ✓
├─ Histogram ✓
├─ Box plot ✓
└─ Interactive (zoom, pan, hover) ✓
```

---

### 1.5 Deployment & Infrastructure

#### Limitation 1.5.1: Local Processing Only
**Current State:**
- Must run on user's machine
- Requires Python installation
- No cloud deployment
- No multi-user support

**Impact:**
- Setup barrier (Python install)
- Can't share results via URL
- No access control
- Not suitable for enterprise use

**Workaround:**
- Docker container (user still manages)
- Jupyter notebook (for data scientists)

**Planned Fix:** Phase 5 (Cloud deployment on AWS/GCP/Azure)

---

#### Limitation 1.5.2: No Database Integration
**Current State:**
- File-based input/output only
- No connection to SQL databases
- No API integration
- Results not stored

**Impact:**
- Can't pull data directly from production databases
- Can't automate workflows
- Manual data export required
- No audit trail

**Planned Fix:** Phase 4 (Database connectors + API layer)

---

#### Limitation 1.5.3: Single-User, Single-Session
**Current State:**
- One user per instance
- Session data lost after close
- No multi-user access control
- No collaboration features

**Planned Fix:** Phase 5 (Enterprise features)

---

## 2. KNOWN ISSUES & WORKAROUNDS

### 2.1 Issue: High Standard Deviation Masks Anomalies

**Scenario:**
```
Data: [10, 11, 9, 10, 11, 200]  (one huge outlier)

Calculated std dev: ~72 (inflated by outlier!)
Z-score of 200: (200-37)/72 = 2.26 (below 3.0 threshold!)
Result: Not flagged as anomaly ✗
```

**Workaround:**
1. Manually inspect data first
2. Remove extreme outliers before analysis
3. Use lower sensitivity threshold (2.0σ instead of 3.0σ)
4. Use robust statistics (planned for Phase 2)

---

### 2.2 Issue: False Positives in Seasonal Data

**Scenario:**
```
Monthly website traffic:
- Jan: 100k (winter spike)
- Feb: 100k (winter spike)
- Jun: 30k (summer dip) ← Flagged as anomaly!
- Jul: 30k (summer dip) ← Flagged as anomaly!

Global mean: 63k
Global std: 35k
Z-score of 30k: (30-63)/35 = 0.94

Actually not flagged, but could be on edge.
```

**Workaround:**
1. Pre-filter to specific season
2. Adjust threshold higher for seasonal data
3. Use deseasonalized data (planned Phase 2)

---

### 2.3 Issue: Small Datasets (< 30 rows)

**Problem:**
- Statistical methods need larger samples
- Z-score assumes large n
- Small samples → inaccurate σ estimation

**Workaround:**
- Aggregate data to fewer, larger values
- Gather more data
- Use different method (planned Phase 2)

---

## 3. FUTURE ROADMAP

### Phase 2: Algorithm Expansion (Q2 2026)

**Objective:** Add more detection methods

#### 2.1 Seasonal Decomposition
- Remove seasonal patterns before detection
- Detect trend anomalies separately
- Handle monthly/weekly/daily patterns

**Technologies:** statsmodels.tsa.seasonal.seasonal_decompose

#### 2.2 Isolation Forest Algorithm
- Tree-based anomaly detection
- Less sensitive to outliers than Z-score
- Works better with multivariate data
- No normality assumptions

**Technologies:** scikit-learn.ensemble.IsolationForest

#### 2.3 Robust Statistics (MAD)
- Median Absolute Deviation instead of std dev
- More resistant to outliers
- Better for heavy-tailed distributions

**Technologies:** scipy.stats.median_abs_deviation

#### 2.4 DBSCAN Clustering
- Density-based anomaly detection
- Groups similar data, flags isolated points
- Parameter tuning required (eps, min_samples)

**Technologies:** scikit-learn.cluster.DBSCAN

---

### Phase 3: Multi-Feature & Advanced UI (Q3 2026)

**Objective:** Support multiple columns and better UX

#### 3.1 Multi-Column Detection
```
Currently: Analyze single column
Future: "Detect anomalies when ANY column is unusual"
        "Find rows where MULTIPLE columns are anomalous"
```

#### 3.2 Correlation Analysis
- Show which columns move together
- Detect correlated anomalies
- Suggest potential root causes

#### 3.3 Mobile Responsive Design
- Optimize for tablets and phones
- Touch-friendly controls
- Responsive tables and charts

#### 3.4 Advanced Visualization
- Interactive Plotly charts
- Zoom, pan, hover details
- Custom color schemes
- Dark mode

---

### Phase 4: Real-Time & Enterprise (Q4 2026)

**Objective:** Support streaming and enterprise use cases

#### 4.1 Real-Time Data Streaming
- Accept data from APIs/webhooks
- Process data as it arrives
- Continuous monitoring
- Alert system for anomalies

**Technologies:** Apache Kafka, AWS Kinesis, WebSockets

#### 4.2 Database Integration
- Connect to PostgreSQL, MySQL, MongoDB
- Scheduled analysis jobs
- Automated data pulls
- Results stored in DB

#### 4.3 API Layer
```
POST /api/analyze
{
  "data": [[1, 2], [3, 4], ...],
  "threshold": 3.0,
  "method": "zscore"
}

Response:
{
  "anomalies": [indices],
  "severity": [levels],
  "explanations": [texts]
}
```

#### 4.4 Alert System
- Email alerts for new anomalies
- Slack integration
- Webhook notifications
- Custom alert rules

---

### Phase 5: Cloud Deployment & Enterprise (Q1 2027)

**Objective:** Production-grade, scalable platform

#### 5.1 Cloud Deployment
- AWS Lambda / Google Cloud Run
- Auto-scaling
- Load balancing
- Multi-region support

**Technologies:** AWS CloudFormation, Docker, Kubernetes

#### 5.2 Advanced Authentication
- User login system
- Role-based access control (RBAC)
- API key management
- SSO integration

#### 5.3 Data Persistence
- Long-term results storage
- Historical comparison
- Trend analysis
- Report generation

**Database:** PostgreSQL, MongoDB, or data warehouse

#### 5.4 Advanced Explanations
- NLP-powered explanations
- External data integration
- Causal analysis
- Anomaly classification (spike/drop/trend/noise)

#### 5.5 Dashboard & Collaboration
- Web dashboard with saved reports
- Share results with team
- Comments and annotations
- Audit trail

#### 5.6 Performance Optimization
- Distributed processing
- GPU acceleration
- In-memory caching
- Query optimization

---

## 4. TECHNICAL DEBT

### 4.1 Code Organization
- [ ] Move hardcoded constants to config file
- [ ] Add logging throughout
- [ ] Implement error recovery
- [ ] Add docstrings to all functions

### 4.2 Testing
- [ ] Increase code coverage to 95%
- [ ] Add integration tests
- [ ] Add performance benchmarks
- [ ] Add regression tests

### 4.3 Documentation
- [ ] API documentation (Swagger/OpenAPI)
- [ ] User guide with examples
- [ ] Architecture diagrams
- [ ] Deployment guide

### 4.4 Performance
- [ ] Optimize Matplotlib rendering
- [ ] Cache computation results
- [ ] Implement lazy loading
- [ ] Profile and optimize bottlenecks

---

## 5. SCALABILITY STRATEGY

### 5.1 Current (Local Processing)
```
User → CSV Upload → Local Processing → Results Display
Max: 100K rows, 10MB, single session
```

### 5.2 Phase 2-3 (Optimized Local)
```
User → CSV Upload → Optimized Processing → Better Results
Max: 1M rows, 100MB, still local
Improvements: Vectorization, caching, streaming UI updates
```

### 5.3 Phase 4 (Cloud-Ready)
```
User → Web Interface → Cloud API → Distributed Processing → Storage
Max: Unlimited rows (distributed)
Improvements: Real-time, persistent, multi-user
```

### 5.4 Phase 5 (Enterprise)
```
Enterprise System → Scheduled Jobs → Distributed Pipeline → Data Warehouse
Multiple sources → Complex analysis → Actionable insights
```

---

## 6. COMPETITIVE ANALYSIS

### What We Do Better (MVP)
✓ Simple, easy to use (no ML expertise required)
✓ Fast (no training time)
✓ Free and open source
✓ Can run locally (privacy)
✓ Good for learning

### What We Do Worse (Limitations)
✗ Less sophisticated algorithms
✗ No real-time capabilities
✗ No enterprise features
✗ Limited visualization options
✗ Single-user only

### Competitors & Our Response

**Outlier:** Splunk (Log analysis)
- Splunk: Enterprise log anomaly detection
- Us: Lightweight CSV analysis (complementary, not competitive)
- Opportunity: Phase 4-5 could target similar market

**Trend Follower:** RobustIntelligence
- RobustIntelligence: ML monitoring + anomaly detection
- Us: Simpler, broader use cases
- Opportunity: Could integrate with ML workflows

**Academic:** NumPyro, PyMC
- NumPyro/PyMC: Bayesian statistical modeling
- Us: Practical anomaly detection
- Opportunity: Different audiences (industry vs research)

---

## 7. ASSUMPTIONS & DEPENDENCIES

### 7.1 MVP Assumptions
- Data is roughly normally distributed ✓
- CSV is the standard input format ✓
- Users have Python/Streamlit knowledge (Phase 1)
- Single-user, single-session is acceptable ✓
- 6-hour build time is sufficient ✓

### 7.2 Phase 2-3 Assumptions
- Seasonal data is common (need seasonal decomposition)
- Multi-column analysis is valuable
- Mobile users are target audience
- Plotly/Altair is suitable for visualization

### 7.3 Phase 4-5 Assumptions
- Real-time is necessary for production
- Cloud deployment is required
- Enterprise features (auth, persistence) are needed
- Horizontal scaling needed for large orgs

---

## 8. RISK ASSESSMENT

### High-Risk Items
1. **Z-Score's normality assumption**
   - Risk: Fails on heavy-tailed data
   - Mitigation: Add alternative algorithms (Phase 2)
   - Likelihood: Medium

2. **No real-time support**
   - Risk: Can't compete in alerting market
   - Mitigation: Add streaming (Phase 4)
   - Likelihood: Low (acceptable for MVP)

3. **Local processing only**
   - Risk: Can't scale to enterprise
   - Mitigation: Cloud deployment (Phase 5)
   - Likelihood: Low (acceptable for MVP)

### Medium-Risk Items
1. **CSV-only input**
   - Risk: Users can't integrate with systems
   - Mitigation: Add database connectors (Phase 4)
   - Likelihood: Medium

2. **No seasonal handling**
   - Risk: False positives in seasonal data
   - Mitigation: Seasonal decomposition (Phase 2)
   - Likelihood: Medium

---

## 9. SUCCESS METRICS FOR FUTURE PHASES

### Phase 2 Metrics
- [ ] Support 5+ anomaly detection algorithms
- [ ] Seasonal data false-positive rate < 5%
- [ ] User satisfaction with algorithm options
- [ ] Code coverage > 90%

### Phase 3 Metrics
- [ ] Multi-column detection available
- [ ] Mobile usability score > 80%
- [ ] Interactive chart engagement > 70%
- [ ] Time to analyze: < 1 second

### Phase 4 Metrics
- [ ] Real-time detection latency < 100ms
- [ ] 99.9% uptime SLA
- [ ] Enterprise customer: 3+
- [ ] API adoption rate

### Phase 5 Metrics
- [ ] 1000+ active users
- [ ] Enterprise penetration: 20+ companies
- [ ] Revenue: $100k+ ARR
- [ ] Net Promoter Score (NPS) > 50

---

## 10. CONCLUSION

### Current State (MVP - April 2026)
The AI Data Anomaly Detection system is a **solid, focused MVP** that:
- ✓ Solves the core problem (detect anomalies in time-series data)
- ✓ Is simple and easy to use
- ✓ Uses proven statistical methods
- ✓ Provides useful explanations
- ✓ Has no external dependencies

### Major Limitations (Awareness)
The system is not suitable for:
- ✗ Real-time production monitoring
- ✗ Enterprise multi-user scenarios
- ✗ Complex multivariate analysis
- ✗ Seasonal data (without preprocessing)
- ✗ Heavy-tailed distributions
- ✗ High-volume data (> 10MB)

### Value Proposition
**Best for:**
- Learning anomaly detection concepts
- Quick ad-hoc analysis
- One-time data investigations
- Educational projects
- Small-team exploratory work

**Not for:**
- Production monitoring systems
- Real-time alerting
- Enterprise deployment
- Complex analytics

### Path Forward
**Each phase adds value in specific areas:**
- Phase 2: Better algorithms
- Phase 3: Better UX
- Phase 4: Real-time capabilities
- Phase 5: Enterprise scale

**The MVP is complete and ready.** Future phases should be driven by user feedback and use-case validation.

---

## APPENDIX: FEATURE PRIORITY MATRIX

```
              HIGH VALUE
                  ↑
                  │
    Phase 5       │      Phase 4
    Cloud         │    Real-time
    Enterprise    │    Streaming
                  │
                  │
    Phase 3       │      Phase 2
    Mobile UX     │    Algorithms
    Dark Mode     │    Seasonal
                  │
                  └──────────────→
              EASY TO BUILD
```

**Quick Wins (Phase 2):**
- Dark mode (1 line of code)
- Additional algorithms (100 lines each)

**Medium Effort (Phase 3):**
- Mobile optimization (200 lines CSS)
- Multi-column support (300 lines logic)

**High Effort (Phase 4):**
- Real-time streaming (1000+ lines)
- Database integration (1500+ lines)

**Very High Effort (Phase 5):**
- Cloud deployment (2000+ lines infra)
- Enterprise features (3000+ lines)

---

**Document Version:** 1.0  
**Last Updated:** April 2026  
**Next Phase Start:** Q2 2026 (Estimated)

