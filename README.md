# AI Data Anomaly Detection & Root Cause Analyzer

## Overview

This project is a web-based application that detects anomalies in time-series data and provides simple, explainable insights. Users can upload a dataset, and the system identifies unusual patterns such as sudden spikes or drops.

The application uses statistical methods along with visualization to make anomaly detection easy to understand and analyze.

---

## Features

* Upload CSV data (Date, Value format)
* Visualize data using line graphs
* Detect anomalies using Z-score method
* Highlight anomalies on the graph
* Display anomaly table with explanations
* Show key statistics (mean, standard deviation, anomaly count)
* Generate basic insights based on data patterns
* Option to download processed results (if implemented)

---

## How It Works

1. The user uploads a CSV file containing time-series data
2. The system reads and processes the data using Pandas
3. Z-score is calculated to identify abnormal values
4. Data points beyond the threshold are marked as anomalies
5. Results are displayed through graphs, tables, and insights

---

## Tech Stack

* Python
* Streamlit
* Pandas
* NumPy
* Matplotlib

---

## Dataset Format

The input CSV file must follow this structure:

```
Date,Value
2024-03-01,1000
2024-03-02,980
```

* Date: Time-based column
* Value: Numeric column

---

## How to Run

1. Clone the repository:

```
git clone <your-repo-link>
cd <project-folder>
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the application:

```
streamlit run app.py
```

---

## Applications

* Business sales analysis
* Website traffic monitoring
* Basic fraud detection
* System performance monitoring

---

## Limitations

* Works with single-column numeric data
* Uses a simple statistical method (Z-score)
* Not suitable for highly complex datasets

---

## Future Scope

* Integration of advanced ML models such as Isolation Forest
* Multi-variable anomaly detection
* Real-time data processing
* Enhanced interactive dashboards

---

## Author

* Kanishka Sharma
* B.Tech CSE (AIML)

---

## Conclusion

This project demonstrates how statistical AI techniques can be used to detect anomalies and generate insights from data. It is designed to be simple, efficient, and suitable for real-world applications.

