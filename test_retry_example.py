from retry_example import calculate_delay


def test_calculate_delay():
    assert calculate_delay(0) == 1
    assert calculate_delay(1) == 2
    assert calculate_delay(2) == 4
    assert calculate_delay(3) == 8
