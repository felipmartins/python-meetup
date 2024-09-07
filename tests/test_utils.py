from unittest.mock import mock_open, patch
from src.utils import (
    read_data,
    write_data,
)


@patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
def test_read_data(mock_file):
    result = read_data()
    mock_file.assert_called_once_with("database.json", "r")
    assert result == {"key": "value"}


@patch("builtins.open", new_callable=mock_open)
def test_write_data(mock_file):
    data = {"key": "value"}
    with patch("json.dump") as mock_json_dump:
        write_data(data)
        mock_file.assert_called_once_with("database.json", "w")
        mock_json_dump.assert_called_once_with(data, mock_file(), indent=4)
