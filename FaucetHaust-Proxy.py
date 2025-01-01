import requests
import json
import time
import random
from fake_useragent import UserAgent
from colorama import Fore, init
import re
import os

init(autoreset=True)

# Constants
URL = "https://faucet-test.haust.network/api/claim"
PROXY = {
    "http": "http://username:password@ip:port",
    "https": "http://username:password@ip:port"
}
PAYLOAD = {"address": "xxxxxxxxxxxxx"}

def get_random_ua():
    user_agent = UserAgent().random
    while "Windows" not in user_agent:
        user_agent = UserAgent().random
    return user_agent

def get_time(message):
    match = re.search(r'Please wait (\d+)s', message)
    return int(match.group(1)) if match else 6.0

try:
    while True:
        user_agent = get_random_ua()
        headers = {"User-Agent": user_agent}
        proxies = PROXY

        try:
            response = requests.post(URL, headers=headers, data=json.dumps(PAYLOAD), proxies=proxies)
            if response.status_code == 200:
                data = response.json()
                print(Fore.GREEN + f"Success: {data['msg']}", end="")
                wait_time = random.uniform(2, 5)
            elif response.status_code == 429:
                wait_time = get_time(response.json().get("msg", "")) + random.uniform(1, 3)
                print(Fore.RED + f"Failed | Status Code: 429 | Reason: {response.json().get('msg')}", end="")
            else:
                wait_time = 3
                print(Fore.RED + f"Failed | Status Code: {response.status_code} | Reason: {response.text}", end="")
        except Exception as e:
            wait_time = 60
            print(Fore.RED + f"An unexpected error occurred: {e}", end="")
        
        print(Fore.BLUE + f" | Waiting for {wait_time:.2f} seconds...", flush=True)
        time.sleep(wait_time)

except KeyboardInterrupt:
    print(Fore.YELLOW + "Program stopped by user.")
