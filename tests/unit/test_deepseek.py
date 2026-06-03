import pytest
from unittest.mock import patch, MagicMock

from algorithms.optimizer.deepseek_client import DeepSeekClient


def test_deepseek_client_initialization():
    client = DeepSeekClient()
    assert client.model == "deepseek-chat"
    assert client.max_retries == 3
    assert client.base_delay == 1.0


@patch("algorithms.optimizer.deepseek_client.OpenAI")
def test_chat_completion_success(mock_openai):
    client = DeepSeekClient()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = '{"result": "ok"}'
    client.client.chat.completions.create.return_value = mock_response

    result = client.chat_completion("system", "user")
    assert result == {"result": "ok"}


@patch("algorithms.optimizer.deepseek_client.OpenAI")
@patch("algorithms.optimizer.deepseek_client.time")
def test_chat_completion_retry(mock_time, mock_openai):
    client = DeepSeekClient()
    client.client.chat.completions.create.side_effect = [
        Exception("API error"),
        Exception("API error"),
        _mock_response('{"result": "retry_ok"}'),
    ]

    result = client.chat_completion("system", "user")
    assert result == {"result": "retry_ok"}
    assert client.client.chat.completions.create.call_count == 3


@patch("algorithms.optimizer.deepseek_client.OpenAI")
def test_chat_completion_all_retries_fail(mock_openai):
    client = DeepSeekClient()
    client.client.chat.completions.create.side_effect = Exception("API down")

    with pytest.raises(RuntimeError, match="重试"):
        client.chat_completion("system", "user")


def _mock_response(content: str):
    m = MagicMock()
    m.choices = [MagicMock()]
    m.choices[0].message.content = content
    return m
