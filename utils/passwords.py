import hashlib


def hashPassword(plain_password):
    return hashlib.sha256(plain_password.encode()).hexdigest()


def verifyPassword(plain_password, stored_password):
    hashed_pwd = hashPassword(plain_password)
    return stored_password == hashed_pwd
