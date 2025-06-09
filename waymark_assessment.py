import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def step1_transform_enrollment_data():
    """
    Step 1: Transform patient_id x month_year to patient_id x enrollment_start_date x enrollment_end_date
    """
    print("Step 1: Data Transformation")
    print("=" * 40)
    
    # Load the patient enrollment data from local CSV
    df_enrollment = pd.read_csv('data/patient_id_month_year.csv')
    
    print(f"Original data shape: {df_enrollment.shape}")
    print("Sample of original data:")
    print(df_enrollment.head())
    
    # Convert month_year to datetime (first day of each month)
    df_enrollment['month_year'] = pd.to_datetime(df_enrollment['month_year'])
    
    # Sort by patient_id and month_year to identify continuous periods
    df_enrollment = df_enrollment.sort_values(['patient_id', 'month_year']).reset_index(drop=True)
    
    # Group by patient_id and identify continuous enrollment periods
    enrollment_periods = []
    
    for patient_id in df_enrollment['patient_id'].unique():
        patient_data = df_enrollment[df_enrollment['patient_id'] == patient_id]['month_year'].sort_values()
        
        if len(patient_data) == 0:
            continue
            
        # Initialize first period
        start_date = patient_data.iloc[0]
        current_date = start_date
        
        for i in range(1, len(patient_data)):
            next_date = patient_data.iloc[i]
            
            # Check if next month is consecutive (difference should be ~30-31 days)
            # We'll check if the difference is approximately 1 month
            expected_next = current_date + pd.DateOffset(months=1)
            
            if next_date <= expected_next + timedelta(days=2):  # Allow small tolerance
                # Continuous enrollment, update current_date
                current_date = next_date
            else:
                # Gap in enrollment, close current period and start new one
                end_date = current_date + pd.DateOffset(months=1) - timedelta(days=1)  # Last day of month
                enrollment_periods.append({
                    'patient_id': patient_id,
                    'enrollment_start_date': start_date.strftime('%Y-%m-%d'),
                    'enrollment_end_date': end_date.strftime('%Y-%m-%d')
                })
                
                # Start new period
                start_date = next_date
                current_date = next_date
        
        # Close the last period
        end_date = current_date + pd.DateOffset(months=1) - timedelta(days=1)  # Last day of month
        enrollment_periods.append({
            'patient_id': patient_id,
            'enrollment_start_date': start_date.strftime('%Y-%m-%d'),
            'enrollment_end_date': end_date.strftime('%Y-%m-%d')
        })
    
    # Create DataFrame with enrollment periods
    df_enrollment_span = pd.DataFrame(enrollment_periods)
    
    # Save to CSV
    df_enrollment_span.to_csv('patient_enrollment_span.csv', index=False)
    
    print(f"\nTransformed data shape: {df_enrollment_span.shape}")
    print("Sample of transformed data:")
    print(df_enrollment_span.head(10))
    
    answer1 = len(df_enrollment_span)
    print(f"\nAnswer 1: Number of rows in patient_enrollment_span.csv = {answer1}")
    
    return df_enrollment_span, answer1

def step2_aggregate_outpatient_data(df_enrollment_span):
    """
    Step 2: Aggregate outpatient visit data with enrollment periods
    """
    print("\n\nStep 2: Data Aggregation")
    print("=" * 40)
    
    # Load the outpatient visits data from local CSV
    df_visits = pd.read_csv('data/outpatient_visits_file.csv')
    
    print(f"Outpatient visits data shape: {df_visits.shape}")
    print("Sample of outpatient visits data:")
    print(df_visits.head())
    
    # Convert date to datetime
    df_visits['date'] = pd.to_datetime(df_visits['date'])
    
    # Convert enrollment dates to datetime for comparison
    df_enrollment_span['enrollment_start_date'] = pd.to_datetime(df_enrollment_span['enrollment_start_date'])
    df_enrollment_span['enrollment_end_date'] = pd.to_datetime(df_enrollment_span['enrollment_end_date'])
    
    # Initialize result list
    result_data = []
    
    # For each enrollment period, calculate visit metrics
    for _, enrollment_row in df_enrollment_span.iterrows():
        patient_id = enrollment_row['patient_id']
        start_date = enrollment_row['enrollment_start_date']
        end_date = enrollment_row['enrollment_end_date']
        
        # Filter visits for this patient within the enrollment period
        patient_visits = df_visits[
            (df_visits['patient_id'] == patient_id) & 
            (df_visits['date'] >= start_date) & 
            (df_visits['date'] <= end_date)
        ]
        
        # Calculate metrics
        ct_outpatient_visits = patient_visits['outpatient_visit_count'].sum()
        ct_days_with_outpatient_visit = len(patient_visits['date'].unique()) if len(patient_visits) > 0 else 0
        
        result_data.append({
            'patient_id': patient_id,
            'enrollment_start_date': start_date.strftime('%Y-%m-%d'),
            'enrollment_end_date': end_date.strftime('%Y-%m-%d'),
            'ct_outpatient_visits': int(ct_outpatient_visits),
            'ct_days_with_outpatient_visit': int(ct_days_with_outpatient_visit)
        })
    
    # Create final result DataFrame
    df_result = pd.DataFrame(result_data)
    
    # Save to CSV
    df_result.to_csv('result.csv', index=False)
    
    print(f"\nFinal result data shape: {df_result.shape}")
    print("Sample of final result:")
    print(df_result.head(10))
    
    # Calculate answer 2
    unique_days_count = df_result['ct_days_with_outpatient_visit'].nunique()
    print(f"\nUnique values in ct_days_with_outpatient_visit:")
    print(sorted(df_result['ct_days_with_outpatient_visit'].unique()))
    
    answer2 = unique_days_count
    print(f"\nAnswer 2: Number of distinct values of ct_days_with_outpatient_visit = {answer2}")
    
    return df_result, answer2

def main():
    """
    Main function to execute the complete assignment
    """
    print("Waymark Healthcare Analytics Assignment")
    print("=" * 50)
    
    # Check if data files exist
    if not os.path.exists('data/patient_id_month_year.csv'):
        print("Error: data/patient_id_month_year.csv not found!")
        print("Please make sure you have downloaded the CSV files and placed them in the 'data' folder.")
        return None, None
    
    if not os.path.exists('data/outpatient_visits_file.csv'):
        print("Error: data/outpatient_visits_file.csv not found!")
        print("Please make sure you have downloaded the CSV files and placed them in the 'data' folder.")
        return None, None
    
    try:
        # Step 1: Transform enrollment data
        df_enrollment_span, answer1 = step1_transform_enrollment_data()
        
        # Step 2: Aggregate outpatient data
        df_result, answer2 = step2_aggregate_outpatient_data(df_enrollment_span)
        
        # Summary
        print("\n\nSUMMARY")
        print("=" * 20)
        print(f"Answer 1: {answer1}")
        print(f"Answer 2: {answer2}")
        
        print("\nFiles created:")
        print("- patient_enrollment_span.csv")
        print("- result.csv")
        
        return answer1, answer2
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    answer1, answer2 = main()