import bcrypt

passwords = [
    "Test123",
    "Test123",
    "Test123"
]

for password in passwords:
    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    print(hashed.decode())