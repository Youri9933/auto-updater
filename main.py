
import os
import json
import subprocess
import platform
from datetime import datetime

CONFIG_FILE = "config.json"
LOG_FILE = "logs/update_log.txt"

SYSTEM = platform.system().lower()

DEV_TOOLS = [
    "Git",
    "GitHub Desktop",
    "GitKraken",
    "Docker",
    "Docker Desktop",
    "Kubernetes",
    "Windows Terminal",
    "PowerShell",
    "WSL",
    "Curl",
    "7zip",
    "Visual Studio Code",
    "Visual Studio",
    "JetBrains Toolbox",
    "IntelliJ IDEA",
    "PyCharm",
    "WebStorm",
    "Android Studio",
    "Notepad++",
    "Node.js",
    "Python",
    "Java",
    ".NET SDK",
    "Go",
    "Rust",
    "PHP",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Redis",
    "SQLite",
    "Postman",
    "Insomnia",
    "AWS CLI",
    "Azure CLI",
    "Google Cloud SDK",
    "Terraform"
]

# Dossier logs
def ensure_directories():
    if not os.path.exists("logs"):
        os.makedirs("logs")


# config utilities
def save_config(config):
    ensure_directories()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)


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


def load_config():
    if not os.path.exists(CONFIG_FILE):
        print("Création config")
        return create_default_config()
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        print("Impossible de lire le fichier de configuration, création d'une config par défaut")
        return create_default_config()


#   LOG
def write_log(content):
    ensure_directories()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(content + "\n")


def open_log():
    try:
        if SYSTEM.startswith("win"):
            os.startfile(LOG_FILE)
        elif SYSTEM == "linux":
            subprocess.run(["xdg-open", LOG_FILE], check=False)
    except Exception:
        pass


def update_dev_tools():
    # only works on Windows with winget
    if not SYSTEM.startswith("win"):
        print("update_dev_tools: winget disponible uniquement sur Windows")
        return
    for tool in DEV_TOOLS:
        print(f"Update / Install: {tool}")
        subprocess.run(["winget", "install", "--id", tool, "-e", "--source", "winget"], check=False)


# detect linux package
def detect_package_manager():
    if os.path.exists("/usr/bin/apt") or os.path.exists("/usr/bin/apt-get"):
        return "apt"
    if os.path.exists("/usr/bin/pacman"):
        return "pacman"
    if os.path.exists("/usr/bin/dnf"):
        return "dnf"
    return None


# UPDATE CROSS PLATFORM
def update_apps(config):
    print("Mise à jour...")
    log = f"\n===== UPDATE {datetime.now()} ====\n"

    try:
        # WINDOWS
        if SYSTEM.startswith("win"):
            if config.get("update_all", True):
                res = subprocess.run(["winget", "upgrade", "--all"], capture_output=True, text=True)
                log += (res.stdout or res.stderr or "")
            else:
                for app in config.get("app_list", []):
                    if any(ex in app.lower() for ex in config.get("exclude_list", [])):
                        continue
                    res = subprocess.run(["winget", "upgrade", app], capture_output=True, text=True)
                    log += (res.stdout or res.stderr or "") + "\n"

        # LINUX
        elif SYSTEM == "linux":
            pm = detect_package_manager()
            if pm == "apt":
                subprocess.run(["sudo", "apt", "update"], check=False)
                res = subprocess.run(["sudo", "apt", "upgrade", "-y"], capture_output=True, text=True)
                log += (res.stdout or res.stderr or "")
            elif pm == "pacman":
                res = subprocess.run(["sudo", "pacman", "-Syu", "--noconfirm"], capture_output=True, text=True)
                log += (res.stdout or res.stderr or "")
            elif pm == "dnf":
                subprocess.run(["sudo", "dnf", "check-update"], check=False)
                res = subprocess.run(["sudo", "dnf", "upgrade", "-y"], capture_output=True, text=True)
                log += (res.stdout or res.stderr or "")
            else:
                log += " Aucun gestionnaire de paquets détecté\n"
                print("Linux non supporté")

        print("Terminé")

    except Exception as e:
        log += f"Erreur : {e}\n"
        print("Erreur")

    write_log(log)
    open_log()


# SCHEDULER
def setup_scheduler(config):
    interval = str(config.get("day_interval", 7))
    if SYSTEM.startswith("win"):
        subprocess.run([
            "schtasks",
            "/Create",
            "/SC", "DAILY",
            "/MO", interval,
            "/TN", "AutoUpdater",
            "/TR", f'python "{os.path.abspath(__file__)}"',
            "/F"
        ], check=False)
    elif SYSTEM == "linux":
        cron_job = f"0 0 */{interval} * * python3 {os.path.abspath(__file__)}"
        subprocess.run(f'(crontab -l 2>/dev/null; echo "{cron_job}") | crontab -', shell=True, check=False)
    print("Scheduler activé")


def remove_scheduler():
    if SYSTEM.startswith("win"):
        subprocess.run(["schtasks", "/Delete", "/TN", "AutoUpdater", "/F"], check=False)
    elif SYSTEM == "linux":
        subprocess.run("crontab -r", shell=True, check=False)
    print("Scheduler supprimé")


# MENU
def config_menu(config):
    print("\nConfig")
    print("1 - Toggle update_all")
    print("2 - Ajouter app")
    print("3 - Ajouter exclusion")
    print("4 - Scheduler ON")
    print("5 - Scheduler OFF")
    print("0 - Retour")

    choice = input("Choix : ")

    if choice == "1":
        config["update_all"] = not config.get("update_all", True)

    elif choice == "2":
        app = input("Nom app : ")
        config.setdefault("app_list", []).append(app)

    elif choice == "3":
        exel = input("Nom à exclure : ")
        config.setdefault("exclude_list", []).append(exel)

    elif choice == "4":
        config["schedule_enabled"] = True
        setup_scheduler(config)

    elif choice == "5":
        config["schedule_enabled"] = False
        remove_scheduler()

    save_config(config)


# MAIN
def main():
    ensure_directories()
    config = load_config()

    while True:
        print("\n=== AUTO UPDATER ====")
        print("os détecté :", SYSTEM)
        print("1 - Update")
        print("2 - Config")
        print("0 - Quitter")

        choice = input("Choix : ")

        if choice == "1":
            update_apps(config)
        elif choice == "2":
            config_menu(config)
        elif choice == "0":
            break


if __name__ == "__main__":
    main()
