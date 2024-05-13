import socket
import random
import pandas as pd

df = pd.read_csv('data.csv')

HOST = "localhost"
PORT = 5050
banner = """

== Guessing Game v1.1 =="""

def genrand(low, high):
    return random.randint(low, high)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

print(f"server is listening in port {PORT}")

guessme = 0
conn = None
repeat = False
    

def difficulty(mode):
    mode = mode.lower()
    if mode == "hard":
        n = genrand(1, 500)
        return n
    elif mode == "medium":
        n = genrand(1, 100)
        return n
    else:
        n = genrand(1, 50)
        return n

while True:
    if conn is None:
        print("[SEARCHING] connecting...")
        conn, addr = s.accept()
        print(f"new client: {addr[0]}")
        conn.sendall(banner.encode())
        username = conn.recv(1024).decode().strip()
        mode = conn.recv(1024).decode().strip()
        print(df)
        guessme = difficulty(mode)
        print(guessme)
    elif repeat is True:
        username = conn.recv(1024).decode().strip()
        mode = conn.recv(1024).decode().strip()
        print(df)
        guessme = difficulty(mode)
        print(guessme)
        repeat = False
    else:
        client_input = conn.recv(1024).decode().strip()
        print(f"User guess attempt: {client_input}")
        if client_input.isdigit():
            guess = int(client_input)
            if guess == guessme:
                conn.sendall(b"Correct Answer!")
                score = int(conn.recv(1024).decode().strip())
                new_row = pd.DataFrame({'Name': [username], 'Score': [score], 'Difficulty': [mode]})
                df = df._append(new_row, ignore_index=True)
                choice = conn.recv(1024).decode().strip()
                if choice == 'n':
                    df = df.sort_values(by='Score', ascending=False)
                    print(df)
                    df.to_csv('data.csv', index=True)
                    break
                else:
                    df = df.sort_values(by='Score', ascending=False)
                    print(df)
                    repeat = True
                continue
            elif guess > guessme:
                conn.sendall(b"Guess Lower!:")
                continue
            elif guess < guessme:
                conn.sendall(b"Guess Higher!:")
                continue
        else:
            conn.sendall(b"Invalid input. Please enter a number.")


