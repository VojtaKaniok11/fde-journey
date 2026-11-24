import typer

from tokcount.pricing import MODEL_PRICING, count_tokens, estimate_cost

app = typer.Typer(help="Nástroj pro odhad počtu tokenů a ceny LLM volání.")


@app.command()
def check(
    text: str = typer.Argument(..., help="Text, pro který chceš spočítat tokeny."),
    model: str = typer.Option("gpt-4o", "--model", "-m", help="Název LLM modelu."),
    output_tokens: int = typer.Option(
        100, "--output", "-o", help="Odhadovaný počet výstupních tokenů."
    ),
) -> None:
    """Spočítá vstupní tokeny a odhadne celkovou cenu dotazu."""
    if model not in MODEL_PRICING:
        typer.secho(f"Chyba: Neznámý model '{model}'.", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    in_tokens = count_tokens(text, model=model)
    cost = estimate_cost(in_tokens, output_tokens, model=model)

    typer.echo(f"Model:          {model}")
    typer.echo(f"Vstupní tokeny: {in_tokens}")
    typer.echo(f"Výstupní (odhad): {output_tokens}")
    typer.secho(f"Odhadovaná cena: ${cost:.6f}", fg=typer.colors.GREEN, bold=True)


def main() -> None:
    app()