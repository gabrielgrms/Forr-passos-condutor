import random

from app.schemas import RandomizationResponse, SequencePair, StepRead


def generate_sequences(steps: list[StepRead]) -> RandomizationResponse:
    left_steps = [step for step in steps if step.starts_with_left_free]
    right_steps = [step for step in steps if not step.starts_with_left_free]

    random.shuffle(left_steps)
    random.shuffle(right_steps)

    pairs: list[SequencePair] = []

    while left_steps and right_steps:
        first_from_left = random.choice([True, False])
        if first_from_left:
            first = left_steps.pop()
            second = right_steps.pop()
        else:
            first = right_steps.pop()
            second = left_steps.pop()
        pairs.append(SequencePair(first=first, second=second))

    leftovers = left_steps + right_steps
    return RandomizationResponse(pairs=pairs, leftovers=leftovers)
