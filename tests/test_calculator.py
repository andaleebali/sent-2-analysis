import sys
import os
import numpy as np
import pytest


# Add parent directory to sys.path to import calculator
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import calculator  

def test_normalised_difference():
    test_a = np.array([1, 2, 3, 4])
    test_b = np.array([2, 3, 4, 5])

    expected = [0.3333, 0.2, 0.1429, 0.1111]
    result = calculator.normalised_difference(band_a=test_a, band_b=test_b)

    # Compare values approximately to avoid float errors
    for r, e in zip(result, expected):
        assert pytest.approx(r, 0.001) == e

def test_normalised_difference_zero():
    test_a = np.array([0, 2, 1, 0])
    test_b = np.array([0, 3, 1, 0])

    expected = [np.nan, 0.2, 0, np.nan]
    result = calculator.normalised_difference(band_a=test_a, band_b=test_b)

    for r, e in zip(result, expected):
        if np.isnan(e):
            assert np.isnan(r)
        else:
            assert pytest.approx(r, 0.001) == e

def test_summary_stats():
    test_a = np.array([1, 2, 3, 4])

    result = calculator.summary_stats(test_a)

    expected = {
        "mean": 2.5, 
        "min": 1,
        "max": 4,
        "std": 1.118033988749895,
        "median": 2.5
    }

    assert pytest.approx(expected) == result