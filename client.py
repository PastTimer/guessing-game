import socket

HOST = "localhost"
PORT = 5050

repeat = False
count = 1

s = socket.socket()
s.connect((HOST, PORT))

data = s.recv(1024)

print(data.decode().strip())

def user():
    name = input("Enter your name: ").upper()
    s.sendall(name.encode())

def diff_choose():
    diff = input("""Choose a difficulty, default is easy:
                 - Easy
                 - Medium
                 - Hard
                 """).strip().lower()
    s.sendall(diff.encode())
    print("Enter guess: ")

user()
diff_choose()

while True:
    user_input = input("").strip()
    s.sendall(user_input.encode())
    reply = s.recv(1024).decode().strip()
    if "Correct" in reply:
        print(reply)
        print("Attemps in total: " + str(count))
        score = str(101-count)
        print("Score: " + score + "/100")
        s.sendall(score.encode())
        choice = input(str("Would you like to play again? y/n\n").lower()).strip()
        s.sendall(choice.encode())
        if choice == 'y':
            user()
            diff_choose()
            count = 1
        else:
            print("See you again!")
            break
    else:
        print(reply)
        count += 1
        continue
s.close()