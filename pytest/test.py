from datetime import date, timedelta
from io import BytesIO

import pytest

from module import (
    addition,
    divide,
    send_email,
    square,
    dict_merge,
    create_user,
    retrieve_user,
    is_negative,
    factorial,
    process_input,
    create_app,
    is_valid_url,
    write_file,
    read_file,
    calculate_date_difference,
    bubble_sort,
    find_matching,
    validate_email,
    memoized_function,
    serialize_to_json,
)

USER_EMAIL = 'user@example.com'


# 1. Unit Test: Testing a Simple Function
def test_addition():
    result = addition(2, 3)

    assert result == 5


# 2. Unit Test: Testing an Exception
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(5, 0)


# 3. Integration Test: Mocking External Service
def test_send_email_success(mocker):
    mocker.patch('smtplib.SMTP.sendmail', return_value={})
    result = send_email(USER_EMAIL, 'Test Subject', 'Test Message')

    assert result == 'Email sent successfully'


# 4. Parametrized Test: Testing Multiple Input Cases
@pytest.mark.parametrize("input_, expected_output", [(2, 4), (3, 9), (5, 25)])
def test_square(input_, expected_output):
    result = square(input_)

    assert result == expected_output


# 5. Unit Test: Testing a Complex Data Structure
def test_dict_merge():
    dict1 = {'a': 1, 'b': 2}
    dict2 = {'b': 3, 'c': 4}
    merged_dict = dict_merge(dict1, dict2)

    assert merged_dict == {'a': 1, 'b': 3, 'c': 4}


# 6. Integration Test: Testing Database Interaction
def test_create_and_retrieve_user():
    create_user(USER_EMAIL, 'password123')
    user = retrieve_user(USER_EMAIL)

    assert user.email == USER_EMAIL


# 7. Parametrized Test: Testing Edge Cases
@pytest.mark.parametrize("input_, expected_output",
                         [(-1, True), (0, True), (1, False)])
def test_is_negative(input_, expected_output):
    result = is_negative(input_)

    assert result == expected_output


# 8. Unit Test: Testing a Recursive Function
def test_factorial():
    result = factorial(5)

    assert result == 120


# 9. Unit Test: Testing Exception Messages
def test_invalid_input_exception():
    with pytest.raises(ValueError, match="Invalid input: must be a positive integer"):
        process_input(-1)


# 10. Integration Test: Testing API Endpoints
@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


def test_api_endpoint(client):
    response = client.get('/api/data')

    assert response.status_code == 200
    assert b'Success' in response.data


# 11. Parametrized Test: Testing URL Validation
@pytest.mark.parametrize("url, expected_result", [
    ('http://example.com', True),
    ('https://invalid', False),
    ('ftp://invalid', False),
])
def test_url_validation(url, expected_result):
    result = is_valid_url(url)

    assert result == expected_result


# 12. Unit Test: Testing File I/O
def test_read_and_write_file(tmp_path):
    file_path = tmp_path / "test_file.txt"
    write_file(file_path, "Hello, World!")
    content = read_file(file_path)

    assert content == "Hello, World!"


# 13. Unit Test: Testing Time-Based Functionality
def test_date_difference():
    date1 = date(2023, 10, 1)
    date2 = date(2023, 10, 5)
    difference = calculate_date_difference(date1, date2)

    assert difference == timedelta(days=4)


# 14. Integration Test: Testing Authentication
def test_authentication(client):
    response = client.post('/login', data={'username': 'user', 'password': 'password'})

    assert response.status_code == 200
    assert b'Authenticated' in response.data


# 15. Unit Test: Testing Sorting Algorithm
def test_bubble_sort():
    unsorted_list = [5, 2, 8, 1, 9]
    sorted_list = bubble_sort(unsorted_list)

    assert sorted_list == [1, 2, 5, 8, 9]


# 16. Integration Test: Testing File Upload
def test_file_upload(client):
    data = {'file': (BytesIO(b'file_content'), 'test_file.txt')}
    response = client.post('/upload', data=data, content_type='multipart/form-data')

    assert response.status_code == 200
    assert b'File uploaded successfully' in response.data


# 17. Unit Test: Testing Regular Expressions
def test_regex_matching():
    text = "This is a test string."
    pattern = r'\w+'
    matches = find_matching(text, pattern)

    assert matches == ['This', 'is', 'a', 'test', 'string']


# 18. Unit Test: Testing Data Validation
def test_validate_email():
    email = 'user@example.com'
    is_valid = validate_email(email)

    assert is_valid is True


# 19. Integration Test: Testing Cache Functionality
def test_cache_memoization():
    result1 = memoized_function(5)
    result2 = memoized_function(5)

    assert result1 == result2


# 20. Unit Test: Testing Data Serialization
def test_json_serialization():
    data = {'name': 'John', 'age': 30}
    json_data = serialize_to_json(data)

    assert json_data == '{"name": "John", "age": 30}'
