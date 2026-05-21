import random

from app.schemas import RandomizationResponse, SequencePair, StepRead


def _build_pairs(steps: list[StepRead]) -> list[SequencePair]:
    best_pairs: list[SequencePair] = []
    possible_edges = [
        (first, second)
        for first in steps
        for second in steps
        if first.id != second.id
        and first.ends_with_left_free == second.starts_with_left_free
    ]

    if not possible_edges:
        return best_pairs

    attempts = min(100, max(10, len(steps) * 5))
    for _ in range(attempts):
        shuffled_edges = possible_edges[:]
        random.shuffle(shuffled_edges)
        used_ids: set[int] = set()
        current_pairs: list[SequencePair] = []

        for first, second in shuffled_edges:
            if first.id in used_ids or second.id in used_ids:
                continue
            current_pairs.append(SequencePair(first=first, second=second))
            used_ids.add(first.id)
            used_ids.add(second.id)

        if len(current_pairs) > len(best_pairs):
            best_pairs = current_pairs

    return best_pairs


def generate_sequences(steps: list[StepRead]) -> RandomizationResponse:
    pairs = _build_pairs(steps)
    used_ids = {step.id for pair in pairs for step in (pair.first, pair.second)}
    leftovers = [step for step in steps if step.id not in used_ids]
    random.shuffle(leftovers)
    return RandomizationResponse(pairs=pairs, leftovers=leftovers)
