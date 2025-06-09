# Waymark Healthcare Analytics Assignment

## Author
**Christian DiVincenzo**  
Healthcare Analytics Assignment for Waymark  
June 2025

## Overview
This repository contains my solution to the Waymark Healthcare Informatics and Business Intelligence Analyst take-home assessment. The assignment transforms patient enrollment data and aggregates outpatient visit metrics to create comprehensive healthcare analytics insights.

## Objective
Create a single CSV file containing patient enrollment periods with aggregated outpatient visit metrics:
- `patient_id` (Primary Key)
- `enrollment_start_date` (Primary Key) 
- `enrollment_end_date` (Primary Key)
- `ct_outpatient_visits`
- `ct_days_with_outpatient_visit`

## Project Structure
```
waymark-assignment/
├── data/
│   ├── patient_id_month_year.csv
│   └── outpatient_visits_file.csv
├── waymark_assessment.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Data Sources
The analysis uses two healthcare datasets:
1. **Patient Enrollment Data** (`data/patient_id_month_year.csv`): Monthly enrollment records by patient
2. **Outpatient Visits Data** (`data/outpatient_visits_file.csv`): Daily outpatient visit counts by patient

## Dependencies
```bash
pip install pandas numpy
```

## Usage
```bash
python waymark_assessment.py
```

## Solution Approach

### Step 1: Data Transformation
- Transforms patient enrollment from monthly records to continuous enrollment periods
- Identifies gaps in enrollment to create distinct enrollment spans
- Outputs `patient_enrollment_span.csv`

### Step 2: Data Aggregation
- Joins enrollment periods with outpatient visit data
- Calculates visit metrics within each enrollment period
- Outputs final `result.csv` with all required fields

## Results
- **Answer 1**: 3105 rows in patient_enrollment_span.csv
- **Answer 2**: 33 distinct values of ct_days_with_outpatient_visit

## Output Files
- `patient_enrollment_span.csv`: Transformed enrollment periods by patient
- `result.csv`: Final dataset with enrollment periods and aggregated visit metrics

## Technical Implementation
- Uses pandas for efficient data manipulation and datetime handling
- Implements continuous enrollment period detection through date gap analysis
- Applies vectorized operations for scalable data processing

## Testing
To validate the results:
```bash
python tests/validate_data.py

