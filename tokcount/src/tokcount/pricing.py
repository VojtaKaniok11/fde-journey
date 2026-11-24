import tiktoken

MODEL_PRICING: dict[str, tuple[float, float]] = {
    "gpt-4o": (2.50, 10.00),
    "gpt-4o-mini": (0.15, 0.60),
    "claude-3-5-sonnet": (3.00, 15.00),
}

def count_tokens(text: str, model: str = "gpt-4o") -> int:
    """Spočítá počet tokenů v textu pro daný model."""
    encoding = tiktoken.get_encoding("o200k_base")
    tokens = encoding.encode(text)
    return len(tokens)

def estimate_cost(input_tokens: int, output_tokens: int, model: str) -> float:
    """Odhadne cenu volání v USD podle počtu vstupních a výstupních tokenů."""
    if model not in MODEL_PRICING:
        raise ValueError(f"Neznámý model: {model}. Dostupné: {list(MODEL_PRICING.keys())}")

    input_price_per_m, output_price_per_m = MODEL_PRICING[model]
    input_cost = (input_tokens / 1_000_000) * input_price_per_m
    output_cost = (output_tokens / 1_000_000) * output_price_per_m
    return round(input_cost + output_cost, 6)