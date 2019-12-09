import random

INITIALISATION = {
    "vectoradd.asm": list(range(1,1001)) + list(range(1,1001))[::-1] + ([0] * 1000),
    "quicksort.asm": random.sample(range(1, 201), 100) + ([0]*(2048-100))
}