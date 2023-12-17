import hashlib


def sha256_hash(value: str) -> str:
    value_hash = hashlib.sha256(value.encode()).hexdigest()
    return value_hash
