import random
import string


def generate_opt(length=6) -> str:
    return "".join(random.choices(string.digits, k=length))
