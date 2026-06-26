"""Lógica de sorteio por lista de nomes."""

import secrets
from dataclasses import dataclass


@dataclass
class DrawResult:
    name: str
    entry_index: int


def crypto_random_int(min_value: int, max_value: int) -> int:
    """Equivalente ao crypto.randomInt(min, max) — retorna min <= n < max."""
    if not isinstance(min_value, int) or not isinstance(max_value, int):
        raise TypeError("Os limites do sorteio devem ser números inteiros.")
    if min_value >= max_value:
        raise ValueError("Intervalo inválido para sorteio.")
    return min_value + secrets.randbelow(max_value - min_value)


def parse_names(text: str) -> list[str]:
    names: list[str] = []
    for line in text.splitlines():
        name = line.strip().lstrip("@")
        if name:
            names.append(name)
    return names


def build_pool(names: list[str], allow_duplicates: bool) -> list[str]:
    if allow_duplicates:
        return list(names)

    seen: set[str] = set()
    unique: list[str] = []
    for name in names:
        key = name.lower()
        if key not in seen:
            seen.add(key)
            unique.append(name)
    return unique


def crypto_sample(pool: list[str], quantity: int, allow_duplicates: bool) -> list[tuple[str, int]]:
    winners: list[tuple[str, int]] = []
    available = list(range(len(pool)))

    for _ in range(quantity):
        pick = crypto_random_int(0, len(available))
        index = available[pick]
        winners.append((pool[index], index + 1))
        if not allow_duplicates:
            available.pop(pick)

    return winners


def draw_winners(
    names: list[str],
    quantity: int,
    allow_duplicates: bool,
) -> list[DrawResult]:
    pool = build_pool(names, allow_duplicates)

    if not pool:
        raise ValueError("Nenhum participante encontrado para sortear.")

    if quantity < 1:
        raise ValueError("Informe pelo menos 1 ganhador.")

    if not allow_duplicates and quantity > len(pool):
        raise ValueError(
            "Participantes únicos insuficientes. "
            "Reduza a quantidade ou permita nomes duplicados."
        )

    results = crypto_sample(pool, quantity, allow_duplicates)

    return [DrawResult(name=name, entry_index=index) for name, index in results]
