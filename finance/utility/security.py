import bcrypt


def get_hashed_string(string: str) -> str:
  salt = bcrypt.gensalt()
  return bcrypt.hashpw(string, salt)


def check_hashed_string(string: str, hashed: str) -> str:
  return bcrypt.checkpw(string, hashed)