import random
import string


def rand_string():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))
