import sys
import os
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style


path = sys.argv[1]
saved_pages = []
back_command_stack = []


def get_content_as_text(p_content):
    result = ""
    soup = BeautifulSoup(p_content, "html.parser")
    specified_tags = soup.find_all(['p', 'a', 'ul', 'ol', 'li', ['h{}'.format(i) for i in range(1, 7)]])
    for t in specified_tags:
        if t.name == "a":
            result += Fore.BLUE + t.get_text() + Style.RESET_ALL
        else:
            result += t.get_text()
    return result


def get_and_save_page_to_file(url):
    if "." not in url:
        print("error: incorrect URL")
        return
    alias = url[0:url.rfind(".")].replace("http://", "").replace("https://", "")
    if "http://" not in url and "https://" not in url:
        url = "https://" + url
    response = requests.get(url)
    content = get_content_as_text(response.content)
    with open(path + "\\" + alias + ".txt", mode="w") as file:
        file.write(str(content))
    saved_pages.append(alias)
    print(content)


def read_page_from_file(file_path):
    with open(file_path) as file:
        return file.read()


def process_user_input(p_user_input):
    if p_user_input in saved_pages:
        print(read_page_from_file(path + "\\" + p_user_input + ".txt"))
        back_command_stack.append(p_user_input)
    elif p_user_input == "back":
        if len(back_command_stack) > 0:
            back_user_input = back_command_stack[len(back_command_stack) - 2]
            process_user_input(back_user_input)
    else:
        get_and_save_page_to_file(p_user_input)
        back_command_stack.append(p_user_input)


# write your code here
user_input = ""
if not os.path.isdir(path):
    os.mkdir(path)
while user_input != "exit":
    user_input = input()
    if user_input != "exit":
        process_user_input(user_input)
