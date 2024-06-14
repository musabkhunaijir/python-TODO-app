import bcrypt


def hashPassword(plain_password):
    # TODO: move to env
    salt = b"$2a$12$w40nlebw3XyoZ5Cqke14M."
    return bcrypt.hashpw(b"{plain_password}", salt)


# TODO: check password
def verifyPassword(plain_password, stored_password):
    # converting password to array of bytes
    # bytes = plain_password.encode('utf-8')

    # # generating the salt
    # salt = bcrypt.gensalt()

    # # Hashing the password
    # hash = bcrypt.hashpw(bytes, salt)

    # # encoding user password
    # userBytes = plain_password.encode('utf-8')

    # checking password
    # return

    # my_salt = bcrypt.gensalt()
    hashed_pwd = hashPassword(plain_password)

    # print(hashed_pwd)
    # print(b"{stored_password}")
    # return

    # check = bcrypt.checkpw(b"{stored_password}", hashed_pwd)
    check = bcrypt.checkpw(b"{stored_password}", hashed_pwd)

    print("hash:", hashed_pwd.decode("utf-8"))
    print("sto", stored_password.encode("utf-8"))
    # print(bool(check))
    return check

    if check:
        return True
    else:
        return False
