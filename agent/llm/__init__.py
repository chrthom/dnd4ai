import os

from .base import LLMAdapter
from .hub_adapter import HubAdapter
from .openai_adapter import OpenAIAdapter
from .anthropic_adapter import AnthropicAdapter
from .groq_adapter import GroqAdapter
from .mistral_adapter import MistralAdapter
from .gemini_adapter import GeminiAdapter


def create_adapter(llm_id: str) -> LLMAdapter:
    """Factory: erstellt den passenden Adapter abhängig von LLM_PROVIDER."""
    provider = os.environ.get("LLM_PROVIDER", "hub").lower()

    if provider == "hub":
        return HubAdapter(model=llm_id)

    if provider == "direct":
        if llm_id.startswith("gpt-"):
            return OpenAIAdapter(model=llm_id)
        if llm_id.startswith("claude-"):
            return AnthropicAdapter(model=llm_id)
        if llm_id.startswith("llama-") or llm_id.startswith("mixtral-") or llm_id.startswith("gemma-"):
            return GroqAdapter(model=llm_id)
        if llm_id.startswith("mistral-") or llm_id.startswith("open-mistral"):
            return MistralAdapter(model=llm_id)
        if llm_id.startswith("gemini-"):
            return GeminiAdapter(model=llm_id)
        raise ValueError(f"LLM_PROVIDER=direct: kein Adapter für '{llm_id}' gefunden")

    raise ValueError(f"Unbekannter LLM_PROVIDER: '{provider}'. Erlaubt: hub, direct")
