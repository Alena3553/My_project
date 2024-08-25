import classes
import pytest


def test_username():
    with pytest.raises(classes.User_name_Error):
        classes.User("a", "1111111")


def test_password():
    with pytest.raises(classes.Password_error):
        classes.User("Alena", "11")


def test_client_name():
    with pytest.raises(classes.Name_error):
        classes.Client("1111111", "a", "hair")


def test_client_phone():
    with pytest.raises(classes.Phone_number_error):
        classes.Client("11", "Alena", "nails")


def test_service():
    with pytest.raises(classes.Service_error):
        classes.Client("111111", "Alena", "toes")
