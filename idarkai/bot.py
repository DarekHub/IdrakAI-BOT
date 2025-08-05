import requests


class IdarkAi:
    """Basic IdarkAi bot interface."""

    def __init__(self, provider: str = "openai", api_key: str | None = None, base_url: str | None = None) -> None:
        self.provider = provider
        self.api_key = api_key
        self.base_url = base_url

    def ask(self, prompt: str) -> str:
        """Send *prompt* to the configured provider and return text response."""
        if self.provider == "openai":
            return self._ask_openai(prompt)
        if self.provider == "gemini":
            return self._ask_gemini(prompt)
        if self.provider == "deepseek":
            return self._ask_deepseek(prompt)
        raise ValueError(f"Unknown provider: {self.provider}")

    def _ask_openai(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("OpenAI API key is required")
        headers = {"Authorization": f"Bearer {self.api_key}"}
        json = {"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}]}
        response = requests.post(
            self.base_url or "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def _ask_gemini(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("Gemini API key is required")
        json = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(
            self.base_url or "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            params={"key": self.api_key},
            json=json,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]

    def _ask_deepseek(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("DeepSeek API key is required")
        headers = {"Authorization": f"Bearer {self.api_key}"}
        json = {"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}]}
        response = requests.post(
            self.base_url or "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=json,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def fetch_url(self, url: str) -> str:
        """Fetch plain text from a URL."""
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text

    def train(self, data: list[str]) -> str:
        """Placeholder training method."""
        return f"Training with {len(data)} records is not implemented yet."
