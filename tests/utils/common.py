import random
import string


def random_str(length: int) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_email() -> str:
    return f"{random_str(30)}@{random_str(15)}.com"


def random_int(start: int = 0, end: int = 2*32) -> int:
    return random.randint(start, end)
