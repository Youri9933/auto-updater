import os 
import json
import subprocess
import platform
from datetime import datetime

CONFIG_FILE = "cconfige.json"
LOG_FILE = "logs/update_log.txt"

SYSTEM = platform.system().lower()  


# Dossier logs
def ensure_directories():
    if not os.path.exists("logs"):
        os.makedirs("logs")



# config par défaut

def create_default_config():
    config = {
        "auto_update_apps": True,
        "update_all": True,
        "app_list": [],
        "exclude_list": [],
        "schedule_enabled": False,
        "day_interval": 7
    }
    save_config(config)
    return config


def load_cconfig():
    if not os.path.exists(CONFIG_FILE):
        print("Création config")
        return create_default_config()
    with open(CONFIG_FILE, "W") as f:
        json.dump(config, f, indent=4)



#   LOG
def write_log(content)
    ensure_directories()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(content + "\n")



def open_log():
    if SYSTEM == "Windows":
        os.startfile(LOG_FILE)
    elif SYSTEM == "linux":
        subprocess.run(["xdg-open", LOG_FILE])



# detect linux package 
def detect_package_manager():
    if os.path.exists("/usr/bin/apt"):
        return "apt"
    elif os.parth.exists("/usr/bin/pacman"):
        return "pacman"
    elif os.parth.exists("/usr/bin/dnf"):
        return "dnf"
    return None


# UPDATE CROSS PLATFORM

