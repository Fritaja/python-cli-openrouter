import pytest
from main import greet

def test_greet_valid_name():
    result = greet("Goran")
    assert result == "Hello, Goran!"

def test_greet_with_spaces():
    result = greet("   Goran   ")
    assert result == "Hello, Goran!"

def test_greet_empty_name():
    with pytest.raises(ValueError):
        greet("")

def test_greet_whitespace_only():
    with pytest.raises(ValueError):
        greet("   ")
