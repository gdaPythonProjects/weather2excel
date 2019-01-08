from ui_functions import *
import pytest


@pytest.mark.parametrize("test_data_from_user, test_MIN_expected_value, test_MAX_expected_value, expected_output",
                         [
                             ('23.4', 0, 90, (1, 1, 23.4)),  # prawidłowa wartość - OK
                             ('55,7', 0, 90, (1, 1, 55.7)),  # przecinek zamiast kropki - OK
                             ('134', 0, 90, (1, 0, None)),   # wartość poza zakresem - BŁĄD
                             ('-1', 0, 90, (1, 0, None)),    # wartość poza zakresem - BŁĄD
                             ('deed', 0, 90, (0, 0, None))   # słowo - BŁĄÐ
                         ]
                         )


def test_check_GPS_value_from_user(test_data_from_user, test_MIN_expected_value, test_MAX_expected_value, expected_output):

    result = check_GPS_value_from_user(test_data_from_user, test_MIN_expected_value, test_MAX_expected_value)

    assert result == expected_output
