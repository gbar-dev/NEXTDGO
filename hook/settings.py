import random
import string
import os
def generate_secret_key(length=50):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.SystemRandom().choice(chars) for _ in range(length))

# Inject the key into the template
def run():
    secret_key = "{{ cookiecutter.SECRET_KEY }}"
    default_msg = "Leave empty to autogenerate a secure secret key"
    if not secret_key.strip() or secret_key == default_msg:
        secret_key = "{{ cookiecutter.SECRET_KEY }}"

    project_slug = "{{ cookiecutter.project_slug }}"
    env_dir = os.path.join(project_slug, "devops", "docker")
    os.makedirs(env_dir, exist_ok=True)

    with open(os.path.join(env_dir, ".env"), "w") as f:
        f.write(f"SECRET_KEY={secret_key}\n")