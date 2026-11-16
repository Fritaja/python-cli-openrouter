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

def test_main_empty_then_valid_name(monkeypatch, capsys):
    inputs = iter(["", "Goran"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    main()

    captured = capsys.readouterr()
    assert captured.out == "Error: Name cannot be empty\nHello, Goran!\n"

def test_main_whitespace_then_valid_name(monkeypatch, capsys):
    inputs = iter(["   ", "Goran"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    main()

    captured = capsys.readouterr()
    assert captured.out == "Error: Name cannot be empty\nHello, Goran!\n"

def test_main_asks_again_until_valid(monkeypatch, capsys):
    calls = []
    inputs = iter(["", "  ", "Goran"])

    def fake_input(prompt):
        calls.append(prompt)
        return next(inputs)

    monkeypatch.setattr("builtins.input", fake_input)

    main()

    captured = capsys.readouterr()
    assert len(calls) == 3
    assert captured.out == (
        "Error: Name cannot be empty\n"
        "Error: Name cannot be empty\n"
        "Hello, Goran!\n"
    )
