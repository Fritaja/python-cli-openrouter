import pytest
from main import greet, main

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

def test_greet_invalid_type():
    with pytest.raises(TypeError):
        greet(None)

def test_main_valid_name(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "Goran")

    main()

    captured = capsys.readouterr()
    assert captured.out == "Hello, Goran!\n"

def test_main_empty_name(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "")

    main()

    captured = capsys.readouterr()
    assert captured.out == "Error: Name cannot be empty\n"