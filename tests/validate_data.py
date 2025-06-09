import pandas as pd

def test_basic_requirements():
    """Test that basic requirements are met"""
    print("Running Basic Requirement Tests...")
    
    # Test 1: Check if result.csv exists and has correct columns
    try:
        results = pd.read_csv('result.csv')
        expected_columns = ['patient_id', 'enrollment_start_date', 'enrollment_end_date', 
                          'ct_outpatient_visits', 'ct_days_with_outpatient_visit']
        
        assert all(col in results.columns for col in expected_columns), "Missing required columns"
        print("✓ All required columns present")
        
        # Test 2: Check answers match expected values
        assert len(results) == 3105, f"Expected 3105 rows, got {len(results)}"
        print("✓ Answer 1 correct: 3105 rows")
        
        distinct_days = results['ct_days_with_outpatient_visit'].nunique()
        assert distinct_days == 33, f"Expected 33 distinct values, got {distinct_days}"
        print("✓ Answer 2 correct: 33 distinct values")
        
        # Test 3: Data quality checks
        assert results['ct_outpatient_visits'].min() >= 0, "Negative visit counts found"
        assert results['ct_days_with_outpatient_visit'].min() >= 0, "Negative day counts found"
        print("✓ No negative values")
        
        # Test 4: Logic check - days with visits should not exceed total visits
        invalid = (results['ct_days_with_outpatient_visit'] > results['ct_outpatient_visits']).sum()
        assert invalid == 0, f"Found {invalid} records where days > visits"
        print("✓ Days with visits ≤ total visits")
        
        print("\n🎉 All tests passed!")
        return True
        
    except FileNotFoundError:
        print("❌ result.csv not found - run waymark_assessment.py first")
        return False
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_basic_requirements()