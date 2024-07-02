import hashlib

## using SHA56 for masking because it handles duplicates easily by assigning the same hash values to duplicate entries
def mask_value(value):
    return hashlib.sha256(value.encode()).hexdigest()

