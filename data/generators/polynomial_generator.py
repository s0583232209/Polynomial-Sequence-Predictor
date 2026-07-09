import random
import csv
from pathlib import Path

import numpy as np


# -----------------------------
# Configuration
# -----------------------------

MAX_DEGREE = 5

MIN_COEFF = -10
MAX_COEFF = 10

INPUT_LENGTH = 8
NEXT_VALUES = 3


NUMBER_OF_SEQUENCES = 200000

OUTPUT_PATH = Path("../generated/polynomial_sequences.csv")


# -----------------------------
# Polynomial evaluation
# -----------------------------

def polynomial_value(coefficients, n):
    value = 0

    for power, coefficient in enumerate(coefficients):
        value += coefficient * (n ** power)

    return int(value)


# -----------------------------
# Generate one sequence
# -----------------------------
generated_sequences = set()
def generate_sequence():


    degree = random.randint(1, MAX_DEGREE)

    coefficients = [0] * (MAX_DEGREE + 1)

    coefficients[degree] = random.choice(
        [i for i in range(MIN_COEFF, MAX_COEFF + 1) if i != 0]
    )

    for i in range(degree):
        coefficients[i] = random.randint(
            MIN_COEFF,
            MAX_COEFF
        )

    length = INPUT_LENGTH

    sequence = []
    start_n = random.randint(-20, 30)

    for n in range(start_n, start_n + length):
        sequence.append(polynomial_value(coefficients, n))

    key = tuple(sequence)
    if key in generated_sequences:
        return generate_sequence()
    generated_sequences.add(key)

    next_values = []

    for n in range(start_n + length,start_n + length + NEXT_VALUES):
        next_values.append(polynomial_value(coefficients, n))

    return {

            "degree": degree,

            "coefficients": coefficients,

            "sequence": sequence,

            "next_values": next_values

         }


# -----------------------------
# Main
# -----------------------------

def main():

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_PATH,
        "w",
        newline="",
        encoding="utf8"
    ) as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow(

            [

                "degree",

                "coefficients",

                "input_sequence",

                "target_sequence"

            ]

        )

        for _ in range(NUMBER_OF_SEQUENCES):

            item = generate_sequence()

            writer.writerow(

                [

                    item["degree"],

                    ",".join(map(str, item["coefficients"])),

                    ",".join(map(str, item["sequence"])),

                    ",".join(map(str, item["next_values"]))

                ]

            )

    print("Dataset created successfully!")
    print("Saved to:", OUTPUT_PATH)


if __name__ == "__main__":
    main()