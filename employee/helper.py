import secrets
import string


def generate_password():
    return "".join(
        secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
        for i in range(8)
    )