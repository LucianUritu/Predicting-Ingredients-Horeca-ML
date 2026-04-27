def load_credentials(filepath):
    with open(filepath, "r") as f:
        line = f.readline().strip()
        username, password = line.split(":")
        return username, password

def check_login(username_input, password_input, filepath="src/users.txt"):
    username, password = load_credentials(filepath)
    return username_input == username and password_input == password