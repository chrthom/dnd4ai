from .base import LLMAdapter
from .openai_adapter import OpenAIAdapter
from .anthropic_adapter import AnthropicAdapter


def create_adapter(llm_id: str) -> LLMAdapter:
    """Factory: resolve llm string from config.json to an adapter instance."""
    if llm_id.startswith("gpt-"):
        return OpenAIAdapter(model=llm_id)
    if llm_id.startswith("claude-"):
        return AnthropicAdapter(model=llm_id)
    raise ValueError(f"Unknown LLM: {llm_id}")
