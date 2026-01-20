# Aadhaar Risk Analytics Engine

**A Unified Risk Detection Framework for Aadhaar Enrolment, Demographic, and Biometric Data**

---

##  Project Overview

The **Aadhaar Risk Analytics Engine** is a data-driven risk assessment framework designed to identify **anomalous, high-risk enrolment activities** within Aadhaar enrolment, demographic, and biometric datasets published by UIDAI.

By combining **statistical anomaly detection**, **temporal velocity analysis**, and **domain-informed risk scoring**, the system highlights potential irregularities such as:
- sudden enrolment spikes,
- abnormal demographic shifts,
- unusual biometric update patterns at the pincode level.

The project emphasizes **explainability, scalability, and policy relevance**, making it suitable for **public-sector analytics and fraud monitoring use cases**.

---

## Objectives

- Perform end-to-end **Exploratory Data Analysis (EDA)** on Aadhaar datasets
- Clean, normalize, and merge multi-source Aadhaar data
- Engineer interpretable **risk indicators** (velocity & deviation)
- Build a **transparent risk engine** without black-box ML dependency
- Generate **actionable risk scores** with clear reasoning
- Present insights via notebooks and a Streamlit-ready architecture

---

##  Datasets Used

All datasets are sourced from **UIDAI Aadhaar Enrolment & Update data**.

### 1. Aadhaar Enrolment Dataset
- Age-wise enrolment counts
- State, district, pincode granularity
- Time-series enrolment trends

### 2. Aadhaar Demographic Dataset
- Demographic update distributions
- Age group-wise updates
- Spatial and temporal variations

### 3. Aadhaar Biometric Dataset
- Biometric update activity
- Temporal spikes in biometric updates
- Regional behavioral patterns

> **Note:** Raw datasets are intentionally excluded from this repository due to size constraints and best practices.  
> The analysis code is fully reproducible.

---

##  Methodology

### 1. Data Cleaning & Standardization
- State name normalization
- Date parsing with mixed formats
- Removal of inconsistencies and duplicates
- Handling missing and outlier values

### 2. Feature Engineering
- **Total activity counts** (enrolment / demographic / biometric)
- **Velocity metrics** (day-over-day change per pincode)
- **Z-score deviation metrics** (statistical anomaly detection)

### 3. Risk Scoring Logic
Instead of black-box ML, the system uses:
- Logistic scaling (sigmoid transformation)
- Weighted risk aggregation
- Domain-driven thresholds

