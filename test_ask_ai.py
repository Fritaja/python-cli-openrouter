import importlib
import json
import urllib.error

import pytest

import ask_ai


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


def make_result(content="Hi", finish_reason="stop"):
    return {
        "choices": [
            {
                "message": {"content": content},
                "finish_reason": finish_reason,
            }
        ],
        "model": "recursive/flint-v1.0:free",
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 5,
            "total_tokens": 15,
            "completion_tokens_details": {"reasoning_tokens": 2},
        },
    }


def make_http_error(code):
    return urllib.error.HTTPError(
        "https://openrouter.ai/api/v1/chat/completions",
        code,
        "Test error",
        {},
        None,
    )


def test_import_does_not_ask_or_call_api(monkeypatch, capsys):
    def fail(*args, **kwargs):
        raise AssertionError("Called during import")

    monkeypatch.setattr("builtins.input", fail)
    monkeypatch.setattr("urllib.request.urlopen", fail)
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    importlib.reload(ask_ai)

    assert capsys.readouterr().out == ""


@pytest.mark.parametrize(
    "finish_reason, expected",
    [("length", True), ("stop", False), (None, False)],
)
def test_is_response_incomplete(finish_reason, expected):
    assert ask_ai.is_response_incomplete(finish_reason) is expected


def test_main_prints_response_details(monkeypatch, capsys):
    monkeypatch.setattr(ask_ai.os, "getenv", lambda name: "test-key")
    monkeypatch.setattr("builtins.input", lambda prompt: "Hello")
    monkeypatch.setattr(
        ask_ai,
        "ask_model",
        lambda question, api_key: make_result(),
    )

    ask_ai.main()

    output = capsys.readouterr().out
    assert "AI response:\nHi\n" in output
    assert "Model: recursive/flint-v1.0:free\n" in output
    assert "Input tokens: 10\n" in output
    assert "Output tokens: 5\n" in output
    assert "Total tokens: 15\n" in output
    assert "Finish reason: stop\n" in output
    assert "Reasoning tokens: 2\n" in output
    assert "WARNING" not in output


def test_main_shows_warning_when_incomplete(monkeypatch, capsys):
    monkeypatch.setattr(ask_ai.os, "getenv", lambda name: "test-key")
    monkeypatch.setattr("builtins.input", lambda prompt: "Hello")
    monkeypatch.setattr(
        ask_ai,
        "ask_model",
        lambda question, api_key: make_result(finish_reason="length"),
    )

    ask_ai.main()

    output = capsys.readouterr().out
    assert "WARNING: AI response was cut off.\n" in output
    assert "The model reached the token limit.\n" in output


def test_main_handles_none_answer(monkeypatch, capsys):
    monkeypatch.setattr(ask_ai.os, "getenv", lambda name: "test-key")
    monkeypatch.setattr("builtins.input", lambda prompt: "Hello")
    monkeypatch.setattr(
        ask_ai,
        "ask_model",
        lambda question, api_key: make_result(content=None),
    )

    ask_ai.main()

    output = capsys.readouterr().out
    assert "AI response:\n(No answer)\n" in output


def test_main_empty_question_exits(monkeypatch):
    monkeypatch.setattr(ask_ai.os, "getenv", lambda name: "test-key")
    monkeypatch.setattr("builtins.input", lambda prompt: "   ")

    def fail(question, api_key):
        raise AssertionError("ask_model should not be called")

    monkeypatch.setattr(ask_ai, "ask_model", fail)

    with pytest.raises(SystemExit, match="Question cannot be empty"):
        ask_ai.main()


def test_main_missing_api_key_exits_before_input(monkeypatch):
    monkeypatch.setattr(ask_ai.os, "getenv", lambda name: None)

    def fail_input(prompt):
        raise AssertionError("input should not be called")

    def fail_model(question, api_key):
        raise AssertionError("ask_model should not be called")

    monkeypatch.setattr("builtins.input", fail_input)
    monkeypatch.setattr(ask_ai, "ask_model", fail_model)

    with pytest.raises(SystemExit, match="API key is missing"):
        ask_ai.main()


