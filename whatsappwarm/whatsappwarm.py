
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

# --- CONFIGURATION ---

# List your accounts here. Each entry should point to a Chrome user‑data directory
# where WhatsApp Web is already logged in (i.e. you scanned the QR once).
# Optionally include proxy (format "host:port") if you want per‑account proxies.
ACCOUNTS = [
    {
        "profile_dir": "/path/to/chrome-profile-whatsapp-account1",
        "proxy": None,  # e.g. "123.45.67.89:8000"
        "target": "Your Test Contact",   # exact name as shown in WhatsApp
        "message": "🤖 Warm‑up ✅"
    },
    {
        "profile_dir": "/path/to/chrome-profile-whatsapp-account2",
        "proxy": "11.22.33.44:3128",
        "target": "Your Test Group",
        "message": "🤖 Warm‑up from account 2!"
    },
    # add more accounts as needed...
]

# Path to your chromedriver (or use webdriver_manager)
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
# How long to wait for chats to load (seconds)
WAIT_LOAD = 15


def launch_driver(profile_dir: str, proxy: str = None):
    """Launch Chrome with a specific user‑data profile and optional proxy."""
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={profile_dir}")
    # Disable notifications bar pop-ups
    options.add_argument("--disable-notifications")
    if proxy:
        options.add_argument(f"--proxy-server=http://{proxy}")
    return webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)


def warm_up_account(account):
    driver = launch_driver(account["profile_dir"], account["proxy"])
    try:
        # 1) Open WhatsApp Web
        driver.get("https://web.whatsapp.com")
        # 2) Wait for page to load & user to be logged in
        time.sleep(WAIT_LOAD)

        # 3) Click search box
        search_box = driver.find_element(By.XPATH, "//div[@contenteditable='true' and @data-tab='3']")
        search_box.click()
        time.sleep(1)
        # 4) Type contact/group name
        search_box.send_keys(account["target"])
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)

        # 5) Find the message input box
        input_box = driver.find_element(By.XPATH, "//div[@contenteditable='true' and @data-tab='10']")
        input_box.click()
        # 6) Send the warm‑up message
        input_box.send_keys(account["message"])
        input_box.send_keys(Keys.ENTER)
        time.sleep(2)

        print(f"[+] Warm‑up message sent for {account['profile_dir']}")
    except Exception as e:
        print(f"[!] Error warming {account['profile_dir']}: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    for acct in ACCOUNTS:
        if not os.path.isdir(acct["profile_dir"]):
            print(f"[!] Profile dir not found: {acct['profile_dir']}. Skipping.")
            continue
        warm_up_account(acct)
        # small delay between accounts
        time.sleep(5)
