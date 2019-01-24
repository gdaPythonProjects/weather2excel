from ..ui_functions import *
import pytest


@pytest.mark.parametrize("test_data_from_user, test_MIN_expected_value, test_MAX_expected_value, expected_output",
                         [
                             ('23.4', -90, 90, (1, 1, 23.4)),  # prawidłowa wartość - OK
                             ('55,7', -90, 90, (1, 1, 55.7)),  # przecinek zamiast kropki - OK
                             ('-45', -90, 90, (1, 1, -45)),  # ujemne wartości - OK
                             ('134', -90, 90, (1, 0, None)),  # wartość poza zakresem - BŁĄD
                             ('-1', -90, 90, (1, 0, None)),  # wartość poza zakresem - BŁĄD
                             ('deed', -90, 90, (0, 0, None))  # słowo - BŁĄÐ
                         ]
                         )
def test_check_GPS_value_from_user(test_data_from_user, test_MIN_expected_value, test_MAX_expected_value,
                                   expected_output):
    result = check_GPS_value_from_user(test_data_from_user, test_MIN_expected_value, test_MAX_expected_value)
    assert result == expected_output


# region test of check_user_choice_is_correct(data_from_user, *args)
def test_check_user_choice_is_correct_param1():
    result = check_user_choice_is_correct("4", ["1", "2", "3"])
    assert result is None


def test_check_user_choice_is_correct_param2():
    result = check_user_choice_is_correct(3, ["1", "2", "3", "4"])
    assert result is None


def test_check_user_choice_is_correct_param3():
    result = check_user_choice_is_correct("3", [1, 2, 3, 4])
    assert result is None


def test_check_user_choice_is_correct_param4():
    result = check_user_choice_is_correct("3", ["1", "2", "3", "4"])
    assert result == "3"


def test_check_user_choice_is_correct_param5():
    result = check_user_choice_is_correct("two", ["one", "two", "three", "four"])
    assert result == "two"


def test_check_user_choice_is_correct_param6():
    result = check_user_choice_is_correct("two", ("one", "two", "three", "two", "four"))
    assert result == "two"


def test_check_user_choice_is_correct_param7():
    result = check_user_choice_is_correct(3, (1, 2, 3, 4, 5))
    assert result == 3

# endregion
