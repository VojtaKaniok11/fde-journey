from dataclasses import dataclass

import tiktoken
from pydantic import BaseModel, Field


@dataclass(frozen=True)
class ModelPrice:
  input_per_million: float
  output_per_million: float

class UsageEstimate(BaseModel):
    model: str
    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)
    total_cost_usd: float = Field(ge=0.0)

MODEL_PRICING: dict[str, ModelPrice] = {
    "gpt-4o": ModelPrice(input_per_million=2.50, output_per_million=10.00),
    "gpt-4o-mini": ModelPrice(input_per_million=0.15, output_per_million=0.60),
    "claude-3-5-sonnet": ModelPrice(input_per_million= 3.00, output_per_million=15.00),
}

def count_tokens(text: str, model: str = "gpt-4o") -> int:
    """Spočítá počet tokenů v textu pro daný model."""
    encoding = tiktoken.get_encoding("o200k_base")
    tokens = encoding.encode(text)
    return len(tokens)

def estimate_cost(input_tokens: int, output_tokens: int, model: str) -> UsageEstimate:
    """Odhadne cenu volání v USD podle počtu vstupních a výstupních tokenů."""
    if model not in MODEL_PRICING:
        raise ValueError(f"Neznámý model: {model}. Dostupné: {list(MODEL_PRICING.keys())}")

    price = MODEL_PRICING[model]
    input_cost = (input_tokens / 1_000_000) * price.input_per_million
    output_cost = (output_tokens / 1_000_000) * price.output_per_million
    total = round(input_cost + output_cost, 6)

    return UsageEstimate(
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_cost_usd=total,
    )
