import hashlib


def hash_pass(password: str):
    hash_object = hashlib.md5(password.encode("utf8"))
    print(hash_object.hexdigest())
    return hash_object.hexdigest()
