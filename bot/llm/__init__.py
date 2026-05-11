from .base import LLMAdapter
from .openai_adapter import OpenAIAdapter
from .anthropic_adapter import AnthropicAdapter
from .groq_adapter import GroqAdapter
from .mistral_adapter import MistralAdapter
from .gemini_adapter import GeminiAdapter


def create_adapter(llm_id: str) -> LLMAdapter:
    """Factory: resolve llm string from config.json to an adapter instance."""
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
    raise ValueError(f"Unknown LLM: {llm_id}")
