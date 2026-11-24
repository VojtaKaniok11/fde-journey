import pytest
from pydantic import ValidationError

from tokcount.pricing import count_tokens, estimate_cost


def test_count_tokens_empty() -> None:
    assert count_tokens("") == 0


def test_count_tokens_non_empty() -> None:
    assert count_tokens("Ahoj světe, testujeme Python!") > 0


def test_estimate_cost_gpt4o() -> None:
    # 1 000 000 vstupních ($2.50) + 1 000 000 výstupních ($10.00) = $12.50
    estimate = estimate_cost(1_000_000, 1_000_000, model="gpt-4o")
    assert estimate.total_cost_usd == 12.5
    assert estimate.model == "gpt-4o"


def test_estimate_cost_unknown_model() -> None:
    with pytest.raises(ValueError, match="Neznámý model"):
        estimate_cost(100, 100, model="neexistujici-model")


def test_estimate_cost_negative_tokens() -> None:
    # Ověříme, že Pydantic nepustí záporný počet tokenů (Field(ge=0))
    with pytest.raises(ValidationError):
        estimate_cost(-10, 100, model="gpt-4o")