def test_ask_model_sends_expected_request(monkeypatch):
    result = make_result()
    captured = {}

    def fake_urlopen(request, timeout):
        captured["request"] = request
        captured["timeout"] = timeout
        return FakeResponse(result)

    monkeypatch.setattr(ask_ai.urllib.request, "urlopen", fake_urlopen)

    returned = ask_ai.ask_model("Hello", "test-key")

    request = captured["request"]
    assert captured["timeout"] == 60
    assert request.full_url == "https://openrouter.ai/api/v1/chat/completions"
    assert request.get_method() == "POST"
    assert "Bearer test-key" in request.headers.values()
    assert "application/json" in request.headers.values()
    assert json.loads(request.data) == {
        "model": "recursive/flint-v1.0:free",
        "messages": [{"role": "user", "content": "Hello"}],
        "max_completion_tokens": 300,
    }
    assert returned == result


def test_ask_model_handles_http_error(monkeypatch, capsys):
    def fake_urlopen(request, timeout):
        raise urllib.error.HTTPError(
            "https://openrouter.ai/api/v1/chat/completions",
            401,
            "Unauthorized",
            {},
            None,
        )

    monkeypatch.setattr(ask_ai.urllib.request, "urlopen", fake_urlopen)

    assert ask_ai.ask_model("Hello", "test-key") is None
    assert capsys.readouterr().out == "HTTP Error: 401\n"


def test_ask_model_handles_url_error(monkeypatch, capsys):
    def fake_urlopen(request, timeout):
        raise urllib.error.URLError("offline")

    monkeypatch.setattr(ask_ai.urllib.request, "urlopen", fake_urlopen)

    assert ask_ai.ask_model("Hello", "test-key") is None
    assert capsys.readouterr().out == "Connection Error: offline\n"


def test_ask_model_success_without_retry(monkeypatch):
    result = make_result()
    calls = []
    sleeps = []

    def fake_urlopen(request, timeout):
        calls.append(timeout)
        return FakeResponse(result)

    monkeypatch.setattr(ask_ai.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(ask_ai.time, "sleep", lambda seconds: sleeps.append(seconds))

    assert ask_ai.ask_model("Hello", "test-key") == result
    assert calls == [60]
    assert sleeps == []


def test_ask_model_retries_429_then_succeeds(monkeypatch, capsys):
    result = make_result()
    responses = iter([make_http_error(429), FakeResponse(result)])
    calls = []
    sleeps = []

    def fake_urlopen(request, timeout):
        calls.append(timeout)
        response = next(responses)
        if isinstance(response, Exception):
            raise response
        return response

    monkeypatch.setattr(ask_ai.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(ask_ai.time, "sleep", lambda seconds: sleeps.append(seconds))

    assert ask_ai.ask_model("Hello", "test-key") == result
    assert calls == [60, 60]
    assert sleeps == [1]

    output = capsys.readouterr().out
    assert "HTTP Error: 429\n" in output
    assert "Retrying after 1s...\n" in output


def test_ask_model_stops_after_three_429_failures(monkeypatch, capsys):
    calls = []
    sleeps = []

    def fake_urlopen(request, timeout):
        calls.append(timeout)
        raise make_http_error(429)

    monkeypatch.setattr(ask_ai.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(ask_ai.time, "sleep", lambda seconds: sleeps.append(seconds))

    assert ask_ai.ask_model("Hello", "test-key") is None
    assert calls == [60, 60, 60]
    assert sleeps == [1, 2]

    output = capsys.readouterr().out
    assert output.count("HTTP Error: 429\n") == 3
    assert "Retrying after 1s...\n" in output
    assert "Retrying after 2s...\n" in output
    assert "Retrying after 4s..." not in output


def test_ask_model_does_not_retry_401(monkeypatch, capsys):
    calls = []
    sleeps = []

    def fake_urlopen(request, timeout):
        calls.append(timeout)
        raise make_http_error(401)

    monkeypatch.setattr(ask_ai.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(ask_ai.time, "sleep", lambda seconds: sleeps.append(seconds))

    assert ask_ai.ask_model("Hello", "test-key") is None
    assert calls == [60]
    assert sleeps == []
    assert capsys.readouterr().out == "HTTP Error: 401\n"
