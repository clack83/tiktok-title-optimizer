import json
import time
import logging

from openai import OpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)


class DeepSeekClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url,
        )
        self.model = settings.deepseek_model
        self.max_retries = 3
        self.base_delay = 1.0

    def chat_completion(self, system_prompt: str, user_prompt: str, temperature: float = 0.8) -> dict:
        last_error = None
        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=temperature,
                    max_tokens=2000,
                    response_format={"type": "json_object"},
                )
                content = response.choices[0].message.content
                return json.loads(content)
            except json.JSONDecodeError as e:
                logger.warning(f"DeepSeek response parse error (attempt {attempt + 1}): {e}")
                last_error = e
            except Exception as e:
                logger.warning(f"DeepSeek API error (attempt {attempt + 1}): {e}")
                last_error = e
                if attempt < self.max_retries - 1:
                    delay = self.base_delay * (2 ** attempt)
                    time.sleep(delay)

        raise RuntimeError(f"DeepSeek API 调用失败（已重试{self.max_retries}次）: {last_error}")


deepseek_client = DeepSeekClient()
