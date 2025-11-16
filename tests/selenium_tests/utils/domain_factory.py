import os
import random
import string


def random_domain():
    return f"{''.join(random.choices(string.ascii_lowercase, k=8))}.com"


def generate_domain_file(directory, count=5):
    domains = [random_domain() for _ in range(count)]
    file_path = os.path.join(directory, "test_domains.txt")

    with open(file_path, "w") as f:
        f.write("\n".join(domains))

    return file_path, domains
