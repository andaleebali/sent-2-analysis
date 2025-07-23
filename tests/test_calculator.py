import pytest
from .. import calculator

def normalised_difference_test():
    test_a = {1,2,3,4}
    test_b = {2,3,4,5}

    nd = calculator.normalised_difference(band_a=test_a, band_b=test_b)

    print(nd)