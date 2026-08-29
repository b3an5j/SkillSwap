import bcrypt

def encrypt_pwd(raw_pwd):
    salt = bcrypt.gensalt()
    pwd = str(bcrypt.hashpw(raw_pwd, salt))
    return pwd


def check_pwd(pwd, hashed):
    return bcrypt.checkpw(pwd, hashed)