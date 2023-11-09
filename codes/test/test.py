
import sys
sys.path.append('../functions_py')

from effect_size_process import calc_sum_effsize_raw
import os

def test_calc_sum_effsize_raw():
    # Prepare a dummy directory with dummy VCF files for the test
    test_mss = "test_data/"
    os.makedirs(test_mss + "originalvcfs/", exist_ok=True)
    dummy_vcf_content = """# Dummy VCF content
3\t500\t.\tA\tG\t.\t.\t.\n"""
    with open(test_mss + "originalvcfs/dummy.vcf", "w") as f:
        f.write(dummy_vcf_content)

    # Prepare a dummy dict_c_g
    dict_c_g = {'gene1': [400, 600, 0.5]}
    
    # Expected result is a list with one element: 0.5
    expected = 0.5

    # Run the function
    result = calc_sum_effsize_raw(test_mss, dict_c_g)

    # Clean up test data directory
    os.remove(test_mss + "originalvcfs/dummy.vcf")
    os.rmdir(test_mss + "originalvcfs/")
    os.rmdir(test_mss)

    # Assert that the result is as expected
    assert result == expected, f"Expected {expected}, got {result}"
