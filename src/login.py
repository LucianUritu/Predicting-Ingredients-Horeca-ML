import os

def load_credentials(filepath):
    # Always resolve path relative to this script's directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    abs_path = os.path.join(base_dir, "users.txt")
    with open(abs_path, "r") as f:
        line = f.readline().strip()
        username, password = line.split(":")
        return username, password

def check_login(username_input, password_input):
    username, password = load_credentials("users.txt")
    return username_input == username and password_input == password