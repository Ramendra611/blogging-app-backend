import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


if __name__ == "__main__":
    password = "mahesh123"
    print(hash_password(password))