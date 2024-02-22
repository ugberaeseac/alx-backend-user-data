#!/usr/bin/env python3
"""
End-to-end Integration test.
Use assert to validate the response expected
status code and payload (if any) for each task
"""


import requests
url = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    """
    test for register_user
    """
    data = {"email": email, "password": password}
    response = requests.post('{}/users'.format(url), data=data)
    assert response.status_code == 200, "Failed Test"


def log_in_wrong_password(email: str, password: str) -> None:
    """
    test for log_in_wrong_password
    """
    data = {"email": email, "password": password}
    response = requests.post('{}/sessions'.format(url), data=data)
    assert response.status_code == 401, "Failed Test"


def profile_unlogged() -> None:
    """
    test for profile_unlogged
    """
    data = {"session_id": ""}
    response = requests.get('{}/profile'.format(url), data=data)
    assert response.status_code == 403, "Failed Test"


def log_in(email: str, password: str) -> str:
    """
    test for log_in
    """
    data = {"email": email, "password": password}
    response = requests.post('{}/sessions'.format(url), data=data)
    assert response.status_code == 200, "Failed Test"
    session_id = response.cookies.get("session_id")
    return session_id


def profile_logged(session_id: str) -> None:
    """
    test for profile_logged
    """
    data = {"session_id": session_id}
    response = requests.get('{}/profile'.format(url), cookies=data)
    assert response.status_code == 200, "Failed Test"


def log_out(session_id: str) -> None:
    """
    test for log_out
    """
    data = {"session_id": session_id}
    response = requests.delete('{}/sessions'.format(url), cookies=data)
    assert response.status_code == 200, "Failed Test"


def reset_password_token(email: str) -> str:
    """
    test for reset_password_token
    """
    data = {"email": email}
    response = requests.post('{}/reset_password'.format(url), data=data)
    assert response.status_code == 200, "Failed Test"
    reset_token = response.json().get("reset_token")
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    test for update_password
    """
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put('{}/reset_password'.format(url), data=data)
    assert response.status_code == 200, "Failed Test"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
