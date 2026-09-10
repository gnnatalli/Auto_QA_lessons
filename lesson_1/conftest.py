from calculator import Calculator
import pytest


@pytest.fixture(scope="module")
def create_calculator():
    return Calculator()